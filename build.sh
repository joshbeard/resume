#!/usr/bin/env sh

function html() {
  echo "-> Creating HTML"
  docker run --rm -v ${PWD}:/work -w /work \
    -it pandoc/latex --from markdown --to html README.md \
    -o dist/index.html \
    -H src/_includes/header.html \
    -B src/_includes/body.html \
    -A src/_includes/footer.html \
    -c assets/css/style.css \
    -c assets/fonts/fa/css/brands.min.css \
    -c assets/fonts/fa/css/fontawesome.min.css \
    -c assets/fonts/fa/css/regular.min.css \
    -c assets/fonts/fa/css/solid.min.css \
    --metadata title="Josh Beard"
}

function docx() {
  echo "-> Creating DOCX"
  docker run --rm -v ${PWD}:/work -w /work \
    -it pandoc/latex --from markdown --to docx README.md \
    -f gfm \
    -V linkcolor:blue \
    -V geometry:a4paper \
    -V geometry:margin=2cm \
    -o dist/resume.docx
}

function pdf() {
  echo "-> Creating PDF"
  docker run --rm -v ${PWD}:/work -w /work \
    --entrypoint=/usr/bin/google-chrome \
    -it browserless/chrome:latest \
    -headless -disable-gpu --no-sandbox \
    --print-to-pdf=dist/resume.pdf dist/index.html
}

if [ -z "$1" ]; then
  html
  docx
  pdf
elif [ "$1" == "html" ]; then
  html
elif [ "$1" == "pdf" ]; then
  pdf
elif [ "$1" == "docx" ]; then
  docx
fi