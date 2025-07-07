# Resume Makefile
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
DATE := $(shell date "+%B %Y")

DOCKER_RUN = docker run --rm -v ${PWD}:/work -w /work -it --user=$(CURRENT_UID):$(CURRENT_GID)
VENV = .venv
BUILD_PY = $(VENV)/bin/python resume.py

.DEFAULT_GOAL := help

.PHONY: all clean html md markdown txt test text gmi gemini pdf docx json man help venv
all: venv html md gmi txt pdf docx json man

help: ## Show help
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\032[0m %s\n", $$1, $$2}'

$(VENV)/bin/activate: requirements.txt ## Create virtual environment
	@echo "Creating virtual environment"
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

venv: $(VENV)/bin/activate ## Setup virtual environment

html md markdown txt text gmi gemini json: venv ## Generate HTML, Markdown, GMI, and other formats
	$(BUILD_PY) $@

pdf: ## Generate PDF
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

docx word: ## Generate DOCX
	@echo "Creating docx"
	$(DOCKER_RUN) \
		pandoc/latex --from markdown --to docx README.md \
		-f gfm \
		-V linkcolor:blue \
		-V geometry:a4paper \
		-V geometry:margin=2cm \
		-o dist/resume.docx

man: ## Generate man page
	@echo "Creating man page"
	echo -e "% JoshBeard(7) joshbeard.me\n% Josh Beard (josh@joshbeard.me)\n% $(DATE)\n" | cat - README.md >| README.man.tmp
	$(DOCKER_RUN) \
		pandoc/latex -s --from markdown --to man README.man.tmp \
		-o dist/joshbeard-resume.7
	rm -f README.man.tmp

serve: ## Serve the resume
	docker run --rm -v ${PWD}/dist:/usr/share/nginx/html/resume -w /work -p 8080:80 nginx

test: ## Run tests
	$(DOCKER_RUN) pipelinecomponents/yamllint yamllint resume.yaml

clean: ## Clean up
	rm -f resume-narrow.txt resume.gmi resume.txt resume.json \
		dist/resume.docx dist/resume.pdf dist/index.html dist/joshbeard-resume.7
	rm -rf $(VENV)
	git restore --staged README.md
	git restore README.md
