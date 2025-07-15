# Development Notes

The [`dist/`](dist) directory contains assets that are deployed for the website
as-is. The `dist` directory acts as a staging directory - the generated
`index.html` would exist at the root of this.

I deploy to S3 and my local Gemini and Gopher servers.

## Copy this for your own resume

You might consider [JSON Resume](https://jsonresume.org/) instead.

I didn't develop this for general use in mind, but feel free to take what you
want from it. You'll want to modify basically all of the files to fit your needs,
but it's fairly generic.

## Build and Deployment

Use the [`Makefile`](Makefile) to build the resume.

To view all `make` targets:

```shell
make
```

To build HTML only:

```shell
make html
```

To serve locally:

```shell
make serve
```

It will be available at <http://localhost:8080/resume/>.

The [GitHub Workflow](.github/workflows/build-deploy.yml) builds and deploys
my resume to S3.

## Template System

The resume uses [gomplate](https://docs.gomplate.ca/) for template processing:

- **Data source**: [`resume.yaml`](resume.yaml) - Contains all resume data
- **Templates**: [`templates/`](templates/) directory with `.tmpl` extensions
- **Output formats**: HTML, Markdown, text, JSON, Gemini, and more

## Required Tools

- [gomplate](https://docs.gomplate.ca/) - Template processing
- [jq](https://stedolan.github.io/jq/) - JSON formatting
- [Docker](https://www.docker.com/) - For PDF/DOCX generation
- [Pandoc](https://pandoc.org/) - For generating Word documents (ran in Docker)

## Resources

### Tools

* GitHub Workflows for build and deployment.
* [gomplate](https://docs.gomplate.ca/) for template processing.
* [jq](https://stedolan.github.io/jq/) for JSON formatting.
* [Pandoc](https://pandoc.org/) for generating Word documents.
* [headless Chrome](https://github.com/marketplace/actions/setup-chrome) for generating the PDF document.
* [minify-action](https://github.com/anthonyftwang/minify-action) for minifying static documents.
* AWS S3 and CloudFront for hosting.

## Why

I've maintained my resume in different ways over the years, more recently in
simple HTML. I don't like using word processors and their nightmare document formats.
I want a website version, but I also wanted a PDF and Markdown copy. For fun,
I generate it in several formats, including some more esoteric ones like
a [man page](), `finger resume@jbeard.co`, and [Gemini](gemini://jbeard.co/resume.gmi)