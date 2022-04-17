#!/bin/bash

if [ "$(id -u)" != "0" ]; then
echo “This script must be run as root” 2>&1
exit 1
fi

rm -rf /usr/share/gtk-emoji-picker
rm -f /usr/share/applications/gtk-emoji-picker.desktop
rm -f /etc/xdg/autostart/gtk-emoji-picker.desktop
rm -f /usr/local/bin/gtk-emoji-picker
