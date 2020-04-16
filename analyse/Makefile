build: Dockerfile
	cp ../gcp_auth.json .
	docker build -t newsfuzz:analyse .

dev: build
	docker run --rm --name newsfuzz_analyse -itv ${PWD}:/usr/src/app newsfuzz:analyse bash

run: build
	docker run --rm -e "PORT=8080" newsfuzz:analyse

register: build
	docker tag newsfuzz:analyse gcr.io/newsfuzz/analyse
	docker push gcr.io/newsfuzz/analyse

deploy: register
	gcloud run deploy --image gcr.io/newsfuzz/analyse --platform managed

teardown:
	docker stop newsfuzz_analyse
	docker system prune
