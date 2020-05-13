IMAGE := quay.io/skupper/salty-pug-store

.PHONY: build
build: common
	docker build -t ${IMAGE} .

# Prerequisite: docker login quay.io
.PHONY: push
push: build
	docker push -q ${IMAGE}

.PHONY: clean
clean:
	rm -rf common
	rm -rf __pycache__

common: ../common ../common/*
	cp -a $< $@
