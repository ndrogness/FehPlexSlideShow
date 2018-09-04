#!/usr/bin/env python3

import sys
import time
import os
from plexapi.myplex import MyPlexAccount
import subprocess

##############################################
def read_config(cfgfile='FehPlexSlideShow.config'):

    fpssConfig = {}
    numtokens = 0

    with open(cfgfile, mode='r') as f:
        configlines = f.read().splitlines()
    f.close()

    for i in range(0,len(configlines)):
        cline = configlines[i].split("=")

        if cline[0] == 'PlexUsername':
            print("Plex Username:", cline[1])
            fpssConfig['plexusername'] = cline[1]
            numtokens += 1

        if cline[0] == 'PlexPassword':
            print("Plex Password:", cline[1])
            fpssConfig['plexpassword'] = cline[1]
            numtokens += 1

        if cline[0] == 'PlexServer':
            print("Plex Server:", cline[1])
            fpssConfig['plexserver'] = cline[1]
            numtokens += 1

        if cline[0] == 'PlexAuthToken':
            print("Plex AuthToken:", cline[1])
            fpssConfig['plexauthtoken'] = cline[1]
            numtokens += 1

        if cline[0] == 'FehPlaylistFile':
            print("Feh Playlist:", cline[1])
            fpssConfig['fehplaylistfile'] = cline[1]
            numtokens += 1

    if numtokens < 3:
        print("Missing FehPlexSlideShow configuration information")
        exit(-2)

    return fpssConfig

####### end read_config
##############################################


##############################################
def get_plex_photos():

    plexPhotos = {}
    numphotos = 0

    loading()
    # Loop through all libraries looking for photos
    for section in plex.library.sections():

        if section.type == 'photo':
            #print("Name:", section.title, "Type:", section.type)

            for section_item in section.all():
                #print("iName:", section_item.title, "Type:", section_item.type)

                for photo in section_item.photos():
                    qobj = plex.query(photo.key)
                    mpart = qobj[0][0][0].get('key')
                    photourl=plex.url(mpart, includeToken=True)
                    #print("PhotoURL:",photourl)
                    plexPhotos[photo.key] = dict([('title', photo.title), ('url', photourl)])

    return plexPhotos

####### end get_plex_photos
##############################################

##############################################
def feh_write_playlist(photos, playlist_file='FehPlexSlideShow.playlist'):

    if len(photos) == 0:
        print("Empty photos")
        return False

    with open(playlist_file, mode='w') as f:

        for key in photos.keys():
            f.write(photos[key]['url'] + '\n')

    f.close()

    return True

####### end feh_write_playlist
##############################################

##############################################
def feh_slideshow(playlist_file = 'FehPlexSlideShow.playlist', debugonly = False):

    # feh cmd
    feh_cmd = 'feh -Z -F -Y -D 7 --cycle-once -Y --auto-rotate -f ' + playlist_file

    if debugonly:
        print("Running command:", feh_cmd)

    else:
        os.system(feh_cmd)
        myproc = subprocess.Popen(["feh", "-Z", "-F", "-Y", "-D 7", "--cycle-once", "--auto-rotate", "-f", playlist_file])

    return myproc

# end feh_slideshow
##############################################

##############################################
def loading():

    proc = subprocess.Popen(["feh", "-Z", "-F", "-Y", "FehPlexSlideShow-loading.jpg"])
    #time.sleep(5)
    #proc.terminate()
    return proc

# end loading
##############################################

# Read in config file
fpssConfig = read_config('Local.config')

# Use the My Plex Account method of connecting
account = MyPlexAccount(fpssConfig['plexusername'], fpssConfig['plexpassword'])
plex = account.resource(fpssConfig['plexserver']).connect()

DoRun = True
FirstTime = True

try:

    while DoRun:

        # Load splash screen
        proc = loading()

        # Get the photos
        plexPhotos = get_plex_photos()

        # Write the feh playlist file
        feh_write_playlist(plexPhotos, playlist_file=fpssConfig['fehplaylistfile'])

        # Terminate splash screen
        proc.terminate()

        #feh_slideshow(playlist_file=fpssConfig['fehplaylistfile'], debugonly=True)
        ssproc = feh_slideshow(playlist_file=fpssConfig['fehplaylistfile'])
        ssproc.wait()
        #time.sleep(2)

except KeyboardInterrupt:
    DoRun = False
    ssproc.terminate()
    #os.system("rm" + fpssConfig['fehplaylistfile'])
