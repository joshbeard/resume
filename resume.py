#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Build script for my resume
#
# This sources the "resume.yaml" and produces the resume in several formats from
# Jinja2 templates, including HTML, plain text, Markdown, and Gemini (gmi).
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
template_dir = os.environ.get('RESUME_TEMPLATE_DIR', 'templates')

resume_yaml = os.environ.get('RESUME_YAML', 'resume.yaml')

# HTML
html_template = os.environ.get('RESUME_HTML_TEMPLATE', 'resume.html')
html_out = os.environ.get('RESUME_HTML_OUT', 'dist/index.html')
# css will be embedded in the html
css_file = os.environ.get('RESUME_CSS_TEMPLATE', 'style.css')

# Markdown
md_template = os.environ.get('RESUME_MD_TEMPLATE', 'resume.md')
md_out = os.environ.get('RESUME_MD_OUT', 'README.md')

# Gemini
gmi_template = os.environ.get('RESUME_GMI_TEMPLATE', 'resume.gmi')
gmi_out = os.environ.get('RESUME_GMI_OUT', 'resume.gmi')

# Plain Text
txt_template = os.environ.get('RESUME_TXT_TEMPLATE', 'resume.txt')
txt_out = os.environ.get('RESUME_TXT_OUT', 'resume.txt')
# Plain Text - narrow width (for Gopher, mobile)
narrow_txt_template = os.environ.get('RESUME_TXT_NARROW_TEMPLATE', 'resume-narrow.txt')
narrow_txt_out = os.environ.get('RESUME_TXT_NARROW_OUT', 'resume-narrow.txt')

# JSON
json_out = os.environ.get('RESUME_JSON_OUT', 'resume.json')
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


def resume(format='plain'):
    """Parses resume YAML, munges, and returns it as a dict.

    Returns:
        The resume content read from YAML as a dict
    """
    with open(resume_yaml, 'r') as file:
        resume_content = yaml.safe_load(file)

        if format == 'raw':
            return resume_content

        print(f'format: {format}')
        for i, job in enumerate(resume_content['experience']):
            if 'details' in job:
                details = []
                for detail in job['details']:
                    if format == 'plain':
                        # Create a new key with Markdown formatting removed (for
                        # plain text).
                        details.append(md_strip(detail))
                    if format == 'html':
                        # Create a new key with the HTMLified details
                        details.append(markdown.markdown(detail))
                    resume_content['experience'][i]['details'] = details

    return resume_content


def css():
    """Loads CSS source file and returns it as a string.

    Returns:
        The CSS from the compiled Jinja2 template as a string
    """
    with open(os.path.join(template_dir, css_file), 'r') as _file:
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
    src_dir = FileSystemLoader(template_dir)
    env = Environment(loader=src_dir,
                      autoescape=select_autoescape(enabled_extensions=('html')))
    src_file = env.get_template(kwargs['source'])

    return src_file.render(resume=resume(format=kwargs['format']), css=css(), year=year)


def write_out(**kwargs):
    """Write a file to disk."""
    file_out = os.path.join(base_dir, kwargs['target'])
    with open(file_out, 'w') as _file:
        _file.write(kwargs['content'])
    _file.close()
    print(f"-> Wrote {kwargs['target']}")


def gen_html():
    """Generate HTML file from Jina2 template."""
    html = build_template(source=html_template, format='html')
    write_out(target=html_out, content=html)


def gen_markdown():
    """Generate Markdown file from Jina2 template."""
    md = build_template(source=md_template, autoescape=True, format='raw')
    write_out(target=md_out, content=md)


def gen_gemini():
    """Generate Gemini file from Jina2 template."""
    gmi = build_template(source=gmi_template, format='plain')
    write_out(target=gmi_out, content=gmi)


def gen_txt():
    """Generate plain text files from Jina2 template.

    A regular-width (<70 chars) and a narrow-width (<45 chars) file is created.
    """
    txt = build_template(source=txt_template, format='plain')
    write_out(target=txt_out, content=txt)

    narrow_txt = build_template(source=narrow_txt_template, format='plain')
    write_out(target=narrow_txt_out, content=narrow_txt)


def gen_json():
    """Generate JSON from converting the YAML source."""
    the_json = json.dumps(resume(format='plain'), indent=2)
    write_out(target=json_out, content=the_json)


def print_usage():
    """Print script usage."""
    print(f"{sys.argv[0]} [ html | md | gmi | txt ]")


def main():
    """Build everything by default."""
    gen_html()
    gen_markdown()
    gen_gemini()
    gen_txt()
    gen_json()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == 'html':
            gen_html()
        elif arg in ('md', 'markdown'):
            gen_markdown()
        elif arg in ('gmi', 'gemini'):
            gen_gemini()
        elif arg in ('txt', 'text', 'gopher'):
            gen_txt()
        elif arg == 'json':
            gen_json()
        elif arg == 'help':
            print_usage()
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
    else:
        print("Building everything")
        main()
