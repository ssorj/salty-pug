IMAGE := quay.io/skupper/salty-pug-console

.PHONY: build
build: common
	docker build -t ${IMAGE} .

# .PHONY: run
# run: build
# 	docker run --rm -p 8080:8080 ${IMAGE}

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
