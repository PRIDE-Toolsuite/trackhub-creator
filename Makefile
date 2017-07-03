install_requirements:
	python_install/bin/pip install pipreqs nose
	python_install/bin/pip install -r requirements.txt

python_install:
	sudo pip install virtualenv
	virtualenv python_install

dev_environment: python_install install_requirements

update_requirements_file: dev_environment
	python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)

tests: dev_environment
	python_install/bin/nosetests

dev_clean:
	rm -rf python_install

clean: dev_clean

.PHONY: dev_environment install_requirements dev_clean update_requirements_file tests clean
