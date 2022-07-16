
BUILD_DIR ?= ./build

.PHONY: all clean build

all: build clean

clean:
	rm -rf ${BUILD_DIR}/python3-10.AppImage
	rm -rf ${BUILD_DIR}/squashfs-root
	rm -rf ${BUILD_DIR}/appimagetool-*.AppImage

build:
	mkdir -p ${BUILD_DIR}
	wget -O ${BUILD_DIR}/python3-10.AppImage "https://github.com/niess/python-appimage/releases/download/python3.10/python3.10.5-cp310-cp310-manylinux2014_x86_64.AppImage"
	chmod +x ${BUILD_DIR}/python3-10.AppImage
	cd ${BUILD_DIR} && ./python3-10.AppImage --appimage-extract
	${BUILD_DIR}/squashfs-root/AppRun -m pip install -r requirements.txt
	cd ${BUILD_DIR} && wget -c https://github.com/$$(wget -q https://github.com/probonopd/go-appimage/releases -O - | grep "appimagetool-.*-x86_64.AppImage" | head -n 1 | cut -d '"' -f 2)
	chmod +x ${BUILD_DIR}/appimagetool-*.AppImage
	rm ${BUILD_DIR}/squashfs-root/*.desktop
	cp Game.desktop ${BUILD_DIR}/squashfs-root/
	cp assets/favicon.png ${BUILD_DIR}/squashfs-root/game.png
	cp game.sh ${BUILD_DIR}/squashfs-root/AppRun
	chmod +x ${BUILD_DIR}/squashfs-root/AppRun
	mkdir -p ${BUILD_DIR}/squashfs-root/opt/Game/
	cd ${BUILD_DIR}/squashfs-root/opt/Game/ && mkdir assets data entities json_utils Sounds utils
	cp -r assets/* ${BUILD_DIR}/squashfs-root/opt/Game/assets/
	cp -r data/* ${BUILD_DIR}/squashfs-root/opt/Game/data/
	cp -r entities/* ${BUILD_DIR}/squashfs-root/opt/Game/entities/
	cp -r json_utils/* ${BUILD_DIR}/squashfs-root/opt/Game/json_utils/
	cp -r Sounds/* ${BUILD_DIR}/squashfs-root/opt/Game/Sounds/
	cp -r utils/* ${BUILD_DIR}/squashfs-root/opt/Game/utils/
	cp level_0.dat ${BUILD_DIR}/squashfs-root/opt/Game/
	cp main.py ${BUILD_DIR}/squashfs-root/opt/Game/
	cp menu.py ${BUILD_DIR}/squashfs-root/opt/Game/
	cp sample_level.dat ${BUILD_DIR}/squashfs-root/opt/Game/
	cp settings.py ${BUILD_DIR}/squashfs-root/opt/Game/
	chmod 0755 ${BUILD_DIR}/squashfs-root/
	cd ${BUILD_DIR} && VERSION=1.0.0 ./appimagetool-*-x86_64.AppImage squashfs-root/

