#!/bin/bash

WUKONGPATH=/tmp/wukong-darjeeling
XMLPATH=$WUKONGPATH/wukong/ComponentDefinitions
UDPPATH=$WUKONGPATH/wukong/gateway/udpwkpf
NATIVEPATH=$WUKONGPATH/src/lib/wkpf/c/arduino.wudevice/native_wuclasses
read -p "This will replace files in your Wukong repository (Y/N): " confirm

if [[ "$confirm" -ne "Y" ]]; then
  echo "Not copy"
  exit 0
fi

if [[ ! -d $XMLPATH ]]; then
  echo "Directory ComponentDefinitions not exist"
  exit 1
fi

if [[ ! -d $UDPPATH ]]; then
  echo "Directory udpwkpf not exist"
  exit 1
fi

if [[ ! -d $NATIVEPATH ]]; then
  echo "Directory native_wuclasses not exist"
  exit 1
fi

cp -v ComponentDefinitions/* $XMLPATH/
cp -v udpdevice/* $XMLPATH/
cp -v native_wuclasses/* $XMLPATH/

