IMAGE := quay.io/skupper/salty-pug-store

.PHONY: build
build: common.py model.py
	docker build -t ${IMAGE} .

.PHONY: run
run: build
	docker run --rm -p 8080:8080 ${IMAGE}

# Prerequisite: docker login quay.io
.PHONY: push
push: build
	docker push -q ${IMAGE}

.PHONY: clean
clean:
	rm model.py
	rm common.py
	rm -rf __pycache__/

../common/%.py: ;

%.py: ../common/%.py
	cp $< $@
