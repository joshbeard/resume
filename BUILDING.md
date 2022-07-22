# Building My Resume

Motivation: My goal is to have my resume in a very simple to maintain format
(plain text) with a simple means of publishing it as a website. I'd also like to
automate generating a PDF.  A Markdown document would be nice. I want a single
source to maintain without a bunch of coding, scripting, etc for piecing it
together or generating different formats. I don't know LaTeX and don't prefer to
use it here. I mainly want Markdown/text, HTML, and PDF. Word is a bonus.

The source of my resume is the [README.md](README.md) Markdown file.

It's published here:

* Markdown: <https://github.com/joshbeard/resume/blob/master/README.md>
* Web: <https://joshbeard.me/resume/>
* PDF: <https://joshbeard.me/resume/Josh-Beard-Resume.pdf>
* Word: <https://joshbeard.me/resume/Josh-Beard-Resume.docx>

## Files

```plain
├── .github/                GitHub Workflows
├── BUILDING.md             This document that describes how it's built and deployed
├── README.md               My resume itself (with minimal HTML in it)
├── build.sh*               Shell script for building locally
├── dist/                   Directory containing things to deploy
│   └── assets/             Static assets for the website
│       ├── css/
│       ├── fonts/
│       └── img/
├── docker-compose.yml      docker-compose file for local development (Nginx)
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
little, but the Chrome "print to PDF" works well out of the box.

My resume is published to the S3 website bucket for
[joshbeard.me](https://github.com/joshbeard/joshbeard.me-tf-aws).

The [`build.sh`](build.sh) script is for local use and uses Docker to run
Pandoc and Chrome.

The [`docker-compose.yml`](docker-compose.yml) is also useful for local
development for previewing the site with an actual HTTP server rather
than as a local file, which is helpful for testing relative URLs and the like
similar to 'production'.

```shell
docker-compose up
```

Visit the local instance via <http://localhost:8080/resume/>

## Resources

### Web Fonts

* [Ubuntu fonts](https://design.ubuntu.com/font/)
* [Play font](https://fonts.google.com/specimen/Play)
* [Font Awesome free](https://fontawesome.com/)

### Tools

* GitHub Workflows for build and deployment.
* [Pandoc](https://pandoc.org/) for generating HTML and Word documents.
* [GitHub action for headless Chrome](https://github.com/marketplace/actions/setup-chrome) for generating the PDF document.
* [minify-action](https://github.com/anthonyftwang/minify-action) for minifying static documents.
* AWS S3 and CloudFront for hosting.

## TODO

* Reduce/remove the HTML in the [README.md](README.md) file. Ideally, the
  Markdown document will be just Markdown (GFM) without any HTML.
* Relative paths have caused issues and two pipeline jobs are used to handle
  this by generating a 'local' HTML page and a 'served' page with the relative
  root varying (/ vs /resume/). This could/should be resolved without this.
