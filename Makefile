NO_COLOR=\x1b[0m
OK_COLOR=\x1b[32;01m

GITHUB_REPO="https://github.com/mattwheeler092/travo-ai-recommendation-engine.git"

EC2_INSTANCE_IP := $(shell sed -n 's/^EC2_INSTANCE_IP=//p' config.ini)
PRIVATE_KEY_PATH := $(shell sed -n 's/^PRIVATE_KEY_PATH=//p' config.ini)


# Command to create local python venv with required packages for development
.SILENT:
.PHONY: setup
setup: create_env
	( \
		source ./env/bin/activate; \
		make install; \
		echo "$(OK_COLOR)Don't forget to activate venv before working on this project.\
		\nCommand: \`source ./env/bin/activate\`.$(NO_COLOR)\n"; \
	)

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
.PHONY: start-server
start-server:
	ssh -i $(PRIVATE_KEY_PATH) ec2-user@$(EC2_INSTANCE_IP) "\
		if ! [ -d 'travo-ai' ]; then \
			git clone $(GITHUB_REPO) travo-ai -q; \
			sudo chmod o+w travo-ai; \
		else \
			cd travo-ai; \
			git pull -q; \
		fi; \
	"; \
	scp -i $(PRIVATE_KEY_PATH) .env ec2-user@$(EC2_INSTANCE_IP):travo-ai/ > /dev/null 2>&1; \
	ssh -i $(PRIVATE_KEY_PATH) ec2-user@$(EC2_INSTANCE_IP) "\
		cd travo-ai; \
		docker-compose up -d > /dev/null 2>&1; \
	"; \
	echo "$(OK_COLOR)Server up and running. Access API at:\
	\nhttp://$(EC2_INSTANCE_IP)/recommendation$(NO_COLOR)\n"; \


.SILENT:
.PHONY: stop-server
stop-server:
	ssh -i $(PRIVATE_KEY_PATH) ec2-user@$(EC2_INSTANCE_IP) "\
		if [ -d 'travo-ai' ]; then \
			cd travo-ai; \
			docker-compose down > /dev/null 2>&1; \
		fi; \
	"; \


