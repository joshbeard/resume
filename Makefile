# Makefile for deploying my resume website
# This deploys to my joshbeard.me s3 bucket.
clean:
	test -d _site && rm -rf _site || exit 0

minify:
	mkdir _site
	docker run --rm -it \
      -v ${PWD}:/site \
      thekevjames/minify:2.5.2 \
      minify --recursive --output /site/_site /site

s3-deploy:
	docker run --env-file=../aws.env -v ${PWD}:/site -w /site mikesir87/aws-cli \
	  aws s3 sync _site s3://s3-website-joshbeard-me/resume/ \
	  --exclude ".git*" \
	  --exclude "Makefile" \
	  --exclude "README.md" \
	  --delete

deploy: clean minify s3-deploy
