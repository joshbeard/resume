# Resume Makefile
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
DATE := $(shell date "+%B %Y")

DOCKER_RUN = docker run --rm -v ${PWD}:/work -w /work --user=$(CURRENT_UID):$(CURRENT_GID)

.DEFAULT_GOAL := help

.PHONY: all clean html md markdown txt test text gmi gemini pdf docx json man help check-deps
all: check-deps html md gmi txt pdf docx json man ## Generate all formats

help: ## Show help
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

check-deps: ## Check if required dependencies are installed
	@echo "Checking dependencies..."
	@command -v gomplate >/dev/null 2>&1 || { echo "❌ gomplate is not installed. Get it from: https://docs.gomplate.ca/installing/"; exit 1; }
	@command -v jq >/dev/null 2>&1 || { echo "❌ jq is not installed. Install with: brew install jq"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "❌ docker is not installed. Get it from: https://docs.docker.com/get-docker/"; exit 1; }
	@echo "✅ All dependencies are installed"

html: check-deps ## Generate HTML using gomplate
	@echo "Creating HTML"
	@mkdir -p dist
	gomplate -c .=resume.yaml -f templates/resume.html.tmpl -o dist/index.html

md markdown: check-deps ## Generate Markdown using gomplate
	@echo "Creating Markdown"
	gomplate -c .=resume.yaml -f templates/resume.md.tmpl -o README.md

txt text: check-deps ## Generate text formats using gomplate
	@echo "Creating text formats"
	@mkdir -p dist
	gomplate -c .=resume.yaml -f templates/resume.txt.tmpl -o dist/resume.txt
	gomplate -c .=resume.yaml -f templates/resume-narrow.txt.tmpl -o dist/resume-narrow.txt

gmi gemini: check-deps ## Generate Gemini format using gomplate
	@echo "Creating Gemini format"
	@mkdir -p dist
	gomplate -c .=resume.yaml -f templates/resume.gmi.tmpl -o dist/resume.gmi

json: check-deps ## Generate pretty-formatted JSON using gomplate and jq
	@echo "Creating JSON"
	@mkdir -p dist
	gomplate -c .=resume.yaml -i '{{ . | toJSON }}' | jq '.' > dist/resume.json

pdf: check-deps ## Generate PDF
	@echo "Creating PDF"
	$(DOCKER_RUN) \
		--entrypoint=/usr/bin/google-chrome \
		browserless/chrome:latest \
		--headless \
		--disable-gpu \
		--no-sandbox \
		--print-to-pdf=dist/resume.pdf \
		--no-pdf-header-footer \
		dist/index.html

docx word: check-deps ## Generate DOCX
	@echo "Creating docx"
	$(DOCKER_RUN) \
		--platform linux/amd64 \
		pandoc/latex --from markdown --to docx README.md \
		-f gfm \
		-V linkcolor:blue \
		-V geometry:a4paper \
		-V geometry:margin=2cm \
		-o dist/resume.docx

man: check-deps ## Generate man page
	@echo "Creating man page"
	@mkdir -p dist
	echo -e "% JoshBeard(7) joshbeard.me\n% Josh Beard (josh@joshbeard.me)\n% $(DATE)\n" | cat - README.md >| README.man.tmp
	$(DOCKER_RUN) \
		--platform linux/amd64 \
		pandoc/latex -s --from markdown --to man README.man.tmp \
		-o dist/joshbeard-resume.7
	rm -f README.man.tmp

serve: ## Serve the resume
	docker run --rm -v ${PWD}/dist:/usr/share/nginx/html/resume -w /work -p 8080:80 nginx

test: ## Run tests
	pre-commit run --all-files

clean: ## Clean up
	rm -f dist/resume-narrow.txt dist/resume.gmi dist/resume.txt dist/resume.json \
		dist/resume.docx dist/resume.pdf dist/index.html dist/joshbeard-resume.7
	git restore --staged README.md
	git restore README.md
