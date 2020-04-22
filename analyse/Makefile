build: Dockerfile
	cp ../gcp_auth.json .
	docker build -t newsfuzz:analyse .

dev: build
	docker run --rm --name newsfuzz_analyse --network host -itv ${PWD}:/usr/src/app newsfuzz:analyse bash

run: build
	docker run --rm --network host -e "PORT=8080" newsfuzz:analyse

cloud-build:
	gcloud builds submit . --tag gcr.io/newsfuzz/analyse

register: build
	docker tag newsfuzz:analyse gcr.io/newsfuzz/analyse
	docker push gcr.io/newsfuzz/analyse

deploy:
	gcloud run deploy analyse --image gcr.io/newsfuzz/analyse --platform managed --region europe-west1

teardown:
	docker stop newsfuzz_analyse
	docker system prune
