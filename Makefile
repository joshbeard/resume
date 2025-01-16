# Resume Makefile
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
DATE := $(shell date "+%B %Y")

DOCKER_RUN = docker run --rm -v ${PWD}:/work -w /work -it --user=$(CURRENT_UID):$(CURRENT_GID)
BUILD_PY = python resume.py

.PHONY: all clean html md markdown txt test text gmi gemini pdf docx json man
all: html md gmi txt pdf docx json man

html md markdown txt text gmi gemini json:
	$(BUILD_PY) $@

pdf:
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

docx word:
	@echo "Creating docx"
	$(DOCKER_RUN) \
		pandoc/latex --from markdown --to docx README.md \
		-f gfm \
		-V linkcolor:blue \
		-V geometry:a4paper \
		-V geometry:margin=2cm \
		-o dist/resume.docx

man:
	@echo "Creating man page"
	echo -e "% JoshBeard(7) joshbeard.me\n% Josh Beard (josh@joshbeard.me)\n% $(DATE)\n" | cat - README.md >| README.man.tmp
	$(DOCKER_RUN) \
		pandoc/latex -s --from markdown --to man README.man.tmp \
		-o dist/joshbeard-resume.7
	rm -f README.man.tmp

serve:
	docker run --rm -v ${PWD}/dist:/usr/share/nginx/html/resume -w /work -p 8080:80 nginx

test:
	$(DOCKER_RUN) pipelinecomponents/yamllint yamllint resume.yaml

clean:
	rm -f resume-narrow.txt resume.gmi resume.txt resume.json \
		dist/resume.docx dist/resume.pdf dist/index.html dist/joshbeard-resume.7
	git restore --staged README.md
	git restore README.md
