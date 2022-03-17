pandoc --from markdown --to html README.md \
  -o web/dist/index.html \
  -H web/src/_includes/header.html \
  -B web/src/_includes/body.html \
  -A web/src/_includes/footer.html \
  -c assets/css/style.css \
  --metadata title="Josh Beard"