.phony: test
test:
	python3 scripts/test-minikube

.phony: demo
demo:
	SKUPPER_DEMO=1 python3 scripts/test-minikube

.phony: build-images
build:
	cd store && make build
	cd factory && make build
	cd console && make build

# Prerequisite: podman login quay.io
.PHONY: push-images
push: build
	cd store && make push
	cd factory && make push
	cd console && make push

.phony: clean
clean:
	rm -rf scripts/__pycache__
	rm -f README.html

README.html: README.md
	pandoc -o $@ $<
