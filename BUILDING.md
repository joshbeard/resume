# Building My Resume

[![Build](https://github.com/joshbeard/resume/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/joshbeard/resume/actions/workflows/build-deploy.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4045419784f447ce874f3cdc6d539617)](https://www.codacy.com/gh/joshbeard/resume/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joshbeard/resume&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/joshbeard/resume/badge)](https://www.codefactor.io/repository/github/joshbeard/resume)
[![DeepSource](https://deepsource.io/gh/joshbeard/resume.svg/?label=active+issues&show_trend=true&token=r6oAHM7Ii2Emi_95lfEkNtxX)](https://deepsource.io/gh/joshbeard/resume/?ref=repository-badge)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/joshbeard/resume)

## Overview

I'm maintaining the contents of my resume in the [`resume.yaml`](resume.yaml)
file. The [`resume.py`](resume.py) script builds several versions from Jinja2
templates:

| Format                  | Template
| ----------------------- | -----------------------------------------
| HTML                    | [`templates/resume.html`](templates/resume.html)
| Markdown                | [`templates/resume.md`](templates/resume.md)
| Gemini                  | [`templates/resume.gmi`](templates/resume.gmi)
| Plain Text              | [`templates/resume.txt`](templates/resume.txt)
| Plain Text Narrow Width | [`templates/resume-narrow.txt`](templates/resume-narrow.txt)
| JSON                    | Converted from YAML source

The [`dist/`](dist) directory contains assets that are deployed for the website
as-is. The `dist` directory acts as a staging directory - the generated
`index.html` would exist at the root of this.

I deploy to S3 and my local Gemini and Gopher servers.

## Copy this for your own resume

I didn't develop this for general use in mind, but feel free to take what you
want from it. You'd probably want to modify the `resume.py` script, the
[`templates/`](templates/), and the [`resume.yaml`](resume.yaml), of course.

## Build and Deployment

Use the [`Makefile`](Makefile) to build the resume.

To build all formats:

```shell
make
```

To build HTML only:

```shell
make html
```

The [GitHub Workflow](.github/workflows/build-deploy.yml) builds and deploys
my resume.

My resume is published to the S3 website bucket for
[joshbeard.me](https://github.com/joshbeard/joshbeard.me-tf-aws).

It's also useful for local development to preview the site with
an actual HTTP server rather than as a local file, which is helpful for testing
relative URLs and the like similar to 'production'.

```shell
make serve
```

Visit the local instance via <http://localhost:8080/resume/>

## Resources

### Tools

* GitHub Workflows for build and deployment.
* [Pandoc](https://pandoc.org/) for generating Word documents.
* [GitHub action for headless Chrome](https://github.com/marketplace/actions/setup-chrome) for generating the PDF document.
* [minify-action](https://github.com/anthonyftwang/minify-action) for minifying static documents.
* AWS S3 and CloudFront for hosting.

## Why

I've maintained my resume in different ways over the years, more recently in
simple HTML. I hate using word processors and their nightmare document formats.
I want a website version, but I also wanted a PDF and Markdown copy. For fun,
I generate it in several formats, including some more esoteric ones like
a [man page](), `finger resume@jbeard.co`, and [Gemini](gemini://jbeard.co/resume.gmi)

## Published Formats

* Web/HTML: <https://joshbeard.me/resume>
* Markdown (GitHub): <https://github.com/joshbeard/resume/blob/master/README.md>
* PDF: <https://joshbeard.me/resume/Josh-Beard-Resume.pdf>
* Word: <https://joshbeard.me/resume/Josh-Beard-Resume.docx>
* Text: <https://joshbeard.me/resume/resume.txt>
* Narrow Text: <https://joshbeard.me/resume/resume-narrow.txt>
* JSON: <https://joshbeard.me/resume/resume.json>
* `gemini://jbeard.co/resume.gmi`
* `gopher://jbeard.co:70/0/resume.txt`
* `finger resume@jbeard.co`

