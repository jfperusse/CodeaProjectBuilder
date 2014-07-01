import os, sys, filecmp, shutil, glob, zipfile, fileinput, subprocess

workspace = os.environ['WORKSPACE']
buildFolder = os.path.join(workspace, "CurrentBuild")
workingFolder = os.path.join(workspace, "WorkingFolder")
extractFolder = os.path.join(workspace, "ExtractedFiles")
rebuildAll = os.environ['REBUILD_ALL']
buildId = os.environ['BUILD_ID']
forceBuildProject = os.getenv('FORCE_BUILD_PROJECT', '')
mobileProvision = os.getenv('MOBILE_PROVISION', '')
projectToBuild = ""
uuid = ""

def PrepareBuild(sourceFile, workingFile):
    global projectToBuild
    
    print("\nPreparing build for " + sourceFile + "...")
    
    # Extract the name of the project from the filename
    basename = os.path.basename(sourceFile)
    projectToBuild = os.path.splitext(basename)[0]
    
    print("  Project name : " + projectToBuild)

    print "  Copying " + sourceFile + "..."
    shutil.copyfile(sourceFile, workingFile)
    
    print "  Removing temporary folders..."
    shutil.rmtree(buildFolder, True)
    shutil.rmtree(extractFolder, True)
    
    print "  Unzipping " + workingFile + "..."
    with zipfile.ZipFile(workingFile, "r") as z:
        z.extractall(extractFolder)
    os.mkdir(buildFolder)
    moveSource = os.path.join(extractFolder, projectToBuild)
    for filename in os.listdir(moveSource):
        shutil.move(os.path.join(moveSource, filename), os.path.join(buildFolder, filename))

def SaveVariables():
    file = open(os.path.join(workspace, 'codeaprojectbuilder.properties'), 'w')
    file.write("PROJECT_TO_BUILD=" + projectToBuild + "\n")
    file.write("BUILD_FOLDER=" + buildFolder + "\n")
    file.write("TARGET_FOLDER=" + workspace + "/Builds/" + projectToBuild + "/" + buildId + "\n")
    file.write("UUID=" + uuid + "\n")

    print("\nLooking for BuildConfig.lua...")
    configPath = os.path.join(buildFolder, projectToBuild + ".codea", "BuildConfig.lua")
    if os.path.isfile(configPath):
        print("  Found! Writing BuildConfig.lua to environment variables...")
        config = ""
        with open(configPath, 'r') as configFile:
            for i, line in enumerate(configFile):
                print("    " + line)
                if not line.startswith('--'):
                    config = config + line
        file.write(config)
        if "BUNDLE_VERSION" not in config:
            file.write("BUNDLE_VERSION=1.0\n")
    else:
        file.write("BUNDLE_VERSION=1.0\n")

    file.close()

def LookForBuilds():
    global uuid
	
    if rebuildAll == 'true':
        shutil.rmtree(workingFolder, True)
    
    if not os.path.isdir(workingFolder):
        os.mkdir(workingFolder)

    print("\nInstalling developer.mobileprovision...")
    pathToParser = os.path.join(workspace, "mobileprovisionParser")
    pathToMobileProvision = os.path.join(workspace, "developer.mobileprovision")
    p = subprocess.Popen([pathToParser, "-f", pathToMobileProvision, "-o", "uuid"], shell=False, stdout=subprocess.PIPE)
    uuid = p.stdout.read().strip()
    print("  uuid : " + uuid + "\n")
    shutil.copyfile(pathToMobileProvision, os.path.join(os.path.expanduser("~"), "Library/MobileDevice/Provisioning Profiles/" + uuid + ".mobileprovision"))

    buildReadyCount = 0
    buildSource = ""
    buildWorking = ""
    
    for f in glob.glob(workspace + "/*.zip"):
        print("Verifying " + f + "...")
        basename = os.path.basename(f)
        projectName = os.path.splitext(basename)[0]
        workingFile = os.path.join(workingFolder, basename)
        if projectName == forceBuildProject or not os.path.isfile(workingFile) or not filecmp.cmp(f, workingFile):
            buildReadyCount = buildReadyCount + 1
            if buildReadyCount == 1:
                print("  Going to build " + f + "...")
                buildSource = f
                buildWorking = workingFile
            else:
                # Delete the file so the build is triggered again
                print("  Queuing build for " + f + "...")
                os.remove(f)

    if buildReadyCount > 0:
        PrepareBuild(buildSource, buildWorking)
        print("\n")
    else:
        print("\nNothing to build\n")
        
    SaveVariables()
    sys.exit(0)
            
LookForBuilds()
