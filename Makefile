# this is our root dir, this makefile must stay at the root of the repo
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

APP_NAME:="triangler"

.PHONY:
	run-develop-native

run-develop-native:
	zsh -c ". .venv/bin/activate &&  cd src && uvicorn --reload 'triangler.app:app'"
