#!/usr/bin/python


import os
import os.path
import shutil

rootdir = "/Users/apple/WtyProject/ios_universe/UniverseTOEFL/UniverseTOEFL"
NameList = []
ClassPathList = []
RemovePathList = []
#  find .h 
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        if filename.find(".h") != -1 :
            NameList.append(filename)
            ClassPath = os.path.join(parent,filename) 
            ClassPathList.append(ClassPath)  

# find .h not be quoted
for ClassName in NameList:
    ImportName = "import " + '"' +  ClassName + '"'
    Flag = False
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            ClassPath = os.path.join(parent,filename)
            ClassMFile = ClassName[0:-1]
            ClassMFile = ClassMFile + "m"
            if filename == ClassName or filename == ClassMFile :
                continue  
            for line in open(ClassPath):
                if line.find(ImportName) != -1:
                    print filename
                    print ClassName
                    Flag = True
    if not Flag:    
        print ClassName
        index = NameList.index(ClassName)
        RemovePathList.append(ClassPathList[index])
        ClassMPath = ClassPathList[index][0:-1]
        ClassMPath = ClassMPath + "m"
        RemovePathList.append(ClassMPath)

print "the class path  needed to be remove"
print  RemovePathList
#  delete class mot be quoted
for RemoveFile in RemovePathList:
#    os.remove(RemoveFile)
#    shutil.move(RemoveFile,"/home/users/hanping") 
    pass


