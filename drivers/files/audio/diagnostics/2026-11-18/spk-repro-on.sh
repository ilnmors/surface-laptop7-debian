#!/bin/bash
C=/sys/bus/platform/devices/6b10000.soundwire/power/control
sudo_() { secret-tool lookup purpose surface-work-sudo | sudo -S -p '' "$@"; }
trap 'sudo_ sh -c "echo auto > $C"; echo "control restored: $(cat $C)" >> $(dirname "$0")/spk-repro/on400/log.txt' EXIT
mkdir -p $(dirname "$0")/spk-repro/on400
sudo_ sh -c "echo on > $C"; echo "control=$(cat $C) at $(date +%T)" >> $(dirname "$0")/spk-repro/on400/log.txt
bash $(dirname "$0")/spk-repro.sh 400 on400
