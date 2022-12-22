all: clean build

build:
	cd src ; \
	zip ../Homebrew-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc* --exclude=*.pyo*

clean:
	rm -f *.alfredworkflow

update-lib:
	/usr/bin/env python3 -m pip install --target src --upgrade Alfred-PyWorkflow
	rm -rf src/Alfred_PyWorkflow-*-info/
