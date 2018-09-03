#!/usr/bin/env python3



import sys
import time
import pygame
import random
import os
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

def readconfig(cfgfile='Plex.cfg'):

    PlexConfig = {}
    numtokens = 0

    print("Opening:", cfgfile)
    with open(cfgfile, mode='r') as f:
        plexconfig = f.read().splitlines()
    f.close()

    for i in range(0,len(plexconfig)):
        cline = plexconfig[i].split("=")
        #print(cline)

        if cline[0] == 'PlexUsername':
            print("Plex Username:", cline[1])
            PlexConfig['plexusername'] = cline[1]
            numtokens += 1

        if cline[0] == 'PlexPassword':
            print("Plex Password:", cline[1])
            PlexConfig['plexpassword'] = cline[1]
            numtokens += 1

        if cline[0] == 'PlexServer':
            print("Plex Server:", cline[1])
            PlexConfig['plexserver'] = cline[1]
            numtokens += 1

        if cline[0] == 'PlexAuthToken':
            print("Plex AuthToken:", cline[1])
            PlexConfig['plexauthtoken'] = cline[1]
            numtokens += 1

    if numtokens < 3:
        print("Missing Plex configuration information")
        exit(-2)

    return PlexConfig

def feh_write_file(feh_playlist='FehPlexSlideShow.playlist'):
    pass


# Read in config file for Plex
PlexConfig = readconfig()

# Use the My Plex Account method of connecting
account = MyPlexAccount(PlexConfig['plexusername'], PlexConfig['plexpassword'])
plex = account.resource(PlexConfig['plexserver']).connect()

# Loop through all libraries looking for photos
for section in plex.library.sections():

    if section.type == 'photo':
        print("Name:", section.title, "Type:", section.type)

        for section_item in section.all():
            print("iName:", section_item.title, "Type:", section_item.type)

            for photo in section_item.photos():
                print("Photo:", photo.title, "Key:", photo.key, "Media:", photo.media, "ParentKey:", photo.parentKey, "ParentRKey:", photo.parentRatingKey)
                #print(dir(photo.media))
                #print(photo.media[0])
                #print(dir(plex.query(photo.key)))
                qobj = plex.query(photo.key)
                #print("Qobj 0:",qobj[0])
                #print("Qobj 0,0:",qobj[0][0])
                #print(plex.transcodeImage(qobj[0][0],320,320))
                mpart = qobj[0][0][0].get('key')
                #print(plex.url(photo.key))

                photourl=plex.url(mpart, includeToken=True)
                print("PhotoURL:",photourl)

                #print(mpart, photo.section(), photo.photoalbum())
                #print(mpart.get('key'))
                #for i in range(0, len(mpart)):
                #for i, v in mpart.items():
                #    print("Key:", i, "Value:", v)
                #exit()
                #pmedia = plex.media
