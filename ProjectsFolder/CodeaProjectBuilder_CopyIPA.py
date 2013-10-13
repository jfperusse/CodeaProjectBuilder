import os, sys, filecmp, shutil, glob, zipfile, fileinput

targetFolder = os.environ['TARGET_FOLDER']
projectToBuild = os.environ['PROJECT_TO_BUILD']
buildFolder = os.environ['BUILD_FOLDER']

os.makedirs(targetFolder)

print("Copying IPA to Builds folder...")

shutil.copyfile(os.path.join(buildFolder, "build/Release-iphoneos/CodeaProject.ipa"), os.path.join(targetFolder, projectToBuild + ".ipa"))
