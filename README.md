CodeaProjectBuilder
===================

The CodeaProjectBuilder is a set of python scripts as well as a Jenkins' job configuration which can be used to create a **Codea build machine** for your exported Codea projects.

The build machine will look for changes in your file system (Dropbox, Google Drive, etc.) and automatically build your project. It can also integrate [plug-and-play add-ons](https://github.com/jfperusse/CodeaAddons), resources like mp3 music, and upload your build to TestFlight so that you can do everything directly on your iPad.

Requirements
------------
- Codea on your iPad
- A Mac already setup to build your Codea projects manually
- Jenkins (http://mirrors.jenkins-ci.org/osx/latest)
- A TestFlight account (https://testflightapp.com/)
- Your iOS provisionning profile

Installation
------------
- Install Jenkins on your Mac
- Unload and remove Jenkins' Daemon

```bash
    sudo launchctl unload /Library/LaunchDaemons/org.jenkins-ci.plist
    sudo rm /Library/LaunchDaemons/org.jenkins-ci.plist
```

- Run Jenkins under the same account used to compile Codea projects
  - The default port used is 8080. You can change this using `--httpPort=<YOUR PORT>`

```bash
    java -jar /Applications/Jenkins/jenkins.war
```

- Open Jenkins in your browser (`http://localhost:8080`)
- Install the following Jenkins' plugins (Manage Jenkins, Manage Plugins, Available)
  - File System SCM
  - Xcode integration
  - Environment Injector Plugin (EnvInject)
  - Testflight plugin
- In Jenkins, create a new "free-style software project" called CodeaProjectBuilder.
- Go to `~/.jenkins/jobs/CodeaProjectBuilder` and overwrite `config.xml` with the one found here.
- Go to **Manage Jenkins** and click **Reload Configuration from Disk**.
- Setup your Testflight tokens under Jenkins' **global configuration**
- Update the Jenkins' project's **configuration**.
  - Set **PROJECTS_FOLDER** with the absolute path to your exported Codea projects (e.g. Dropbox, Google Drive).
  - Update the Source Code Management section with the same path.
  - Choose your TestFlight *Token Pair*.
- Copy the files found here to your **PROJECTS_FOLDER** (mobileprovisionParser and python files).
- Copy your mobileprovision to your **PROJECTS_FOLDER** and rename it to "developer.mobileprovision".
  - This allows you to easily update the provisionning provile used by simply updating the version in **PROJECTS_FOLDER**.
- Put your [plug-and-play add-ons](https://github.com/jfperusse/CodeaAddons) under **PROJECTS_FOLDER/Addons**.
- Put your resource files under **PROJECTS_FOLDER/Resources**.

Codea Project Configuration
---------------------------

Some options can be configured per-project directly in Codea by adding a file called "BuildConfig" (BuildConfig.lua).

Here is an example:

```
  --[[
  BUNDLE_ID=com.username.projectname
  DISTRIBUTION_LISTS=DeveloperOnly
  BUNDLE_VERSION=1.1
  BUILD_NOTES=Slower clear of the screen.
  ADDONS=CommonAddon,MusicAddon
  -- We can also have additional comments
  RESOURCES=MenuMusic.mp3,GameMusic.mp3
  FRAMEWORKS=GameKit
  --]]
```

The supported options are:

- BUNDLE_ID
  - Allows you to override the default bundle identifier (CFBundleIdentifier) set by Codea.
- DISTRIBUTION_LISTS
  - Distribution lists to use for TestFlight (which users will have access to the build and get notified).
  - Default value : *empty* (you will have to give permissions manually on TestFlight).
- BUNDLE_VERSION
  - Version to use in Xcode for CFBundleVersion and CFBundleShortVersionString.
  - Default value : 1.0
- BUILD_NOTES
  - Build notes to send to TestFlight.
  - Default value : *empty*
- ADDONS
  - Comma-separated list of [plug-and-play add-ons](https://github.com/jfperusse/CodeaAddons) to include in your Xcode project.
- RESOURCES
  - Comma-separated list of resources to include in your Xcode project (e.g. mp3 files)
  - If this option is missing, all resources are added.
- FRAMEWORKS
  - Comma-separated list of SDK Frameworks to include in your Xcode project (e.g. GameKit)

Usage
-----

- Export your Xcode projects as usual and open them in your desired Cloud service (Dropbox, Google Drive, etc.) corresponding to your **PROJECTS_FOLDER**.
- Wait a few minutes, you should receive an e-mail from TestFlight once your build is ready.
  - If the build fails, you can look at the Console Output in Jenkins.
- Install your project using TestFlight on your iOS device.

Resources
---------

Video presentation of the CodeaProjectBuilder : http://www.youtube.com/watch?v=miS08qAhswY
