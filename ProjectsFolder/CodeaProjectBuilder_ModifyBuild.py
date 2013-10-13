import os, sys, filecmp, shutil, glob, zipfile, fileinput, subprocess

workspace = os.environ['WORKSPACE']
useAddons = os.environ['USE_ADDONS']
addonsFolder = os.path.join(workspace, 'Addons')
resourcesFolder = os.path.join(workspace, 'Resources')
buildFolder = os.path.join(workspace, "CurrentBuild")
projectToBuild = os.environ['PROJECT_TO_BUILD']
addons = os.getenv('ADDONS', '<ALL>')
resources = os.getenv('RESOURCES', '<ALL>')

def AddFilesToProject():
    # Add files from the ADDONS_FOLDER to the Xcode project
    sys.path.append(workspace)
    from mod_pbxproj import XcodeProject
    projectPath = os.path.join(buildFolder, projectToBuild + ".xcodeproj", "project.pbxproj")
    project = XcodeProject.Load(projectPath)
    project_group = project.get_or_create_group('CameraMask')
    
    if addonsFolder and useAddons == 'true' and addons:
        if addons == '<All>':
            print("  Adding all addons to the Xcode project...")
            project.add_folder(addonsFolder, project_group)
        else:
            print("\nFiltering addons...")
            addons_group = project.get_or_create_group('Addons', None, project_group)
            addonsList = addons.split(',')
            [x.strip() for x in addonsList]
            for f in glob.glob(addonsFolder + "/*.*"):
                basename = os.path.basename(f)
                addonName = os.path.splitext(basename)[0]
                if addonName in addonsList:
                    print("  Adding " + basename + " to the Xcode project...")
                    project.add_file(f, addons_group)
    
    if resourcesFolder and resources:
        if resources == '<All>':
            print("  Adding all resources to the Xcode project...")
            project.add_folder(resourcesFolder, project_group)
        else:
            print("\nFiltering resources...")
            resources_group = project.get_or_create_group('CustomResources', None, project_group)
            resourcesList = resources.split(',')
            [x.strip() for x in resourcesList]
            for f in glob.glob(resourcesFolder + "/*.*"):
                basename = os.path.basename(f)
                if basename in resourcesList:
                    print("  Adding " + basename + " to the Xcode project...")
                    project.add_file(f, resources_group, ignore_unknown_type=True)

    if project.modified:
        project.backup()
        project.save()

# Apply my plug-and-play add-ons patch to AppDelegate.mm
# (http://codeatricks.blogspot.ca/2013/07/codea-addons-auto-registration.html)
def ApplyAddonsPatch():
    fileToPatch = os.path.join(workspace, "CurrentBuild", projectToBuild, "AppDelegate.mm")
    insertAfter = "self.viewController = [[CodeaViewController alloc] init];"
    patchLine = "\n\t[[NSNotificationCenter defaultCenter] postNotificationName:@\"RegisterAddOns\" object:self];"
    print("\nPatching AppDelegate.mm...")
    for line in fileinput.input(fileToPatch, inplace=1):
        print line,
        if insertAfter in line:
            print patchLine

def ModifyProject():
    if useAddons == 'true':
        ApplyAddonsPatch()
    AddFilesToProject()
    print("\n")

ModifyProject()