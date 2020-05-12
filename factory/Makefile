IMAGE := quay.io/skupper/salty-pug-factory

.PHONY: build
build: model.py
	podman build -t ${IMAGE} .

.PHONY: run
run: build
	podman run -p 8080:8080 ${IMAGE}

# Prerequisite: podman login quay.io
.PHONY: push
push: build
	podman push -q ${IMAGE}

model.py: ../common/model.py
	cp $< $@
