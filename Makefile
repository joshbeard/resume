# Resume Makefile
DOCKER_RUN = docker run --rm -v ${PWD}:/work -w /work -it
BUILD_PY = python resume.py

.PHONY: all clean html md markdown txt text gmi gemini pdf docx
all: html md gmi txt pdf docx

html md markdown txt text gmi gemini:
	$(BUILD_PY) $@

pdf:
	@echo "Creating PDF"
	$(DOCKER_RUN) \
		--entrypoint=/usr/bin/google-chrome \
		browserless/chrome:latest -headless -disable-gpu \
		--no-sandbox --print-to-pdf=dist/resume.pdf dist/index.html

docx:
	@echo "Creating docx"
	$(DOCKER_RUN) \
		pandoc/latex --from markdown --to docx README.md \
		-f gfm \
		-V linkcolor:blue \
		-V geometry:a4paper \
		-V geometry:margin=2cm \
		-o dist/resume.docx

serve:
	docker run --rm -v ${PWD}/dist:/usr/share/nginx/html/resume -w /work -p 8080:80 nginx

test:
	$(DOCKER_RUN) pipelinecomponents/yamllint yamllint resume.yaml

clean:
	rm -f resume-45w.txt resume.gmi resume.txt \
		dist/resume.docx dist/resume.pdf dist/index.html
	git restore --staged README.md
	git restore README.md
