install_requirements:
	@python_install/bin/pip install pipreqs nose
	@python_install/bin/pip install -r requirements.txt

python_install:
	@sudo pip install virtualenv
	@virtualenv python_install

bin/cluster-file-exporter.jar: tmp
	cd tmp; git clone git@github.com:PRIDE-Cluster/cluster-file-exporter.git
	cd tmp/cluster-file-exporter; mvn clean package; mv target/cluster-file-exporter*.jar ../bin/cluster-file-exporter.jar

tmp:
	@mkdir tmp

dev_environment: python_install install_requirements bin/cluster-file-exporter.jar

install: dev_environment

update_requirements_file: dev_environment
	@python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)

tests: dev_environment
	@python_install/bin/python main_app.py test

clean_dev:
	@rm -rf python_install

clean_logs:
	@rm -rf logs/*log

clean_tmp:
	@rm -rf tmp

clean_sessions:
	@find run/* -type d | xargs -I{} rm -rf {}

clean: clean_logs clean_sessions clean_tmp

clean_all: clean clean_dev

.PHONY: install dev_environment install_requirements update_requirements_file tests clean_logs clean_sessions clean_dev clean_all clean_tmp clean
