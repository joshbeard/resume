# Building My Resume

Motivation: My goal is to have my resume in a very simple to maintain format with a simple
means of publishing it as a website. I'd also like to automate generating a PDF.
A Markdown document would be nice.

The source of my resume is the [README.md](README.md) Markdown file.

It's published here:

* Markdown: <https://github.com/joshbeard/resume/blob/master/README.md>
* Web: <https://joshbeard.me/resume/>
* PDF: <https://joshbeard.me/resume/Josh-Beard-Resume.pdf>
* Word: <https://joshbeard.me/resume/Josh-Beard-Resume.docx>

## Files

```plain
├── .github/                GitHub Workflows
├── BUILDING.md             This document
├── README.md               The resume (with minimal HTML in it)
├── build.sh*               Shell script for building locally
├── dist/                   Directory containing things to deploy
│   └── assets/             Static assets for the website
│       ├── css/
│       ├── fonts/
│       └── img/
├── docker-compose.yml      docker-compose file for local development
└── src/                    Source files used during building (html snips)
    └── _includes/          HTML sections that are used to produce the website by Pandoc
        ├── body.html
        ├── footer.html
        └── header.html
```

## Build and Deployment

The [GitHub Workflow](.github/workflows/build-deploy.yml) uses [Pandoc](https://pandoc.org/)
to create the HTML page from the source Markdown. Pandoc is also used to
generate the Microsoft Word document from the Markdown source.

A [GitHub action for headless Chrome](https://github.com/marketplace/actions/setup-chrome)
is used to generate the PDF from the HTML. I experimented with Pandoc a
little, but the Chrome "print to PDF" works pleny well out of the box.

My resume is published to the S3 website bucket for
[joshbeard.me](https://github.com/joshbeard/joshbeard.me-tf-aws).

The [`build.sh`](build.sh) script is for local use and uses Docker to run
Pandoc and Chrome.

The [`docker-compose.yml`](docker-compose.yml) is also useful for local
development for previewing the site with an actual HTTP server rather
than as a local file.
