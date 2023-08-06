#!/bin/bash
cd $1
ln -s ~/.local/share/famcy/$2/console/ _CONSOLE_FOLDER_

cd static
ln -s ~/.local/share/famcy/$2/console/_static_/user_css/ user_css
ln -s ~/.local/share/famcy/$2/console/_static_/user_js/ user_js
ln -s ~/.local/share/famcy/$2/console/_static_/user_image/ user_image