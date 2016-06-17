# -*- coding: utf-8 -*-
from optparse import OptionParser
import subprocess
import requests
#使用poster上传文件，需要安装模块poster easy_install poster

from poster.encode import multipart_encode

from poster.streaminghttp import register_openers

import urllib, urllib2
import json

#configuration for iOS build setting
CODE_SIGN_IDENTITY = "iPhone Distribution: Beijing Xiaomaguohe Internet Technology Co., Ltd. (KJ2RF3GMZR)"
PROVISIONING_PROFILE = "9e9b4a13-da9f-4c98-9707-3b6613504813"
CONFIGURATION = "Release"
SDK = "iphoneos"
#定义认证key
authkey="f22e6521aa00---fire对应的token--16861aaeb08d112"

# configuration for pgyer
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "15d6xxxxxxxxxxxxxxxxxx"
API_KEY = "efxxxxxxxxxxxxxxxxxxxx"

def cleanBuildDir(buildDir):
  cleanCmd = "rm -r %s" %(buildDir)
  process = subprocess.Popen(cleanCmd, shell = True)
  process.wait()
  print "cleaned buildDir: %s" %(buildDir)


def parserUploadResult(jsonResult):
  resultCode = jsonResult['code']
  if resultCode == 0:
    downUrl = DOWNLOAD_BASE_URL +"/"+jsonResult['data']['appShortcutUrl']
    print "Upload Success"
    print "DownUrl is:" + downUrl
  else:
    print "Upload Fail!"
    print "Reason:"+jsonResult['message']

def uploadIpaToPgyer(ipaPath):
  print "ipaPath:"+ipaPath
  files = {'file': open(ipaPath, 'rb')}
  headers = {'enctype':'multipart/form-data'}
  payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'2','isPublishToPublic':'2', 'password':'DanluTest'}
  print "uploading...."
  r = requests.post(PGYER_UPLOAD_URL, data = payload ,files=files,headers=headers)
  if r.status_code == requests.codes.ok:
    result = r.json()
    parserUploadResult(result)
  else:
    print 'HTTPError,Code:'+r.status_code

def buildProject(project, target, output):
  buildCmd = 'xcodebuild -project %s -target %s -sdk %s -configuration %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' %(project, target, SDK, CONFIGURATION, CODE_SIGN_IDENTITY, PROVISIONING_PROFILE)
  process = subprocess.Popen(buildCmd, shell = True)
  process.wait()

  signApp = "./build/%s-iphoneos/%s.app" %(CONFIGURATION, target)
  signCmd = "xcrun -sdk %s -v PackageApplication %s -o %s" %(SDK, signApp, output)
  process = subprocess.Popen(signCmd, shell=True)
  (stdoutdata, stderrdata) = process.communicate()

#	uploadIpaToPgyer(output)
#	cleanBuildDir("./build")

def buildWorkspace(workspace, scheme, output):
  process = subprocess.Popen("pwd", stdout=subprocess.PIPE)
  (stdoutdata, stderrdata) = process.communicate()
  buildDir = stdoutdata.strip() + '/build'
  print "buildDir: " + buildDir
  buildCmd = 'xcodebuild -workspace %s -scheme %s -sdk %s -configuration %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" SYMROOT=%s' %(workspace, scheme, SDK, CONFIGURATION, CODE_SIGN_IDENTITY, PROVISIONING_PROFILE, buildDir)
  process = subprocess.Popen(buildCmd, shell = True)
  process.wait()

  signApp = "./build/%s-iphoneos/%s.app" %(CONFIGURATION, scheme)
  signCmd = "xcrun -sdk %s -v PackageApplication %s -o %s" %(SDK, signApp, output)
  process = subprocess.Popen(signCmd, shell=True)
  (stdoutdata, stderrdata) = process.communicate()
#    print (" zhi  %s"%("dsadda"))
#    print ("His name is %s"%("Aviad"))
  PostFilename(output)
#  print(output)

#  uploadIpaToPgyer(output)
  cleanBuildDir(buildDir)

# 立柱 添加


def get_token_key():
  url = "http://api.fir.im/apps"
  values = {'type':'ios','bundle_id':'com.xiaoma.UniverseTOEFLEnterprise','api_token':authkey}
  encodedata = urllib.urlencode(values)
  request = urllib2.Request(url,encodedata)
  respone = urllib2.urlopen(request)
  getdata = json.loads(respone.read())
  return getdata


def PostFilename(filename):
  getdata_dirs = get_token_key()
  register_openers()
  key = getdata_dirs['cert']['binary']['key']
  token = getdata_dirs['cert']['binary']['token']
  url = getdata_dirs['cert']['binary']['upload_url']
  file = filename
  x_name = '宇宙托福'
  x_version =  '1.2.0'
  x_build = '2'
  datagen, headers = multipart_encode({"file": open(file, "rb"),"key": key,"token":token,
                                        "url":url,"x:name": x_name, "x:version": x_version,"x:build":x_build
                                        })
  request = urllib2.Request(url, datagen, headers)
  print urllib2.urlopen(request).read()

#PostFilename('UniverseTOEFL.ipa')

# 立柱 添加

def xcbuild(options):
  project = options.project
  workspace = options.workspace
  target = options.target
  scheme = options.scheme
  output = options.output
  if project is None and workspace is None:
    pass
  elif project is not None:
    buildProject(project, target, output)
  elif workspace is not None:
    buildWorkspace(workspace, scheme, output)

def main():
  parser = OptionParser()
  parser.add_option("-w", "--workspace", help="Build the workspace name.xcworkspace.", metavar="name.xcworkspace")
  parser.add_option("-p", "--project", help="Build the project name.xcodeproj.", metavar="name.xcodeproj")
  parser.add_option("-s", "--scheme", help="Build the scheme specified by schemename. Required if building a workspace.", metavar="schemename")
  parser.add_option("-t", "--target", help="Build the target specified by targetname. Required if building a project.", metavar="targetname")
  parser.add_option("-o", "--output", help="specify output filename", metavar="output_filename")
  (options, args) = parser.parse_args()
  print "options: %s, args: %s" % (options, args)
  xcbuild(options)

if __name__ == '__main__':
  main()
