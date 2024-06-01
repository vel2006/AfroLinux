# AfroLinux
Hello user, Afro linux is basically an expantion for Alpine Linux Standard version 3.20 x86_64. The base disk size is ~40GB and will need a minimum of 4BG of ram to use (still smaller than windows on all fronts >:3). All information I have documentated about it is below under the title of that section.

## Installation
To get Afro Linux, you need to have standard Alpine Linux version 3.20 for x84_64 on a bootable drive. Once booted into Alpine Linux, simply follow the prompts when using the command 'setup-alpine', then reboot and remove the drive, then use 'setup-desktop xfce' and reboot when done. Finnaly, log into the root account (or account with perms) and use the following commands: 'apk add git' 'git clone https://github.com/vel2006/AfroLinux' 'chmod +x AfroLinux/intoAfro.sh' './AfroLinux/intoAfro.sh'

## Added features
Afro Linux adds several packages to Alpine Linux, which make it more usable as a daily choice. 

### If you wish to get your own tool(s) added to this project, check the wiki page for information

Below are all of the packages added in 1.0:
1) UFW firewall
2) Networking tools:
   iproute2
   net-tools
3) Programing langues:
   python3
   gcc         [C]
   g++         [C++]
   dotnet6-sdk [C#]
   openjdk     [Java]
4) Mousepad
5) Libre Office Suite
6) Claws Mail
7) htop
8) Desktop environment:
   XFCE
   xdg-utils
   Custom walpapers in /usr/share/walpapers/xfce
9) Boot:
   GRUB (BIOS, and efi versions)
   efibootmgr
   Custom splash-screen
10) Custom:
    Afro.sh [Custom package manager for this github's branches held in /etc/AfroLinux]

## Special thanks to the Testers of this horrid software:
1) BorderDestroyer <https://www.youtube.com/@BorderDestroyer> <https://www.twitch.tv/borderdestroyer1>
2) Russian Spy     <<https://www.youtube.com/@therussianspy0725> <https://www.twitch.tv/the_russian_spy07>
