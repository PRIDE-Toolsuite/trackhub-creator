install_requirements:
	python_install/bin/pip install -r requirements.txt

python_install:
	sudo pip install virtualenv
	virtualenv python_install

dev_environment: python_install install_requirements

.PHONY: dev_environment install_requirements
