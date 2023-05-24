include config.ini

NO_COLOR=\x1b[0m
OK_COLOR=\x1b[32;01m

.SILENT:
.PHONY: create_env
create_env:
ifeq ("$(wildcard ./env)", "")
	python3 -m venv env
endif

.PHONY: install
install:
	printf "Installing Packages... "
	pip install -q --upgrade 'pip>=22.2.2'
	pip install -q -r ./requirements.txt
	echo "DONE\n"

.SILENT:
.PHONY:
setup: create_env
	( \
		source ./env/bin/activate; \
		make install; \
		echo "$(OK_COLOR)Don't forget to activate venv before working on this project.\
		\nCommand: \`source ./env/bin/activate\`.$(NO_COLOR)\n"; \
	)

.PHONY: test
test:
	echo $(EC2_INSTANCE_IP)
