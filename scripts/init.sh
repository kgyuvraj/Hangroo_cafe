################'''
#Created on May 30, 2019
#
#@author: akshay.gupta
#################'''


mkdir /var/log/django/
sudo yum -y install python3
sudo yum -y install python-pip3
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openldap-devel python3-devel libpq-dev python3-dev mysql-devel
sudo yum -y install xorg-x11-server-Xvfb xorg-x11-fonts-Type1 xorg-x11-fonts-75dpi
sudo yum -y install wkhtmltopdf

#### installing pip modules
pip3 install -r /apps/hangroo/requirements.txt

############# migrate
cd /apps/hangroo
python3 manage.py migrate


