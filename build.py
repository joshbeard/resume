#!/usr/bin/env python
from jinja2 import Template
import yaml
import markdown
import datetime
import re


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
resume_yaml = 'resume.yaml'

# HTML
html_template = 'src/resume.html'
html_out = "dist/index.html"
# css will be embedded in the html
css_file = "src/style.css"

# Markdown
md_template = 'src/resume.md'
md_out = "README.md"

# Gemini
gmi_template = 'src/resume.gmi'
gmi_out = "resume.gmi"

# Plain Text
txt_template = 'src/resume.txt'
txt_out = "resume.txt"
# Plain Text - narrow width (for Gopher, mobile)
narrow_txt_template = 'src/resume-45w.txt'
narrow_txt_out = "resume-45w.txt"
# -----------------------------------------------------------------------------

# Current date
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")


def md_strip(string):
    """Strip Markdown URLs and emphasis from a string"""
    _s = re.sub(r"\[([\w\s]+)\]\([\w\d\/\-\.:]+\)", "\\1", string)
    _s = re.sub(r"(\s+)__?(.*)__?(\s+)?", "\\1\\2\\3", _s)
    return _s


def resume():
    """Read resume YAML"""
    with open(resume_yaml, 'r') as file:
        resume_content = yaml.safe_load(file)

        for job in resume_content['experience']:
            if 'details' in job:
                job['details_html'] = []
                job['details_plain'] = []
                for detail in job['details']:
                    job['details_html'].append(markdown.markdown(detail))
                    job['details_plain'].append(md_strip(detail))

    return resume_content


def css():
    """Read CSS template"""
    with open(css_file, 'r') as _file:
        css_content = _file.read()
    _file.close()
    return css_content


def build_template(**kwargs):
    """Compile Jinja2 template and return it as a string"""
    _autoescape = kwargs['autoescape'] if 'autoescape' in kwargs else False
    with open(kwargs['source'], 'r') as _template_file:
        _template = _template_file.read()
    _template_file.close()

    _tm = Template(_template, autoescape=_autoescape)
    return _tm.render(resume=resume(), css=css(), year=year)


def write_out(**kwargs):
    """Write a file"""
    with open(kwargs['target'], 'w') as _file:
        _file.write(kwargs['content'])
    _file.close()
    print(f"-> Wrote {kwargs['target']}")


def gen_html():
    """Generate HTML"""
    html = build_template(source=html_template)
    write_out(target=html_out, content=html)


def gen_markdown():
    """Generate Markdown"""
    md = build_template(source=md_template, autoescape=True)
    write_out(target=md_out, content=md)


def gen_gemini():
    """Generate Gemini"""
    gmi = build_template(source=gmi_template)
    write_out(target=gmi_out, content=gmi)


def gen_txt():
    """Generate plain text"""
    txt = build_template(source=txt_template)
    write_out(target=txt_out, content=txt)

    narrow_txt = build_template(source=narrow_txt_template)
    write_out(target=narrow_txt_out, content=narrow_txt)


def run():
    """Build everything by default"""
    gen_html()
    gen_markdown()
    gen_gemini()
    gen_txt()


run()
