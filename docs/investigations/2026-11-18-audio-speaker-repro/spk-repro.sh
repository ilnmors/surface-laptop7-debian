#!/bin/bash
# Speaker silence reproduction: close the speaker PCM, wait, reopen with a short tone, detect it on the internal mic.
# Usage: spk-repro.sh <cycles> <tag>
N=${1:-20}; TAG=${2:-run}
P=$(dirname "$0"); D=$P/spk-repro/$TAG; mkdir -p "$D"; LOG=$D/cycles.tsv
SINK=alsa_output.platform-sound.HiFi__Speaker__sink; SRC=alsa_input.platform-sound.HiFi__Mic__source
SWR=/sys/bus/platform/devices/6b10000.soundwire/power
sudo_() { secret-tool lookup purpose surface-work-sudo | sudo -S -p '' "$@"; }
VOL=$(wpctl get-volume @DEFAULT_AUDIO_SINK@); SPKVOL=$(pactl get-sink-volume $SINK | grep -o '[0-9]*%' | head -1); SPKMUTE=$(pactl get-sink-mute $SINK | awk '{print $2}')
restore() { pactl set-sink-volume $SINK "$SPKVOL"; pactl set-sink-mute $SINK "$SPKMUTE"; pactl suspend-sink $SINK 0; echo "restored vol=$SPKVOL mute=$SPKMUTE" >> $D/log.txt; }
trap restore EXIT
pactl set-sink-mute $SINK 0; pactl set-sink-volume $SINK 25%
python3 -I - "$P/tone1500.wav" <<'EOF'
import wave,struct,math,sys
w=wave.open(sys.argv[1],'w');w.setnchannels(2);w.setsampwidth(2);w.setframerate(48000)
n=int(48000*0.8)
w.writeframes(b''.join(struct.pack('<hh',*(int(12000*math.sin(2*math.pi*1500*i/48000)*min(1,i/480,(n-i)/480)),)*2) for i in range(n)))
EOF
cat > "$P/detect.py" <<'EOF'
import wave,struct,math,sys
w=wave.open(sys.argv[1]);r=w.getframerate();ch=w.getnchannels();raw=w.readframes(w.getnframes())
s=struct.unpack('<%dh'%(len(raw)//2),raw)[::ch]
def g(seg,f):
    k=2*math.cos(2*math.pi*f/r);a=b=0
    for x in seg: a,b=x+k*a-b,a
    return math.sqrt(max(a*a+b*b-k*a*b,0))/max(len(seg),1)
win=int(r*0.1); best=0; ref=0
for i in range(0,max(len(s)-win,1),win):
    seg=s[i:i+win]; t=g(seg,1500); n=(g(seg,1100)+g(seg,1900))/2
    if t>best: best,ref=t,n
print(f"{best:.1f} {ref:.1f} {best/max(ref,0.01):.1f}")
EOF
printf 'cycle\ttime\twait_s\tswr_before\ttone\tnoise\tratio\tresult\n' > $LOG
for c in $(seq 1 $N); do
  W=$(( (c % 4 == 0) ? 1 : (3 + RANDOM % 8) ))   # mostly 3-10 s (controller autosuspend is 3 s), every 4th 1 s
  pactl suspend-sink $SINK 1; sleep $W
  st=$(cat $SWR/runtime_status)
  pw-record --target $SRC --rate 48000 --channels 1 "$D/rec.wav" & R=$!; sleep 0.3
  pactl suspend-sink $SINK 0; pw-play --target $SINK "$P/tone1500.wav"; sleep 0.3; kill $R; wait $R 2>/dev/null
  read tone noise ratio < <(python3 -I "$P/detect.py" "$D/rec.wav")
  res=OK; awk -v r="$ratio" 'BEGIN{exit !(r<8)}' && res=SILENT
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' $c "$(date +%T)" $W "$st" "$tone" "$noise" "$ratio" $res >> $LOG
  if [ $res = SILENT ]; then
    cp "$D/rec.wav" "$D/silent-$c.wav"
    { date; for d in /sys/bus/platform/devices/*.soundwire /sys/bus/soundwire/devices/*; do echo "$(basename $d) $(cat $d/power/runtime_status 2>/dev/null)"; done; head -5 /proc/asound/card0/pcm1p/sub0/status; sudo_ journalctl -k --since -2min --no-pager | grep -iE 'swr|soundwire|wsa|clsh|apm|q6|lpass' | tail -20; } > "$D/silent-$c.txt" 2>&1
  fi
done
echo "done $(date +%T)" >> $D/log.txt
