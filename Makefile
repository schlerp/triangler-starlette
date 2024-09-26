# this is our root dir, this makefile must stay at the root of the repo
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

APP_NAME:="triangler"

.PHONY:
	run-develop-native

run-develop-native:
	zsh -c ". .venv/bin/activate &&  cd src && uvicorn --reload 'triangler.app:app'"

run-develop-docker:
	docker build --target develop -t ${APP_NAME} . && docker run -it --rm --env-file ./dev.env -v ${ROOT_DIR}/src/${APP_NAME}:/app/src/${APP_NAME} -p 8000:8000 ${APP_NAME}

run-shell-docker:
	docker build --target develop -t ${APP_NAME} . && docker run --rm -it --env-file ./dev.env -v ${ROOT_DIR}/src/${APP_NAME}:/app/src/${APP_NAME} --entrypoint bash -p 8000:8000 ${APP_NAME}
