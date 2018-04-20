# -*-coding:utf-8-*-
#author thc
# 多渠道打包

import os
import xml.etree.ElementTree as ET
import shutil

curPath = os.path.abspath('.')

files = os.listdir(curPath)
apkFileName = ''
apkName = ''
align = ''
keyPassword = ''
alignPassword = ''

with open(curPath+'/config/config.txt') as f:
    str = f.readlines(3)
    align = str[0].strip('\n')
    keyPassword = str[1].strip('\n')
    alignPassword = str[2].strip('\n')
    print(align)
    print(keyPassword)
    print(alignPassword)


for f in files:
    if f.endswith('.apk'):
        apkFileName = f
        apkName = apkFileName.split('.')[0]
print(apkFileName)


def getChannel():
    file = curPath + '/config/channel.txt'
    deleteApk()
    with open(file, 'r') as f:
        for channel in f.readlines():
            print(channel.strip('\n'))
            channel = channel.strip('\n')
            packApk(channel)

def packApk(channel):
    print(channel)
    removeDir(channel)
    unpackcmd = 'java -jar tools/apktool.jar d ' + apkFileName + ' -o ' + curPath + '\out' + '\\' + channel
    print(unpackcmd)
    os.system(unpackcmd)
    modifyXml(channel, curPath + '\out\\' + channel + '\AndroidManifest.xml')
    packcmd = 'java -jar tools/apktool.jar b ' + curPath + '\out' + '\\' + channel
    os.system(packcmd)
    print('pack apk success')
    keydir = curPath + '\keystore'
    if os.path.isdir(keydir):
        if os.path.isfile(keydir+'\\'+os.listdir(keydir)[0]):
            print(os.listdir(keydir)[0])
            keystoreFile = curPath + '\keystore\\'+os.listdir(keydir)[0]
            print(keystoreFile)
            signedApk(channel,keystoreFile,keyPassword,alignPassword,curPath+'\out\\apk\\'+apkName+'_'+channel+".apk ",curPath+'\out\\'+channel+'\dist\\'+apkFileName,align)


def signedApk(channel,keystore,storepass,alignpass,signedapk,unsignedapk,align):
    signApkCmd = 'jarsigner -verbose -keystore "%s" -storepass "%s" -keypass "%s" -signedjar "%s" "%s" "%s"' %(keystore,storepass,alignpass,signedapk,unsignedapk,align)
    print(signApkCmd)
    os.system(signApkCmd)
    removeDir(channel)

def removeDir(channel):
    file = curPath + '\out' + '\\' + channel
    if os.path.isdir(file):
        print(curPath + '\out' + '\\' + channel)
        shutil.rmtree(curPath + '\out' + '\\' + channel)
    else:
        print('channel file not exit')

def deleteApk():
    if os.path.isdir(curPath+'\out\\apk'):
        shutil.rmtree(curPath + '\out\\apk')
        os.mkdir(curPath + '\out\\apk')
    else:
        os.mkdir(curPath + '\out\\apk')


def modifyXml(channel, descfile):
    print(channel,descfile)
    androidManifestFile = descfile
    desc_tree = ET.parse(androidManifestFile)
    desc_root = desc_tree.getroot()
    application = desc_root.find('application')
    metadatas = application.findall('meta-data')
    for metadata in metadatas:
        if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'Channel':
            value = metadata.get('{http://schemas.android.com/apk/res/android}value')
            print(value)
            print(channel)
            metadata.set('{http://schemas.android.com/apk/res/android}value', channel)
            print(metadata.get('{http://schemas.android.com/apk/res/android}value'))
            desc_tree.write(androidManifestFile)


getChannel()