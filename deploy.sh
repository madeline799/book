#!/bin/bash

ROOT=$(pwd)

EXCLUDEMODE="flase"

proxy="false"
prerequisite="false"
apache="false"
buildenv="false"
database="false"
pyjs="false"
inflate="false"

read -s -p "enter sudo password:" sudopasswd
echo ''
read -s -p "enter mysql-root password:" mysqlpasswd
echo ''
read -s -p "enter ziped resource password:" zippasswd
echo ''

for para in $@
do
    if [ "test-$para" = "test-exclude" ]
    then
        EXCLUDEMODE="true"
    elif [ "test-$para" = "test-proxy" ]
    then
        proxy="true"
    elif [ "test-$para" = "test-prerequisite" ]
    then
        prerequisite="true"
    elif [ "test-$para" = "test-apache" ]
    then
        apache="true"
    elif [ "test-$para" = "test-buildenv" ]
    then
        buildenv="true"
    elif [ "test-$para" = "test-database" ]
    then
        database="true"
    elif [ "test-$para" = "test-pyjs" ]
    then
        pyjs="true"
    elif [ "test-$para" = "test-inflate" ]
    then
        inflate="true"
    fi
done

####################################################################
####################################################################
####################################################################

#proxy
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${proxy} = "false" ]
    then
        export http_proxy=http://proxy-prc.intel.com:911
        export https_proxy=http://proxy-prc.intel.com:911
    fi
else
    if [ ${proxy} = "true" ]
    then
        export http_proxy=http://proxy-prc.intel.com:911
        export https_proxy=http://proxy-prc.intel.com:911
    fi
fi





#prerequisite
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${prerequisite} = "false" ]
    then
        echo ${sudopasswd} |sudo -S apt-get update
        echo ${sudopasswd} |sudo -S apt-get -y install python-dev
        echo ${sudopasswd} |sudo -S apt-get -y install python-virtualenv
        echo ${sudopasswd} |sudo -S apt-get -y install mysql-server libmysqld-dev libmysqlclient-dev
    fi
else
    if [ ${prerequisite} = "true" ]
    then
        echo ${sudopasswd} |sudo -S apt-get update
        echo ${sudopasswd} |sudo -S apt-get -y install python-dev
        echo ${sudopasswd} |sudo -S apt-get -y install python-virtualenv
        echo ${sudopasswd} |sudo -S apt-get -y install mysql-server libmysqld-dev libmysqlclient-dev
    fi
fi

#python virtualenv
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${buildenv} = "false" ]
    then
        echo ${sudopasswd} |sudo -S rm -rf ${ROOT}/venv
        virtualenv venv
        ${ROOT}/venv/bin/pip install -r ${ROOT}/requirements.txt -i http://pypi.hustunique.com/simple/
    fi
else
    if [ ${buildenv} = "true" ]
    then
        echo ${sudopasswd} |sudo -S rm -rf ${ROOT}/venv
        virtualenv venv
        ${ROOT}/venv/bin/pip install -r ${ROOT}/requirements.txt -i http://pypi.hustunique.com/simple/
    fi
fi




