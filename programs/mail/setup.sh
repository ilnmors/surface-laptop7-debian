#!/bin/bash
# Terminal mail: mbsync + notmuch + aerc + msmtp; accounts and credentials come from GNOME Online Accounts.
set -euo pipefail
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bundle=$(CDPATH= cd -- "$here/../.." && pwd)
if [[ -r $bundle/local/site.env ]]; then source "$bundle/local/site.env"; fi
mail_dir=${SL7_MAIL_DIR:-$HOME/workspace/mails}

# apt-get refused these local files ("Pathname to install is not absolute", 2026-11-27); every
# dependency outside the base system is in the set, so dpkg installs them directly.
missing=()
for deb in "$here"/files/packages/*.deb; do
  read -r pkg ver < <(dpkg-deb --show --showformat='${Package} ${Version}\n' "$deb")
  [[ $(dpkg-query -W -f='${db:Status-Status} ${Version}' "$pkg" 2>/dev/null) == "installed $ver" ]] || missing+=("$deb")
done
if (( ${#missing[@]} )); then sudo dpkg -i "${missing[@]}"; fi

install -D -m 755 "$here/goa-mail-secret.py" "$HOME/.local/bin/goa-mail-secret"
install -D -m 755 "$here/files/sl7-mail-sync" "$HOME/.local/bin/sl7-mail-sync"
install -D -m 644 -t "$HOME/.config/systemd/user" "$here"/files/systemd/*
python3 "$here/mail-config.py" "$mail_dir"
install -D -m 755 "$here/files/post-new" "$HOME/.config/notmuch/default/hooks/post-new"

if [[ ! -d $mail_dir/.notmuch ]]; then
  echo "mail: first full sync into $mail_dir (this can take a while)"
  mbsync --all || echo 'mail: first sync incomplete; the timer continues it.' >&2
  SL7_MAIL_QUIET=1 notmuch new
fi
systemctl --user daemon-reload
systemctl --user enable --now sl7-mail-sync.timer
# Geary was the previous client; its autostart entry would only fail now.
rm -f "$HOME/.config/autostart/geary-autostart.desktop"
