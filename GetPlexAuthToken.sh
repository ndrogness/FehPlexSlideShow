#!/usr/bin/env bash

ProductName=`uname -o -m -r`
ProductID=`uname -n`

read -p "Enter your Plex Username: " PlexUsername
read -p "Enter your Plex Password: " PlexPassword

echo "Generating X-Auth-Token for $ProductName, $ProductID"

curl -X "POST" "https://plex.tv/users/sign_in.json" \
     -H "X-Plex-Version: 1.0.0" \
     -H "X-Plex-Product: $ProductName" \
     -H "X-Plex-Client-Identifier: $ProductID" \
     -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
     --data-urlencode "user[password]=$PlexPassword" \
     --data-urlencode "user[login]=$PlexUsername"