#!/bin/ash
print_heading1() {
  printf "${COLCYAN}%s${COLRSET}\n" "$1"
}
print_heading2() {
  printf "${COLWHITE}%s${COLORSET}\n" "$1"
}
print_heading1 " Starting upgrade to Afro Linux "
print_heading1 "--------------------------------"
echo ""
sleep 3
print_heading2 "Installing packages & base files "
print_heading2 "---------------------------------"
sleep 1
apk update
apk upgrade
apk add iproute2
apk add net-tools
apk add python3
apk add gcc
apk add g++
apk add openjdk11
apk add dotnet6-sdk
apk add htop
apk add ufw
apk add mousepad
apk add libreoffice
apk add gimp
apk add claws-mail
apk add xdg-utils
mkdir .temp
rm -Rf /usr/share/backgrounds/xfce
cp AfroLinux/solo.png /usr/share/backgrounds/xfce
cp AfroLinux/textOnly.png /usr/share/backgrounds/xfce
echo ""
print_heading2 " Installing GRUB boot-loader "
print_heading2 "-----------------------------"
sleep 1
apk add grub brub-bios grub-efi efibootmgr
cp .temp/images/bootLoader.png /boot/grub/bootLoader.png
echo 'GRUB_DISTRIBUTOR="Afro Linux"' > /etc/default/grub
echo 'GRUB_CMDLINE_LINUX_DEFAULT="quier splash logo.nologo"' >> /etc/default/grub
echo 'GRUB_BACKGROUND=/boot/grub/bootLoader.png' >> /etc/default/grub
echo 'GRUB_TIMEOUT=5' >> /etc/default/grub
echo 'GRUB_DISABLE_SUBMENU=true' >> /etc/default/grub
echo 'GRUB_DISABLE_RECOVERY=true' >> /etc/default/grub
rm -Rf .temp
echo ""
print_heading2 " Installing afro.sh for Afro Linux "
print_heading2 "-----------------------------------"
sleep 1
mkdir .temp
git clone --single-branch afro https://github.com/vel2006/AfroLinux
chmod +x .temp/afro.sh
mkdir /etc/AfroLinux
cp .temp/afro.sh /etc/AfroLinux/
touch /etc/AfroLinux/files
rm -Rf .temp
echo ""
print_heading1 " If no errors happened, the system should be converted to Afro Linux, a fork of Alpine Linux "
print_heading1 "---------------------------------------------------------------------------------------------"
print_heading2 " Thanks to these two goobers for being my test dummys:"
print_heading2 "    1) BorderDestroyer "
print_heading2 "        links:"
print_heading2 "            <https://www.youtube.com/@BorderDestroyer>" 
print_heading2 "            <https://www.twitch.tv/borderdestroyer1>"
print_heading2 "    2) Russian Spy"
print_heading2 "        links:"
print_heading2 "            <https://www.youtube.com/@therussianspy0725>"
print_heading2 "            <https://www.twitch.tv/the_russian_spy07>"
