# Resume Makefile
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
DATE := $(shell date "+%B %Y")

DOCKER_RUN = docker run --rm -v ${PWD}:/work -w /work --user=$(CURRENT_UID):$(CURRENT_GID)

.DEFAULT_GOAL := help

.PHONY: all clean html md markdown txt test text gmi gemini pdf docx json man help check-deps serve
all: check-deps html md gmi txt pdf docx json man ## Generate all formats

help: ## Show help
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

check-deps: ## Check if required dependencies are installed
	@echo "Checking dependencies..."
	@command -v gomplate >/dev/null 2>&1 || { echo "❌ gomplate is not installed. Get it from: https://docs.gomplate.ca/installing/"; exit 1; }
	@command -v jq >/dev/null 2>&1 || { echo "❌ jq is not installed. Install with: brew install jq"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "❌ docker is not installed. Get it from: https://docs.docker.com/get-docker/"; exit 1; }
	@command -v python3 >/dev/null 2>&1 || { echo "❌ python3 is not installed. Install with: brew install python3"; exit 1; }
	@echo "✅ All dependencies are installed"

html: check-deps ## Generate HTML using gomplate
	@echo "Creating HTML"
	@mkdir -p public
	gomplate -c .=resume.yaml -f templates/resume.html.tmpl -o public/index.html

md markdown: check-deps ## Generate Markdown using gomplate
	@echo "Creating Markdown"
	gomplate -c .=resume.yaml -f templates/resume.md.tmpl -o README.md

txt text: check-deps ## Generate text formats using gomplate
	@echo "Creating text formats"
	@mkdir -p public
	gomplate -c .=resume.yaml -f templates/resume.txt.tmpl -o public/resume.txt
	gomplate -c .=resume.yaml -f templates/resume-narrow.txt.tmpl -o public/resume-narrow.txt

gmi gemini: check-deps ## Generate Gemini format using gomplate
	@echo "Creating Gemini format"
	@mkdir -p public
	gomplate -c .=resume.yaml -f templates/resume.gmi.tmpl -o public/resume.gmi

json: check-deps ## Generate pretty-formatted JSON using gomplate and jq
	@echo "Creating JSON"
	@mkdir -p public
	gomplate -c .=resume.yaml -i '{{ . | toJSON }}' | jq '.' > public/resume.json

pdf: check-deps ## Generate PDF
	@echo "Creating PDF"
	$(DOCKER_RUN) \
		--entrypoint=/usr/bin/google-chrome \
		browserless/chrome:latest \
		--headless \
		--disable-gpu \
		--no-sandbox \
		--print-to-pdf=public/Josh-Beard-Resume.pdf \
		--no-pdf-header-footer \
		public/index.html

docx word: check-deps ## Generate DOCX
	@echo "Creating docx"
	gomplate -c .=resume.yaml -f templates/resume-docx.md.tmpl -o public/Josh-Beard-Resume.md
	$(DOCKER_RUN) \
		--platform linux/amd64 \
		pandoc/latex --from markdown --to docx public/Josh-Beard-Resume.md \
		-f gfm \
		-V linkcolor:blue \
		-V geometry:a4paper \
		-V geometry:margin=2cm \
		-o public/Josh-Beard-Resume.docx
	rm -f public/Josh-Beard-Resume.md

man: check-deps ## Generate man page
	@echo "Creating man page"
	@mkdir -p public
	echo -e "% JoshBeard(7) joshbeard.com\n% Josh Beard (josh@joshbeard.com)\n% $(DATE)\n" | cat - README.md >| README.man.tmp
	$(DOCKER_RUN) \
		--platform linux/amd64 \
		pandoc/latex -s --from markdown --to man README.man.tmp \
		-o public/joshbeard-resume.7
	rm -f README.man.tmp

serve: html ## Serve the resume with auto-rebuild on changes
	@command -v fswatch >/dev/null 2>&1 || { echo "❌ fswatch is not installed. Install with: brew install fswatch"; exit 1; }
	@mkdir -p _serve && ln -sf ../public _serve/resume 2>/dev/null || true
	@echo "Starting server at http://localhost:8080/resume/"
	@echo "Watching resume.yaml and templates/ for changes... Press Ctrl+C to stop"
	@fswatch -o resume.yaml templates/ | xargs -n1 -I{} sh -c 'echo "Change detected, rebuilding..."; make html' & \
	  cd _serve && python3 -m http.server 8080

test: ## Run tests
	pre-commit run --all-files

clean: ## Clean up
	rm -f public/resume-narrow.txt public/resume.gmi public/resume.txt public/resume.json \
		public/Josh-Beard-Resume.docx public/Josh-Beard-Resume.pdf public/index.html public/joshbeard-resume.7
	rm -rf _serve
	git restore --staged README.md
	git restore README.md
