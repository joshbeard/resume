#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Build script for my resume
#
# This sources the "resume.yaml" and produces the resume in several formats
# from Jinja2 templates, including HTML, plain text, Markdown, and Gemini.
# -----------------------------------------------------------------------------
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
import json
import markdown
import datetime
import os
import re
import sys

# -----------------------------------------------------------------------------
# Config
# Environment variables with defaults.
# -----------------------------------------------------------------------------


class Config(dict):
    """Config class."""

    def __getattr__(self, attr):
        if attr in self:
            item = self[attr]
            if isinstance(item, dict):
                return Config(item)
            return item
        raise AttributeError(f"Config has no attribute {attr}")


config = Config({
    'template_dir': os.environ.get('RESUME_TEMPLATE_DIR', 'templates'),
    'resume_yaml': os.environ.get('RESUME_YAML', 'resume.yaml'),
    'html': {
        'template': os.environ.get('RESUME_HTML_TEMPLATE', 'resume.html'),
        'out': os.environ.get('RESUME_HTML_OUT', 'dist/index.html'),
        'css_src': os.environ.get('RESUME_CSS_TEMPLATE', 'style.css'),
    },
    'markdown': {
        'template': os.environ.get('RESUME_MD_TEMPLATE', 'resume.md'),
        'out': os.environ.get('RESUME_MD_OUT', 'README.md'),
    },
    'gemini': {
        'template': os.environ.get('RESUME_GMI_TEMPLATE', 'resume.gmi'),
        'out': os.environ.get('RESUME_GMI_OUT', 'dist/resume.gmi'),
    },
    'txt': {
        'template': os.environ.get('RESUME_TXT_TEMPLATE', 'resume.txt'),
        'out': os.environ.get('RESUME_TXT_OUT', 'dist/resume.txt'),
        'narrow_template': os.environ.get('RESUME_TXT_NARROW_TEMPLATE',
                                          'resume-narrow.txt'),
        'narrow_out': os.environ.get('RESUME_TXT_NARROW_OUT',
                                     'dist/resume-narrow.txt'),
    },
    'json': {
        'out': os.environ.get('RESUME_JSON_OUT', 'dist/resume.json'),
    },
})

# -----------------------------------------------------------------------------

# Helpers
base_dir = os.path.dirname(os.path.realpath(__file__))

# Current date
current_date_time = datetime.datetime.now()
date = current_date_time.date()
year = date.strftime("%Y")


def md_strip(string: str):
    """Returns a string with Markdown URLs and emphasis removed.

    Parameters:
        string (str): The string to parse
    Returns:
        _s (str): A string with Markdown removed
    """
    _s = re.sub(r"\[([\w\s]+)\]\([\w\d\/\-\.:]+\)", "\\1", string)
    _s = re.sub(r"(\s+)__?(.*)__?(\s+)?", "\\1\\2\\3", _s)
    return _s


def resume(theformat='plain'):
    """Parses resume YAML, munges, and returns it as a dict.

    Returns:
        The resume content read from YAML as a dict
    """
    with open(config.resume_yaml, 'r') as file:
        resume_content = yaml.safe_load(file)

        if theformat == 'raw':
            return resume_content

        for i, job in enumerate(resume_content['experience']):
            if 'details' in job:
                details = []
                for detail in job['details']:
                    if theformat == 'plain':
                        details.append(md_strip(detail))
                    if theformat == 'html':
                        details.append(markdown.markdown(detail))
                    resume_content['experience'][i]['details'] = details

    return resume_content


def css():
    """Loads CSS source file and returns it as a string.

    Returns:
        The CSS from the compiled Jinja2 template as a string
    """
    css_file = os.path.join(config.template_dir, config.html.css_src)
    with open(css_file, 'r') as _file:
        css_content = _file.read()
    _file.close()
    return css_content


def build_template(**kwargs):
    """Compile Jinja2 template and return it as a string.

    Returns:
        A string containing the compiled resume template
    Keyword Arguments:
        source: The source template file
    """
    src_dir = FileSystemLoader(config.template_dir)
    env = Environment(loader=src_dir,
                      autoescape=select_autoescape(
                          enabled_extensions=('html')
                      ))
    src_file = env.get_template(kwargs['source'])

    return src_file.render(
        resume=resume(theformat=kwargs['theformat']), css=css(), year=year
    )


def write_out(**kwargs):
    """Write a file to disk."""
    file_out = os.path.join(base_dir, kwargs['target'])
    with open(file_out, 'w') as _file:
        _file.write(kwargs['content'])
    _file.close()
    print(f"-> Wrote {kwargs['target']}")


def gen_html():
    """Generate HTML file from Jina2 template."""
    html = build_template(source=config.html.template, theformat='html')
    write_out(target=config.html.out, content=html)


def gen_markdown():
    """Generate Markdown file from Jina2 template."""
    md = build_template(source=config.markdown.template,
                        autoescape=True, theformat='raw')
    write_out(target=config.markdown.out, content=md)


def gen_gemini():
    """Generate Gemini file from Jina2 template."""
    gmi = build_template(source=config.gemini.template, theformat='plain')
    write_out(target=config.gemini.out, content=gmi)


def gen_txt():
    """Generate plain text files from Jina2 template.

    A regular-width (<70 chars) and a narrow-width (<45 chars) file is created.
    """
    txt = build_template(source=config.txt.template, theformat='plain')
    write_out(target=config.txt.out, content=txt)

    narrow_txt = build_template(
        source=config.txt.narrow_template, theformat='plain')
    write_out(target=config.txt.narrow_out, content=narrow_txt)


def gen_json():
    """Generate JSON from converting the YAML source."""
    the_json = json.dumps(resume(theformat='plain'), indent=2)
    write_out(target=config.json.out, content=the_json)


def print_usage():
    """Print script usage."""
    print(f"{sys.argv[0]} [ html | md | gmi | txt ]")


def buill_all():
    """Build everything by default."""
    gen_html()
    gen_markdown()
    gen_gemini()
    gen_txt()
    gen_json()


if __name__ == '__main__':
    actions = {
        'html': gen_html,
        'md': gen_markdown,
        'markdown': gen_markdown,
        'gmi': gen_gemini,
        'gemini': gen_gemini,
        'txt': gen_txt,
        'text': gen_txt,
        'gopher': gen_txt,
        'json': gen_json,
        'help': print_usage,
    }
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in actions:
            actions[arg]()
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
    else:
        print("Building everything")
        buill_all()
