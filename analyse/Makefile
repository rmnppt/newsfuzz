build: Dockerfile
	cp ../gcp_auth.json .
	docker build -t newsfuzz:analyse .

dev: build
	docker run --rm --name newsfuzz_analyse -itv ${PWD}:/usr/src/app newsfuzz:analyse bash

run: build
	docker run --rm newsfuzz:analyse

teardown:
	docker stop newsfuzz_analyse
	docker system prune
