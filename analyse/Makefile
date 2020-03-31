build: Dockerfile
	docker build -t newsfuzz:analyse .

dev: build
	docker run --rm --name newsfuzz_analyse -itv ${PWD}:/usr/src/app newsfuzz:analyse

teardown:
	docker stop newsfuzz_analyse
	docker system prune
