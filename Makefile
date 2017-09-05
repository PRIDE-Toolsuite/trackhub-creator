lsf_install_requirements: install_requirements
	@echo -e "\n[LSF] Requirements installed <---\n\n"

install_requirements:
	@python_install/bin/pip install pipreqs nose
	@python_install/bin/pip install -r requirements.txt

lsf_python_install:
	@source scripts/commons-priv/ebi-lsf-clean-environment.sh; pip install --upgrade --user virtualenv
	@source scripts/commons-priv/ebi-lsf-clean-environment.sh; virtualenv -p `which python3` lsf_python_install
	@ln -s lsf_python_install python_install
	@echo -e "\n[LSF] Local Python Environment READY <---\n\n"

python_install:
	@sudo pip install virtualenv
	@virtualenv python_install

bin/maven:
	@cd tmp; wget http://www.mirrorservice.org/sites/ftp.apache.org/maven/maven-3/3.5.0/binaries/apache-maven-3.5.0-bin.tar.gz
	@cd tmp; tar xzvf apache-maven-3.5.0-bin.tar.gz
	@mv tmp/apache-maven-3.5.0 bin/maven

bin/lsf-cluster-file-exporter: tmp bin/maven
	@cd tmp; git clone https://github.com/PRIDE-Cluster/cluster-file-exporter.git
	@source scripts/commons-priv/ebi-lsf-clean-environment.sh; source scripts/commons-priv/ebi-lsf-java8-environment.sh; cd tmp/cluster-file-exporter; ../../bin/maven/bin/mvn clean package -s ../../config/private/maven/settings.xml -P ebi-repo-profile,db-pride-repo-pridepro,db-pride-repo-pridecluster-user
	@mkdir bin/lsf-cluster-file-exporter
	@cd bin/lsf-cluster-file-exporter; unzip ../../tmp/cluster-file-exporter/target/cluster-file-exporter*zip; cp cluster-file-exporter-*jar cluster-file-exporter.jar
	@cd bin; ln -s lsf-cluster-file-exporter cluster-file-exporter

bin/cluster-file-exporter/cluster-file-exporter.jar: tmp bin/maven
	@cd tmp; git clone https://github.com/PRIDE-Cluster/cluster-file-exporter.git
	@cd tmp/cluster-file-exporter; ../../bin/maven/mvn clean package -s ../../config/private/maven/settings.xml -P ebi-repo-profile,db-pride-repo-pridepro,db-pride-repo-pridecluster-user
	@mkdir bin/cluster-file-exporter
	@cd bin/cluster-file-exporter; unzip ../../tmp/cluster-file-exporter/target/cluster-file-exporter*zip; cp cluster-file-exporter-*jar cluster-file-exporter.jar

bin/pogo/pogo: tmp
	@cd tmp; git clone https://github.com/PRIDE-Toolsuite/PoGo.git pogo
	@cd tmp/pogo/PoGo/src; make
	@mkdir -p bin/pogo
	@cp tmp/pogo/PoGo/src/PoGo bin/pogo/pogo

tmp:
	@mkdir tmp

install_dev: python_install install_requirements bin/cluster-file-exporter/cluster-file-exporter.jar bin/pogo/pogo

install: python_install install_requirements bin/cluster-file-exporter/cluster-file-exporter.jar bin/pogo/pogo

lsf_install: lsf_python_install lsf_install_requirements bin/lsf-cluster-file-exporter bin/pogo/pogo

update_requirements_file: dev_environment
	@python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)

tests: 
	@python_install/bin/python main_app.py test

lsf_tests: 
	@echo "[LSF] - Unit Tests under LSF environment run"
	@python_install/bin/python main_app.py test

clean_dev: clean_bin
	@rm -rf python_install

clean_logs:
	@rm -rf logs/*log

lsf_clean_logs:
	@rm -rf logs/lsf-*

clean_tmp:
	@rm -rf tmp

clean_sessions:
	@find run/* -type d | xargs -I{} rm -rf {}

clean_bin:
	@rm -rf bin/*
	@touch bin/empty

lsf_clean: clean lsf_clean_logs
	@echo "[LSF] - Clean run"

clean: clean_logs clean_sessions clean_tmp

lsf_clean_all: clean clean_bin
	@rm python_install
	@rm -rf lsf_python_install

clean_all: clean clean_dev

.PHONY: install install_dev install_requirements update_requirements_file tests clean_logs clean_sessions clean_dev clean_all clean_tmp clean_bin clean lsf_install_requirements lsf_python_install lsf_install lsf_tests lsf_clean lsf_clean_all lsf_clean_logs
