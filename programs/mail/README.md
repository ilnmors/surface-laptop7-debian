# Terminal mail (aerc, mbsync, notmuch, msmtp)

Replaces Geary (2026-11-27). Mail is plain Maildir files, so it can be read, searched and tagged from the shell (`notmuch`) as well as in aerc.

| Piece | Role |
| --- | --- |
| mbsync (isync 1.5.1) | Two-way IMAP ⇄ Maildir sync into `~/workspace/mails/<account>/<folder>` (`SL7_MAIL_DIR` in `local/site.env` overrides the path) |
| notmuch 0.39 | Index, tags and search over all accounts (`~/workspace/mails/.notmuch`); maildir flags sync with the `unread`/`flagged` tags |
| aerc 0.20.0 | Terminal client on the Maildir folders; sends with msmtp; HTML parts are shown as text through w3m, and `:open` hands them to Firefox |
| msmtp 1.8.28 | SMTP for aerc, one account per GOA account (`msmtp -a <account>`) |
| `sl7-mail-sync.timer` | systemd user timer: `mbsync --all` then `notmuch new` 1 min after login and every 2 min after the previous run |
| notmuch `post-new` hook | GNOME notification (`notify-send`) for new INBOX mail; up to 3 messages are listed by sender and subject |

## Accounts and credentials

`mail-config.py` reads the mail-enabled accounts of GNOME Online Accounts (Settings → Online Accounts) and writes `~/.config/isyncrc`, `~/.config/msmtp/config`, `~/.config/notmuch/default/config` and `~/.config/aerc/accounts.conf` (all 0600). A Google account is named `google`; an IMAP/SMTP account is named after the first label of its mail domain. The generated files hold no secret: mbsync (`PassCmd`) and msmtp (`passwordeval`) call `goa-mail-secret <account-id> <imap|smtp|token>`, which asks GOA over D-Bus for the keyring password or a fresh Google OAuth2 token. Google logs in with XOAUTH2 through `libsasl2-modules-kdexoauth2` (mbsync) and msmtp's built-in `xoauth2`.

Folders are matched by their IMAP SPECIAL-USE flag, because Gmail names them in the account's display language (for example `[Gmail]/보낸편지함`); servers without the flags fall back to the names `Drafts`, `Sent`, `Trash` and `Archive`. Gmail's `\All`, `\Important` and `\Flagged` folders are not synced: they only repeat mail that is in INBOX or a label folder. Gmail files sent mail itself, so aerc copies sent mail to `Sent` only for the other accounts.

Re-run `python3 programs/mail/mail-config.py` after adding or removing an account; it overwrites the generated files (`aerc.conf` only while it still carries the generated header).

## Setup

`programs/mail/setup.sh` (called by `programs/setup.sh`) installs the packages in `files/packages/` with `dpkg -i` (apt-get refused these local files with "Pathname to install is not absolute"; every dependency outside the base system is in the set), installs `goa-mail-secret` and `sl7-mail-sync` to `~/.local/bin`, writes the configs and the hook, runs the first full sync when no notmuch database exists (without notifications), enables the timer and removes the old Geary autostart entry.

## Use

- `aerc` — read and write; `:check-mail` starts a sync at once.
- `notmuch search tag:unread`, `notmuch show --format=text <thread>`, `notmuch tag +todo -- <query>`.
- `systemctl --user start sl7-mail-sync.service`, `systemctl --user list-timers sl7-mail-sync.timer`.
- msmtp logs every delivery to `~/.cache/msmtp.log`.

## Limits

- No IMAP IDLE: new mail appears within about 2 minutes.
- Only GOA Google and IMAP/SMTP accounts; other providers are skipped with a message.
- Deleting in aerc expunges on the server at the next sync (`Expunge Both`). On Gmail, deleting from INBOX archives the message unless the Gmail IMAP setting says otherwise.
