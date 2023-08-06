REQUIREMENTS_TXT ?= requirements.txt requirements-dev.txt

include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2020.08.14/Makefile.venv"
	echo "5afbcf51a82f629cd65ff23185acde90ebe4dec889ef80bbdc12562fbd0b2611 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv

help:
    @IFS=$$'\n' ; \
    help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`); \
    for help_line in $${help_lines[@]}; do \
        IFS=$$'#' ; \
        help_split=($$help_line) ; \
        help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
        help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
        printf "%-30s %s\n" $$help_command $$help_info ; \
    done

all: pip dev

.PHONY: dev
dev: venv

clean: clean-venv
	rm -rf dist/*

.PHONY: test
test: dev
	tox -p all

build: test
	$(VENV)/python3 setup.py sdist bdist_wheel
	$(VENV)/twine check dist/*

upload: build
	$(VENV)/twine upload dist/*

check: dev # Code format check with isort and black
	tox -efmt-check
	tox -epep8

fix: dev # fixes code formatting with isort and black
	tox -efmt
