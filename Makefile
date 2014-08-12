all: clean build

build:
	cd src ; \
	zip ../Homebrew-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm -f *.alfredworkflow