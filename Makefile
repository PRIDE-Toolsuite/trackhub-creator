lsf_install_requirements: install_requirements
	@echo "LSF - Requirements installed"

install_requirements:
	@python_install/bin/pip install pipreqs nose
	@python_install/bin/pip install -r requirements.txt

lsf_python_install:
	@source scripts/commons-priv/ebi-lsf-clean-environment.sh; pip install --upgrade --user virtualenv
	@source scripts/commons-priv/ebi-lsf-clean-environment.sh; virtualenv -p `which python3` lsf_python_install
	@ln -s lsf_python_install python_install

python_install:
	@sudo pip install virtualenv
	@virtualenv python_install

bin/maven:
	@cd tmp; wget http://www.mirrorservice.org/sites/ftp.apache.org/maven/maven-3/3.5.0/binaries/apache-maven-3.5.0-bin.tar.gz
	@cd tmp; tar xzvf apache-maven-3.5.0-bin.tar.gz
	@mv tmp/apache-maven-3.5.0 bin/maven
	
bin/cluster-file-exporter/cluster-file-exporter.jar: tmp
	@cd tmp; git clone git@github.com:PRIDE-Cluster/cluster-file-exporter.git
	@cd tmp/cluster-file-exporter; mvn clean package -P ebi-repo-profile,db-pride-repo-pridepro,db-pride-repo-pridecluster-user
	@mkdir bin/cluster-file-exporter
	@cd bin/cluster-file-exporter; unzip ../../tmp/cluster-file-exporter/target/cluster-file-exporter*zip; cp cluster-file-exporter-*jar cluster-file-exporter.jar

bin/pogo/pogo: tmp
	@cd tmp; git clone https://github.com/PRIDE-Toolsuite/PoGo.git pogo
	@cd tmp/pogo/PoGo/src; make
	@mkdir -p bin/pogo
	@cp tmp/pogo/PoGo/src/PoGo bin/pogo/pogo

tmp:
	@mkdir tmp

dev_environment: python_install install_requirements bin/cluster-file-exporter/cluster-file-exporter.jar bin/pogo/pogo

install: dev_environment

lsf_install: lsf_python_install lsf_install_requirements bin/pogo/pogo

update_requirements_file: dev_environment
	@python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)

lsf_tests: tests
	@echo "LSF - Unit Tests under LSF environment run"

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

clean_bin:
	@rm -rf bin/*
	@touch bin/empty

lsf_clean: clean
	@echo "LSF - Clean run"

clean: clean_logs clean_sessions clean_tmp

lsf_clean_all: clean
	@rm python_install
	@rm -rf lsf_python_install

clean_all: clean clean_dev

.PHONY: install dev_environment install_requirements update_requirements_file tests clean_logs clean_sessions clean_dev clean_all clean_tmp clean_bin clean lsf_install_requirements lsf_python_install lsf_install lsf_tests lsf_clean lsf_clean_all
