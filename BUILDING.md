# Building My Resume

I'm maintaining the contents of my resume in the [`resume.yaml`](resume.yaml)
file. The [`build.py`](build.py) script builds several versions from Jinja2
templates:

* HTML from [`src/resume.html`](src/resume.html)
* Markdown from [`src/resume.md`](src/resume.md)
* Gemini from [`src/resume.gmi`](src/resume.gmi)
* Plain Text from [`src/resume.txt`](src/resume.txt)
* Plain Text Narrow Width from [`src/resume-45w.txt](src/resume-45w.txt)

The [`dist/`](dist) directory contains assets that are deployed to my resume
site as-is - currently, that's just a few images. The `dist` directory acts as a
staging directory - the generated `index.html` would exist at the root of this.

I deploy to S3 and my local Gemini and Gopher servers.

## Files

```plain
├── .github/                GitHub Workflows
├── BUILDING.md             This document that describes how it's built and deployed
├── README.md               A Markdown document generated and merged via CI (GitHub action) or via the build.py script
├── build.py                Python script for building HTML and Markdown
├── build.sh                Shell script for building locally
├── dist/                   Directory containing things to deploy
│   └── assets/             Static assets for the website
│       └── img/
├── docker-compose.yml      docker-compose file for local development (Nginx)
├── requirements.txt        Python dependencies
├── resume.yaml             My resume data
└── src/                    Source template files
```

## Build and Deployment

The [GitHub Workflow](.github/workflows/build-deploy.yml) does several things:

* Spell check (the contents of the most recent commit)
* Builds HTML and Markdown using [`build.py`](build.py)
* Generates Word document using [Pandoc](https://pandoc.org/)
* Generates PDF document using [GitHub action for headless Chrome](https://github.com/marketplace/actions/setup-chrome)

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

### Tools

* GitHub Workflows for build and deployment.
* [Pandoc](https://pandoc.org/) for generating Word documents.
* [GitHub action for headless Chrome](https://github.com/marketplace/actions/setup-chrome) for generating the PDF document.
* [minify-action](https://github.com/anthonyftwang/minify-action) for minifying static documents.
* AWS S3 and CloudFront for hosting.
