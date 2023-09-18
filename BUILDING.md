# Building My Resume

The [`dist/`](dist) directory contains assets that are deployed for the website
as-is. The `dist` directory acts as a staging directory - the generated
`index.html` would exist at the root of this.

I deploy to S3 and my local Gemini and Gopher servers.

## Copy this for your own resume

You might consider [JSON Resume](https://jsonresume.org/) instead.

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

