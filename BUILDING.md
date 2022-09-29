# Building My Resume

[![Build](https://github.com/joshbeard/resume/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/joshbeard/resume/actions/workflows/build-deploy.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4045419784f447ce874f3cdc6d539617)](https://www.codacy.com/gh/joshbeard/resume/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joshbeard/resume&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/joshbeard/resume/badge)](https://www.codefactor.io/repository/github/joshbeard/resume)
[![DeepSource](https://deepsource.io/gh/joshbeard/resume.svg/?label=active+issues&show_trend=true&token=r6oAHM7Ii2Emi_95lfEkNtxX)](https://deepsource.io/gh/joshbeard/resume/?ref=repository-badge)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/joshbeard/resume)

## Published

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

## Overview

I'm maintaining the contents of my resume in the [`resume.yaml`](resume.yaml)
file. The [`resume.py`](resume.py) script builds several versions from Jinja2
templates:

| Document                | Template
| ----------------------- | -----------------------------------------
| HTML                    | [`templates/resume.html`](templates/resume.html)
| Markdown                | [`templates/resume.md`](templates/resume.md)
| Gemini                  | [`templates/resume.gmi`](templates/resume.gmi)
| Plain Text              | [`templates/resume.txt`](templates/resume.txt)
| Plain Text Narrow Width | [`templates/resume-narrow.txt`](templates/resume-narrow.txt)

It also produces a JSON file directly from the YAMl source (not a template).

The [`dist/`](dist) directory contains assets that are deployed to my resume
site as-is - currently, that's just a few images. The `dist` directory acts as a
staging directory - the generated `index.html` would exist at the root of this.

I deploy to S3 and my local Gemini and Gopher servers.

## Files

```plain
├── .github/                GitHub Workflows
├── BUILDING.md             This document that describes how it's built and deployed
├── README.md               A Markdown document generated and merged via CI (GitHub action) or via the `resume.py` script
├── dist/                   Directory containing things to deploy
│   └── assets/             Static assets for the website
│       └── img/
├── Makefile                Makefile for building and local tasks
├── requirements.txt        Python dependencies
├── resume.py               Python script for building HTML and Markdown
├── resume.yaml             My resume data
└── templates/              Source template files
```

### Other Files

Some other files for various integrations are also maintained in this repository:

* `.codacy.yml`: configuration for Codacy (via GitHub)
* `.deepsource.toml`: configuration for DeepSource integration (via GitHub)
* `.remarkrc.js`: configuration for the Remark Markdown validator (via Codacy, CodeFactor)
* `.stylelintrc.json`: configuration for linters (used via GitHub - Codacy, CodeFactor)
* `renovate.json`: configuration for RenovateBot (via GitHub)

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

The [GitHub Workflow](.github/workflows/build-deploy.yml) does several things:

* Spell check (the contents of the most recent commit)
* Builds HTML and Markdown using [`resume.py`](resume.py)
* Generates Word document using [Pandoc](https://pandoc.org/)
* Generates PDF document using [GitHub action for headless Chrome](https://github.com/marketplace/actions/setup-chrome)

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

Just for fun. I've maintained it in different ways over the years, more recently in simple HTML. However, I'd like to be able to
provide it in Markdown, too, and also other formats as desired. YAML seems like the best choice for a human-friendly and
machine-parsable format to maintain the source in to produce multiple formats. While this may not be the most intuitive for many people,
it's all comfortable to me.

