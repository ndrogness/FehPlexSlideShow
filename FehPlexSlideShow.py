#!/usr/bin/env python3

import sys
import time
import os
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
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

        if cline[0] == 'PlexMethod':
            print("Plex Method:" , cline[1])
            fpssConfig['plexmethod'] = cline[1]
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

    #loading()
    # Loop through all libraries looking for photos
    for section in plex.library.sections():

        if section.type == 'photo':
            #print("Name:", section.title, "Type:", section.type)

            for section_item in section.all():
                #print("iName:", section_item.title, "Type:", section_item.type)

                for photo in section_item.photos():
                    # Query for photo key (returns Media Container)
                    qobj = plex.query(photo.key)

                    # Need media part of media container
                    mpart = qobj[0][0][0].get('key')

                    # Various Media information
                    photo_height = qobj[0][0].get('height')
                    photo_width = qobj[0][0].get('width')
                    photo_aspect_ratio = qobj[0][0].get('aspectRatio')

                    #if img_width > img_height:
                    #    print(img_height, img_width, img_aspect_ratio)
                    #   print(photo.title, photo.media, photo.key, photo.ratingKey, imgurl)

                    # Direct URL to media part (only works when local but useful for debuggin)
                    photo_direct_url = plex.url(mpart, includeToken=True)

                    # plex.url works when local to PMS, but not public network
                    #photo_url2 = plex.url(mpart)
                    #photo_url2 = photo_url2 + '?X-Plex-Token=' + fpssConfig['plexauthtoken']
                    #print("PhotoURL:",photo_direct_url, photo_url2)
                    #plexPhotos[photo.key] = dict([('title', photo.title), ('url', photo_direct_url)])

                    # Using transcode call since it works on local and pub networks
                    photo_url = plex.transcodeImage(mpart, photo_height, photo_width)

                    plexPhotos[photo.key] = dict([('title', photo.title), ('url', photo_url)])
                    print("Adding", photo.key, photo_direct_url)

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
        #os.system(feh_cmd)
        myproc = subprocess.Popen(["feh", "-Z", "-F", "-Y", "-D 7", "--cycle-once", "--auto-rotate", "-f", playlist_file])

    return myproc

# end feh_slideshow
##############################################

##############################################
def loading():

    lproc = subprocess.Popen(["feh", "-Z", "-F", "-Y", "FehPlexSlideShow-loading.jpg"])
    #time.sleep(5)
    #proc.terminate()
    return lproc

# end loading
##############################################

def get_plex_server():

    PlexMethod = MyPlexAccount
    if fpssConfig['plexmethod'] == 'MyPlexAccount':
        # Use the My Plex Account method of connecting
        #account = MyPlexAccount(fpssConfig['plexusername'], fpssConfig['plexpassword'], token=fpssConfig['plexauthtoken'], timeout=5)
        account = MyPlexAccount(fpssConfig['plexusername'], fpssConfig['plexpassword'], timeout=5)
        cons = account.resource(fpssConfig['plexserver']).connections
        print("Connections available:", len(cons), "Access Token:", account.resource(fpssConfig['plexserver']).accessToken)

        for r in range(0, len(cons)):
            conr = cons[r]
            #print(dir(conr))
            print(conr.address, conr.httpuri, conr.protocol, conr.key, conr.uri, conr.local)
            #print(cons[r])
            #exit()

        try:
            pms = account.resource(fpssConfig['plexserver']).connect()
        except plexapi.exceptions.NotFound:
            print("Could not connect to plex")
            exit(-1)

    else:

        baseurl = fpssConfig['plexmethod']
        pms = PlexServer(baseurl, fpssConfig['plexauthtoken'])

    return pms

# end get plex server
##############################################

# Read in config file
fpssConfig = read_config('Local.config')


DoRun = True
FirstTime = True

try:

    while DoRun:

        # Load splash screen
        proc = loading()

        # Connect to the Plex Server
        plex = get_plex_server()

        # Get the photos from Plex Server
        plexPhotos = get_plex_photos()

        # Write the feh playlist file
        feh_write_playlist(plexPhotos, playlist_file=fpssConfig['fehplaylistfile'])

        # Terminate splash screen
        proc.kill()

        #feh_slideshow(playlist_file=fpssConfig['fehplaylistfile'], debugonly=True)
        ssproc = feh_slideshow(playlist_file=fpssConfig['fehplaylistfile'])
        ssproc.wait()


except:
    DoRun = False
    proc.kill()
    ssproc.kill()
    exit()
    #os.system("rm" + fpssConfig['fehplaylistfile'])
