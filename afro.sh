#!/bin/bash
PackageExists()
{
  mkdir .existsTemp
  found=0
  git clone --single-branch --branch versions https://github.com/vel2006/AfroLinux .existsTemp
  while IFS= read -r line; do
    if [ "$line" == "$1" ]; then
      found=1
      break
    else
      continue
    fi
  done < .existsTemp/todateVersion
  if [ "$found" == 1 ]; then
    echo 1
  else
    echo 0
  fi
  rm -Rf .existsTemp
}
SystemPackageVersion()
{
  echo $(echo $(cat /etc/AfroLinux/files) | grep "$1" | awk '{print $2}')
}
PackageVersion()
{
  mkdir .versionTemp
  git clone --single-branch --branch versions https://github.com/vel2006/AfroLinux .versionTemp
  versions=$(cat .versionTemp/todateVersion)
  echo $(echo $versions | grep "$1" | awk '{print $2}')
  rm -Rf .versionTemp
}
DownloadPackage()
{
  mkdir .installTemp
  git clone --single-branch --branch $1 https://github.com/vel2006/AfroLinux .installTemp
  mv .installTemp/$(ls) /etc/AfroLinux
  chmod +x .installTemp/$1
  echo "$1 $(PackageVersion $1)" >> /etc/AfroLinux/files
  rm -Rf .installTemp
}
RemovePackage()
{
  rm /etc/AfroLinux/$1
}
PackageOnSystem()
{
  if [ $(cat /etc/AfroLinux/files | grep "$1") ]; then
    echo 1
  else
    echo 0
  fi
}
UpdatePackage()
{
  mkdir .updateTemp
  git clone --single-branch --branch $1 https://github.com/vel2006/AfroLinux .updateTemp
  if [ $(PackageExists $1) == 1 ]; then
    if [ $(PackageOnSystem $1) == 1 ]; then
      if [ $(SystemPackageVersion $1) < $(PackageVersion $1) ]; then
        RemovePackage $1
        DownloadPackage $1
      else
        echo "ERROR: package up to date"
      fi
    else
      echo "ERROR: $1 package no installed"
    fi
  else
    echo "ERROR: $1 package does not exist or not connected to internet"
  fi
  rm -Rf .updateTemp
}
if [ "$1" == "--help" ]; then
  echo "Afro is the custom (very bad) package manager for Afro Linux"
  echo "It only works for custom scripts the dev has published on Github under the package's branch"
  echo "Format to use is this:"
  echo "afro <add/remove/update/version/find> <package>"
  exit
fi
if [ $# != 2 ]; then
  echo "ERROR: incorrect amount of arguments, correct format: (you can only do them one at a time)"
  echo "afro <add/remove/update/version/find> <package>"
  exit
fi
if [ $1 == "remove" ]; then
  if [ $(PackageOnSystem $1) == 1 ]; then
    RemovePackage $2
  else
    echo "ERROR: Package not installed"
  fi
elif [ $1 == "find" ]; then
  if [ $(PackageExists) == 1 ]; then
    if [ $(PackageOnSystem $1) == 1 ]; then
      if [ $(SystemPackageVersion $1) < $(PackageVersion $1) ]; then
        echo "Package exists and can be updated"
      else
        echo "Package exists and is up to date"
      fi
    else
      echo "Package exists and can be downloaded"
    fi
  else
    echo "ERROR: Package does not exists in the Afro Linux packages"
  fi
  exit
elif [ $1 == "add" ]; then
  if [ $(PackageExists) == 1 ]; then
    if [ $(PackageOnSystem $1) == 1 ]; then
      echo "ERROR: Package already installed"
    else
      DownloadPackage $1
    fi
  else
    echo "ERROR: Package does not exist in the Afro Linux packages"
  fi
  exit
elif [ "$1" == "update" ]; then
  if [ $(PackageExists) == 1 ]; then
    UpdatePackage $1
  else
    echo "ERROR: Package does not exist in the Afro Linux packages"
  fi
  exit
elif [ $1 == "version" ]; then
  if [ $(PackageOnExists $1) ]; then
    echo "$1 version: $(SystemPackageVersion $1)"
  else
    echo "ERROR: Package not installed"
  fi
  exit
else
  echo "ERROR: Incorrect arguments"
fi
