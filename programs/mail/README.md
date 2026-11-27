# Terminal mail (Alpine, mbsync, notmuch, msmtp)

Replaces Geary (2026-11-27; aerc was the first client and was replaced by Alpine the same day). Mail is plain Maildir files, so it can be read, searched and tagged from the shell (`notmuch`) as well as in Alpine.

| Piece | Role |
| --- | --- |
| mbsync (isync 1.5.1) | Two-way IMAP ⇄ Maildir sync into `~/workspace/mails/<account>/<folder>` (`SL7_MAIL_DIR` in `local/site.env` overrides the path) |
| notmuch 0.39 | Index, tags and search over all accounts (`~/workspace/mails/.notmuch`); maildir flags sync with the `unread`/`flagged` tags |
| Alpine 2.26 (`2.26+dfsg-3+maildir1`, local build) | Terminal client on the Maildir folders (`#md/` paths); sends with `msmtp --read-envelope-from -t`, which picks the account from the From address; renders HTML parts as text, and opens them or links in Firefox (`~/.mailcap`, `url-viewers`) |
| msmtp 1.8.28 | SMTP for Alpine, one account per GOA account |
| `sl7-mail-sync.timer` | systemd user timer: `mbsync --all` then `notmuch new` 1 min after login and every 2 min after the previous run |
| notmuch `post-new` hook | GNOME notification (`notify-send`) for new INBOX mail; up to 3 messages are listed by sender and subject |

## Accounts and credentials

`mail-config.py` reads the mail-enabled accounts of GNOME Online Accounts (Settings → Online Accounts) and writes `~/.config/isyncrc`, `~/.config/msmtp/config`, `~/.config/notmuch/default/config` (all 0600) and the account variables of `~/.pinerc`. A Google account is named `google`; an IMAP/SMTP account is named after the first label of its mail domain. The generated files hold no secret: mbsync (`PassCmd`) and msmtp (`passwordeval`) call `goa-mail-secret <account-id> <imap|smtp|token>`, which asks GOA over D-Bus for the keyring password or a fresh Google OAuth2 token. Google logs in with XOAUTH2 through `libsasl2-modules-kdexoauth2` (mbsync) and msmtp's built-in `xoauth2`.

Folders are matched by their IMAP SPECIAL-USE flag, because Gmail names them in the account's display language (for example `[Gmail]/보낸편지함`); servers without the flags fall back to the names `Drafts`, `Sent`, `Trash` and `Archive`. Gmail's `\All`, `\Important` and `\Flagged` folders are not synced: they only repeat mail that is in INBOX or a label folder. Gmail files sent mail itself, so Alpine saves a copy (Fcc) only for the other accounts.

Re-run `python3 programs/mail/mail-config.py` after adding or removing an account; it overwrites the generated files. In `~/.pinerc` it sets only the variables it owns (`personal-name`, `customized-hdrs`, `maildir-location`, `inbox-path`, `incoming-folders`, `folder-collections`, `default-fcc`, `postponed-folder`, `sendmail-path`, `url-viewers`, `feature-list`, `patterns-roles`); every other Alpine setting stays as set in Alpine. `~/.mailcap` is written only while it still carries the generated header.

## Setup

`programs/mail/setup.sh` (called by `programs/setup.sh`) installs the packages in `files/packages/` with `dpkg -i` (apt-get refused these local files with "Pathname to install is not absolute"; every dependency outside the base system is in the set), installs `goa-mail-secret` and `sl7-mail-sync` to `~/.local/bin`, writes the configs and the hook, runs the first full sync when no notmuch database exists (without notifications), enables the timer, puts `alpine` on hold, and removes the old Geary autostart entry.

## Alpine with Maildir

Debian builds Alpine without Maildir support. `files/alpine-maildir/` keeps the Debian trixie source (`alpine_2.26+dfsg-3`: `.dsc`, `.orig.tar.xz`, `.debian.tar.xz`, SHA-256 checked against the Sources index that APT verified), Eduardo Chappa's patch as downloaded (`maildir.patch.gz`, from https://alpineapp.email/alpine/patches/alpine-2.26/maildir.patch.gz) and the same patch in unified form for `debian/patches` (`maildir.patch`). `build.sh` rebuilds `alpine_2.26+dfsg-3+maildir1_arm64.deb` into `files/packages/`. The driver adds its own `,u=<uid>` tag to file names and `.uidlast`/`.uidtemp` files next to `cur/`; mbsync keeps finding messages by its `,U=` tag and ignores the extra files, and notmuch ignores them (tested 2026-11-27: 1928 INBOX files renamed by Alpine, the next sync succeeded with no duplicate or loss).

## Use

- `alpine` — read and write. The first account's INBOX opens first; the other INBOX is under Incoming Message Folders, and every folder is under the account's collection (`L`). Replies take the From address and Fcc of the account the message was sent to (one role per account, matched on To); a new message asks which account to use.
- `notmuch search tag:unread`, `notmuch show --format=text <thread>`, `notmuch tag +todo -- <query>`.
- `systemctl --user start sl7-mail-sync.service`, `systemctl --user list-timers sl7-mail-sync.timer`.
- msmtp logs every delivery to `~/.cache/msmtp.log`.

## Limits

- No IMAP IDLE: new mail appears within about 2 minutes.
- Only GOA Google and IMAP/SMTP accounts; other providers are skipped with a message.
- Deleting and expunging in Alpine removes the message on the server at the next sync (`Expunge Both`). On Gmail, deleting from INBOX archives the message unless the Gmail IMAP setting says otherwise.
