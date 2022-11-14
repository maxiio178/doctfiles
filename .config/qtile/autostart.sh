#!/bin/bash

#configuracion teclado
setxbmkey es &

#resolucion
xrandr --output VGA1 --primary --mode 1366x768 --pos 0x0 --rotate normal --output VIRTUAL1 --off

#iconos del sistema

udiskie -t &

nm-applet &

volumeicon &

cbatticon -u 5 &

nitrogen --restore &

picom -b &

