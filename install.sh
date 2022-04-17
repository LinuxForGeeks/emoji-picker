#!/bin/bash

if [ "$(id -u)" != "0" ]; then
echo “This script must be run as root” 2>&1
exit 1
fi

sh uninstall.sh

cp *.py /usr/share/gtk-emoji-picker/
chmod 755 -R /usr/share/gtk-emoji-picker/

cp gtk-emoji-picker.desktop /usr/share/applications/
chmod 755 /usr/share/applications/gtk-emoji-picker.desktop

ln -s /usr/share/gtk-emoji-picker/gtk-emoji-picker.py /usr/local/bin/gtk-emoji-picker
chmod 755 /usr/local/bin/gtk-emoji-picker
