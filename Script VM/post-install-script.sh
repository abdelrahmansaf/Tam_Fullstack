#!/bin/bash

echo "##########################################"
echo "# UBUNTU LIVE SERVER POST-INSTALL SCRIPT #"
echo "##########################################"

echo "Mise à jour de l'APT"
apt-get update
#apt-get upgrade

echo "Installation des paquets de base"
sudo apt-get install --yes git git-extras build-essential python3-pip htop glances

clear

#Installation de mysql-server
echo "Installation de MySql-server.."
apt install mysql-server

#echo "Installation de MySql-server-secure.."
#mysql_secure_installation

# Réglage de la date et l'heure 
echo "Réglage de la date et l'heure"
timedatectl set-timezone Europe/Paris

#Commande permettant de désactiver l'authentification par mdp
# while true; do
#     read -p "Voulez vous désactiver l'authentification par mot de passe ?" yn
#     case $yn in
#         [Yn]* ) cd /etc/ssh
#         sed -i -e 's/#PasswordAuthentication yes/PasswordAuthentication no/g' sshd_config; break;;
#         [Nn]* ) exit;;
#         * ) echo "Please answer yes or no.";;
#     esac
# done

#Commande permettant le changement automatique d'une ligne dans sshd_config

echo desactivation du PasswordAuthentication
cd /etc/ssh
sed -i -e 's/#PasswordAuthentication yes/PasswordAuthentication no/g' sshd_config



#mysql --user=root --password=selma2015 < file.sql
sudo sed -i "s/^bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
#sed 's/bind-address            = 0.0.0.0/bind-address            = 192.168.3.20/' /etc/mysql/mysql.conf.d/mysqld.cnf
systemctl restart mysql
sudo /sbin/iptables -A INPUT -i eth0 -p tcp --destination-port 3306 -j ACCEPT
sudo ufw allow from 192.168.1.92 to any port 3306


mysql --user=root --password=selma2015 --execute='source /home/selem/file.sql'

# mysql --user=root --password= --execute='CREATE DATABASE db_selemtest;'

# mysql --user=root --password= --execute='show databases;'


echo "Server has been configured successfully!"

