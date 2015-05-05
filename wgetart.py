#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# This script writed by Python. And download from Artifactory needed
# for us artifacts. {jar, war} and another branches. For example branch,
# set is ext-release-local. And it has seven folders for our project.
# Full path is - ext-release-local/com/transporttv/gradle/{common/server/etc...} -
# Host: 127.0.0.1
# Port: 8082
# Name: Artifactory OSS
# URI: http://{$HOST}/{$PORT}/artifactory/
# method for download: wget (module)
# request to Artifactory: Web API
'''


import os, shutil
import argparse
import wget
import json
import urllib2

url = 'http://10.8.0.138:8081/artifactory/api/'
release = 'ext-release-local'
snapshot = 'ext-snapshot-local'
stable = 'ext-stable-local'
groupId = '/com/transporttv/gradle/'
pathWAR = '/opt/ttv-daemon-java/webapps/root.war'
tmpWAR = '/tmp/root.war'
cmdRestart = '/opt/ttv-daemon-java/bin/jetty.sh restart'
backupWAR = pathWAR + '.1'


def createParse():
    parsesArg = argparse.ArgumentParser(
        prog='wgetart',
        usage='%(prog)s [option]',
        description='This script writed by Python. And download from Artifactory needed \
                    for us artifacts. {jar, war} and another branches. For example branch, \
                    set is ext-release-local. And it has seven folders for our project.',
        version='wgetart 0.1 - (C) 2015 Artem Afonin \
                | Released under the GNU GPL',
        epilog='(C) kdelinx 2015. OpenSource, released under the GNU GPL'
    )
    parsesArg.add_argument('-st', '--stable', action='store_const', const=True, help='GET stable version')
    parsesArg.add_argument('-rl', '--release', action='store_const', const=True, help='GET release version')
    parsesArg.add_argument('-sn', '--snapshot', action='store_const', const=True, help='GET snapshot version')
    parsesArg.add_argument('-bu', '--backup', action='store_const', const=True, help='Return previous version')

    return parsesArg


def prevVersion():
    os.remove(pathWAR)
    shutil.move(backupWAR, pathWAR)


def getListRepo(version, state, build):
    urlStr = url + 'storage/' + release + groupId + build + '/' + version + '-' + state
    listing = urllib2.urlopen(urlStr)
    jsonList = listing.read()
    jsQ = json.loads(jsonList)
    for i in jsQ['children']:
        if 'war' in i['uri']:
            link = urlStr + i['uri']
            downloadUri = link[0:34] + link[46:]
            os.system("echo Start downloading...\n")
            wget.download(downloadUri, tmpWAR)
            if not os.path.exists(pathWAR):
                shutil.move(tmpWAR, pathWAR)
                os.system(cmdRestart)
            else:
                shutil.move(pathWAR, backupWAR)
                shutil.move(tmpWAR, pathWAR)
                os.system(cmdRestart)


if __name__ == "__main__":
    parsesArg = createParse()
    namespace = parsesArg.parse_args()
    parsesArg.print_help()
    # parsesArg.print_usage()

    if parsesArg.parse_args().stable:
        getListRepo(version='0.2.0', state='STABLE', build='mediaserv')
    elif parsesArg.parse_args().release:
        getListRepo(version='0.2.0', state='RELEASE', build='mediaserv')
    elif parsesArg.parse_args().snapshot:
        getListRepo(version='0.2.0', state='SNAPSHOT', build='mediaserv')
    elif parsesArg.parse_args().backup:
        prevVersion()
