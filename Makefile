.phony: run
run:
	scripts/run

.phony: build
build:
	cd store && make build
	cd factory && make build
	cd console && make build

# Prerequisite: podman login quay.io
.PHONY: push
push: build
	cd store && make push
	cd factory && make push
	cd console && make push

.phony: clean
clean:
	rm -rf scripts/__pycache__
	rm -f README.html

.phony: deploy
deploy:
	scripts/deploy

README.html: README.md
	pandoc -o $@ $<

.phony: update-%
update-%:
	curl -sfo scripts/$*.py "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py"
