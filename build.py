#!/usr/bin/env python
from jinja2 import Template
#from weasyprint import HTML, CSS
import yaml
import markdown
import datetime

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
# -----------------------------------------------------------------------------

# Current date
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

def run():
  gen_html()
  gen_markdown()
  gen_gemini()

def resume():
    global resume_yaml
    ## Read resume YAML
    with open(resume_yaml, 'r') as file:
        resume_content = yaml.safe_load(file)

    parsed_jobs = []
    for job in resume_content['experience']:
        job['details_html'] = []
        for detail in job['details']:
            job['details_html'].append(markdown.markdown(detail))
        parsed_jobs.append(job)
    resume_content['experience'] = parsed_jobs

    return resume_content

def css():
    global css_file
    _file = open(css_file, 'r')
    css_content = _file.read()
    _file.close()
    return css_content

## HTML Template
def gen_html():
    global html_template
    global html_out, year

    html_template_file = open(html_template)
    html_template = html_template_file.read()
    html_template_file.close()

    html_tm = Template(html_template, autoescape=True)
    html = html_tm.render(resume=resume(), css=css(), year=year)

    with open(html_out, 'w') as html_file:
        html_file.write(html)
    html_file.close()
    print(f"-> Wrote {html_out}")

## Markdown Template
def gen_markdown():
    global md_template
    global md_out
    md_template_file = open(md_template)
    md_template = md_template_file.read()
    md_template_file.close()

    md_tm = Template(md_template, autoescape=True)
    md = md_tm.render(resume=resume(), year=year)

    with open(md_out, 'w') as md_file:
        md_file.write(md)
    md_file.close()
    print(f"-> Wrote {md_out}")

## Gemini Template
def gen_gemini():
    global gmi_template
    global gmi_out
    gmi_template_file = open(gmi_template)
    gmi_template = gmi_template_file.read()
    gmi_template_file.close()

    gmi_tm = Template(gmi_template, autoescape=True)
    md = gmi_tm.render(resume=resume(), year=year)

    with open(gmi_out, 'w') as gmi_file:
        gmi_file.write(md)
    gmi_file.close()
    print(f"-> Wrote {gmi_out}")

## Word

run()