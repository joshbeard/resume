#!/usr/bin/env sh
echo "-> Creating HTML"
docker run --rm -v ${PWD}:/work -w /work \
  -it pandoc/latex --from markdown --to html README.md \
  -o web/dist/index.html \
  -H web/src/_includes/header.html \
  -B web/src/_includes/body.html \
  -A web/src/_includes/footer.html \
  -c assets/css/style.css \
  --metadata title="Josh Beard"

echo "-> Creating DOCX"
docker run --rm -v ${PWD}:/work -w /work \
  -it pandoc/latex --from markdown --to docx README.md \
  -f gfm \
  -V linkcolor:blue \
  -V geometry:a4paper \
  -V geometry:margin=2cm \
  -o resume.docx

echo "-> Creating PDF"
docker run --rm -v ${PWD}:/work -w /work \
  --entrypoint=/usr/bin/google-chrome \
  -it browserless/chrome:latest \
  -headless -disable-gpu --no-sandbox \
  --print-to-pdf=resume.pdf web/dist/index.html
