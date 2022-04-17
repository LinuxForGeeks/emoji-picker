Emoji Picker
============

An emoji picker for Gnome based Linux desktops.

![screenshot](screenshot.png)

## Installation

The following dependencies are required:
- python3
- python3-gi
- gir1.2-gtk-3.0
- python3-xlib

To install all the dependencies on debian or derivates, run:
```bash
sudo apt install python3 python3-gi gir1.2-gtk-3.0 python3-xlib
```

Next, open a terminal in the 4g-indicator folder & run install script:
```bash
sudo ./install.sh
```

To uninstall run:
```bash
sudo ./uninstall.sh
```

## Update

Simply run the install script in `sudo` mode & all files should be updated.

## Credits

Original work done by [mdebski](https://github.com/mdebski/gtk-emoji-chooser).

## License

Emoji Picker is licensed under the [GPL license](LICENSE).
