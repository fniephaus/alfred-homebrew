all: clean build

build:
	cd src ; \
	zip ../Homebrew-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc* --exclude=*.pyo*

clean:
	rm -f *.alfredworkflow

update-lib:
	pip install -d ./ Alfred-Workflow
	tar xzvf Alfred-Workflow-*.tar.gz
	cp -r Alfred-Workflow-*/workflow src/
	rm -rf Alfred-Workflow-*