#!/usr/bin/env sh

html_md() {
  python build.py
}

docx() {
  echo "-> Creating DOCX"
    -it pandoc/latex --from markdown --to docx README.md \
    -f gfm \
    -V linkcolor:blue \
    -V geometry:a4paper \
    -V geometry:margin=2cm \
    -o dist/resume.docx
}

pdf() {
  echo "-> Creating PDF"
  docker run --rm -v ${PWD}:/work -w /work \
    --entrypoint=/usr/bin/google-chrome \
    -it browserless/chrome:latest \
    -headless -disable-gpu --no-sandbox \
    --print-to-pdf=dist/resume.pdf dist/index.html
}

if [ -z "$1" ]; then
  html_md
  docx
  pdf
elif [ "$1" == "html" ]; then
  html_md
elif [ "$1" == "md" ]; then
  md
elif [ "$1" == "pdf" ]; then
  pdf
elif [ "$1" == "docx" ]; then
  docx
fi