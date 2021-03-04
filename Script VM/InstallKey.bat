::La commande echo off désactive l'affichage pour le script entier.
@ECHO OFF
:: chcp 65001 nous permet de prendre en compte les caractères utf-8
chcp 65001

echo                                     ################################
ECHO ------------------------------------### Lancement du script Bat..###-----------------------------------
echo                                     ################################

:: Commande qui nous renvoie notre adresse Ip (de l'hôte)
FOR /F "tokens=4 delims= " %%i in ('route print ^| find " 0.0.0.0"') do set localIp=%%i

echo Your IP Address is: %localIp%
:: Commande qui nous renvoie notre nom d'utilisateur
Echo Salut %USERNAME% !

ECHO Génération de la clé publique :

:: Commande permettant de demander à si il veut bien générer la clé
:: Le "goto" nous permet de nous renvoyer au debut de la commande 
:choice
set /P c=Etes vous sûr de vouloir générer la clé [Y/N]?
if /I "%c%" EQU "Y" goto :somewhere
if /I "%c%" EQU "N" goto :somewhere_else
goto :choice

:: Début des actions si Yes
:somewhere

set /p login=Veuillez entrer votre LOGIN:
:blank
if "%LOGIN%" == "" (
    echo Entrez quelque chose !
    set /p login=Veuillez entrer votre LOGIN:
    goto :blank
)

set /p ip=Veuillez entrer votre IP:
:blank2
if "%ip%" == "" (
    echo Entrez quelque chose !
    set /p ip=Veuillez entrer votre IP:
    goto :blank2
)

ECHO Génération de la clé pour l'adresse %LOGIN%@%ip%
PAUSE

::Commande nous permettant de générer les clés

ssh-keygen

ECHO Connexion au serveur ssh ...
PAUSE

:: Commande permettant créer le dossier .ssh et d'y ajouter le fichier authorized key
ssh %LOGIN%@%ip% "mkdir .ssh && cd .ssh && touch authorized_keys"

:: Commande qui envoie la clé vers le fichier dans la VM
type C:\Users\%USERNAME%\.ssh\id_rsa.pub | ssh %LOGIN%@%ip% "cat >> .ssh/authorized_keys"

ECHO La clé a été généré et copié vers l'adresse !
:: Permet de générer un fichier texte avec l'adresse Ip de la VM
echo %ip%>C:\Users\%USERNAME%\Desktop\iptest.txt
PAUSE

::Commande proposant d'envoyer un fichier 
:choicefile
set /P c=Souhaitez vous envoyer un fichier vers l'adresse [Y/N]?
if /I "%c%" EQU "Y" goto :somewhere1
if /I "%c%" EQU "N" goto :somewhere_else1
goto :choicefile
::Commandes si on veut envoyer un fichier
:somewhere1

echo Envoie du fichier fichier vers l'adresse ...

set /p cheminfichier=Veuillez entrer le chemin exact vers le fichier postinstall :
echo (exemple :C:\Users\%USERNAME%\Desktop\fichier.sh)

:blank3
if "%cheminfichier%" == "" (
    echo Entrez quelque chose !
    set /p cheminfichier=Veuillez entrer le chemin exact vers le fichier postinstall:
    goto :blank3
)

set /p cheminfichier2=Veuillez entrer le chemin exact vers le fichier sql:
echo (exemple :C:\Users\%USERNAME%\Desktop\fichier.sql)
:blank5
if "%cheminfichier2%" == "" (
    echo Entrez quelque chose !
    set /p cheminfichier2=Veuillez entrer le chemin exact vers le fichier sql:
    goto :blank5
)


set /p destinationfichier=Veuillez entrer la destination du fichier: 
:blank4
if "%destinationfichier%" == "" (
    echo Entrez quelque chose !
    set /p destinationfichier=Veuillez entrer la destination du fichier:
    goto :blank4
)

:: ligne permettant d'envoyer un fichier !
scp %cheminfichier% %LOGIN%@%ip%:%destinationfichier%
scp %cheminfichier2% %LOGIN%@%ip%:%destinationfichier%

echo Le fichier à bien été envoyé !
pause
Echo Lancement du script sur la vm :

set /p nmfich1=Veuillez entrer le nom du fichier bash à lancer: 
echo exemple:%cheminfichier%
:nmfich
if "%nmfich1%" == "" (
    echo Entrez quelque chose !
    set /p nmfich=Veuillez entrer le nom du fichier bash à lancer:
    goto :nmfich
)
pause

::Installation de module sur la machine hôte
ECHO Mise à jour du pip install :
python -m pip install --upgrade pip

echo Installation PyMySql
pip install PyMySQL

echo Installation cryptography
pip install cryptography

::Echo Changement des noms de vos fichier
::ren %cheminfichier% post-install-server.sh
::ren %cheminfichier2% file.sql


ssh %LOGIN%@%ip% "chmod 777 ./%nmfich1%"
ssh -t %LOGIN%@%ip% "sudo -S ./%nmfich1%"

pause

exit
:: Commandes si on ne veut pas envoyer de fichier
:somewhere_else1
echo Vous avez choisis de ne pas envoyer de fichier .
Echo Lancement du script sur la vm :

ssh %LOGIN%@%ip% "chmod 777 ./%nmfich%"
ssh -t %LOGIN%@%ip% "sudo -S ./%nmfich%"

pause
echo Fin du script.
pause
exit



:somewhere_else

ECHO La clé n'a pas été généré...
echo Fin du script

PAUSE
exit

