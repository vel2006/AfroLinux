#!/bin/bash
PackageExists()
{
  mkdir .existsTemp
  git clone --single-branch --branch versions https://github.com/vel2006/AfroLinux
  versions=$(cat .existsTemp/AfroLinux/todateVersion)
  if [ $(echo $versions | grep $1) ]; then
    echo 1
  else
    echo 0
  fi
  rm -Rf .existsTemp
}
SystemPackageVersion()
{
  echo $(echo $(cat /etc/AfroLinux/files) | grep $1 | awk '{print $2}')
}
PackageVersion()
{
  mkdir .versionTemp
  git clone --single-branch --branch versions https://github.com/vel2006/AfroLinux
  versions=$(cat .versionTemp/AfroLinux/todateVersion)
  echo $(echo $versions | grep $1 | awk '{print $2}')
}
DownloadPackage()
{
  mkdir .installTemp
  git clone --single-branch --branch $1 https://github.com/vel2006/AfroLinux
  mv .installTemp/$(ls) /etc/AfroLinux
  echo "$1 $(PackageVersion $1)" >> /etc/AfroLinux/files
  rm -Rf .installTemp
}
RemovePackage()
{
  rm /etc/AfroLinux/$1
}
PackageOnSystem()
{
  if [ $(cat /etc/AfroLinux/files | grep $1) ]; then
    echo 1
  else
    echo 0
  fi
}
UpdatePackage()
{
  mkdir .updateTemp
  git clone --single-branch --branch $1 https://github.com/vel2006/AfroLinux
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
}
