#!/bin/sh/

Name_Db_Container="db"
if [ "$(docker ps -q -f name=$Name_Db_Container)" ]; then
    echo "Le conteneur ($Name_Db_Container) fonctionne bien."
else
    echo "Le conteneur ($Name_Db_Container) ne fonctionne pas."
fi

Name_Client_Container="app"
if [ "$(docker ps -q -f name=$Name_Client_Container)" ]; then
    echo "Le conteneur ($Name_Client_Container) fonctionne bien."
else
    echo "Le conteneur ($Name_Client_Container) ne fonctionne pas."
fi