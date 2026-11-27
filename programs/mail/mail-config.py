#!/usr/bin/python3
"""Write mbsync, msmtp, notmuch and aerc configs for the GNOME Online Accounts mail accounts.

Usage: mail-config.py [MAILDIR]   (default: $SL7_MAIL_DIR or ~/workspace/mails)

Every GOA account with mail enabled becomes one account: Google (OAuth2) is
named `google`, an IMAP/SMTP account is named after the first label of its
mail domain. Configs hold no secret: mbsync and msmtp ask goa-mail-secret at
run time. Run it again after adding or removing an account in Settings →
Online Accounts; it overwrites the generated files.
"""
import base64
import imaplib
import os
import re
import subprocess
import sys
from pathlib import Path

import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio

HOME = Path.home()
CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
SECRET = HOME / ".local/bin/goa-mail-secret"
SYNC = "systemctl --user start sl7-mail-sync.service"
# Gmail exposes every label as a folder; \All, \Important and \Flagged only repeat mail
# held in other folders, so they are not synced. Folders are found by their IMAP
# SPECIAL-USE flag because Gmail names them in the account's display language.
GMAIL_SKIP = ("\\All", "\\Important", "\\Flagged")
ROLES = {"\\Drafts": "drafts", "\\Sent": "sent", "\\Trash": "trash", "\\Archive": "archive"}
LIST_LINE = re.compile(rb'\((?P<flags>[^)]*)\) "(?:[^"]*)" (?P<name>"(?:[^"\\]|\\.)*"|\S+)')


def decode_mailbox(raw):
    """IMAP modified UTF-7 (RFC 3501) to str."""
    name = raw.decode("ascii")
    if name.startswith('"'):
        name = name[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    def part(m):
        chunk = m.group(1).replace(",", "/")
        if not chunk:
            return "&"
        return base64.b64decode(chunk + "=" * (-len(chunk) % 4)).decode("utf-16-be")
    return re.sub(r"&([^-]*)-", part, name)


def special_use(a):
    """Map SPECIAL-USE flags to folder names by asking the server once."""
    secret = subprocess.run([str(SECRET), a["id"], a["secret"][0]], check=True,
                            capture_output=True, text=True).stdout.strip()
    imap = imaplib.IMAP4_SSL(a["imap_host"]) if a["imap_ssl"] else imaplib.IMAP4(a["imap_host"])
    if not a["imap_ssl"]:
        imap.starttls()
    if a["imap_auth"] == "XOAUTH2":
        imap.authenticate("XOAUTH2", lambda _: f"user={a['imap_user']}\x01auth=Bearer {secret}\x01\x01".encode())
    else:
        imap.login(a["imap_user"], secret)
    roles, names = {}, set()
    for line in imap.list()[1]:
        m = LIST_LINE.match(line or b"")
        if m:
            name = decode_mailbox(m.group("name"))
            for flag in m.group("flags").decode().split():
                roles.setdefault(flag, name)
            names.add(name)
    # Servers without SPECIAL-USE flags: fall back to the conventional folder names.
    for flag in ROLES:
        if flag not in roles and flag[1:] in names:
            roles[flag] = flag[1:]
    imap.logout()
    return roles


def accounts():
    bus = Gio.bus_get_sync(Gio.BusType.SESSION)
    manager = Gio.DBusObjectManagerClient.new_sync(
        bus, Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START,
        "org.gnome.OnlineAccounts", "/org/gnome/OnlineAccounts", None, None, None)
    found = []
    for obj in manager.get_objects():
        account, mail = (obj.get_interface(f"org.gnome.OnlineAccounts.{n}") for n in ("Account", "Mail"))
        if not account or not mail or account.get_cached_property("MailDisabled").unpack():
            continue
        prop = lambda name: (v.unpack() if (v := mail.get_cached_property(name)) is not None else None)
        provider = account.get_cached_property("ProviderType").unpack()
        address = prop("EmailAddress")
        entry = {"id": obj.get_object_path().rsplit("/", 1)[1], "address": address,
                 "name": prop("Name") or ""}
        if provider == "google":
            entry.update(key="google", imap_host="imap.gmail.com", imap_user=address, imap_ssl=True,
                         smtp_host="smtp.gmail.com", smtp_user=address, smtp_ssl=False,
                         imap_auth="XOAUTH2", smtp_auth="xoauth2", secret=("token", "token"))
        elif provider == "imap_smtp":
            entry.update(key=address.split("@", 1)[1].split(".", 1)[0],
                         imap_host=prop("ImapHost"), imap_user=prop("ImapUserName"),
                         imap_ssl=prop("ImapUseSsl"), smtp_host=prop("SmtpHost"),
                         smtp_user=prop("SmtpUserName"), smtp_ssl=prop("SmtpUseSsl"),
                         imap_auth="PLAIN LOGIN", smtp_auth="on", secret=("imap", "smtp"))
        else:
            print(f"mail-config: skipping unsupported provider {provider}", file=sys.stderr)
            continue
        roles = special_use(entry)
        entry.update({key: roles.get(flag, "") for flag, key in ROLES.items()})
        entry["skip"] = [roles[f] for f in GMAIL_SKIP if f in roles] if provider == "google" else []
        found.append(entry)
    return sorted(found, key=lambda a: a["key"])


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(text)
    path.chmod(0o600)
    print(f"mail-config: wrote {path}")


def mbsync(accts, maildir):
    out = ["# Generated by mail-config.py; run it again instead of editing.\n"]
    for a in accts:
        k, local = a["key"], maildir / a["key"]
        patterns = " ".join(["*"] + [f'"!{name}"' for name in a["skip"]])
        out.append(f"""IMAPAccount {k}
Host {a['imap_host']}
Port {993 if a['imap_ssl'] else 143}
TLSType {'IMAPS' if a['imap_ssl'] else 'STARTTLS'}
User {a['imap_user']}
AuthMechs {a['imap_auth']}
PassCmd "{SECRET} {a['id']} {a['secret'][0]}"

IMAPStore {k}-remote
Account {k}

MaildirStore {k}-local
Path {local}/
Inbox {local}/INBOX
SubFolders Verbatim

Channel {k}
Far :{k}-remote:
Near :{k}-local:
Patterns {patterns}
Create Near
Expunge Both
CopyArrivalDate yes
SyncState *
""")
    return "\n".join(out)


def msmtp(accts):
    out = ["# Generated by mail-config.py; run it again instead of editing.\n"
           "defaults\ntls on\ntls_trust_file system\nlogfile ~/.cache/msmtp.log\n"]
    for a in accts:
        out.append(f"""account {a['key']}
host {a['smtp_host']}
port {465 if a['smtp_ssl'] else 587}
tls_starttls {'off' if a['smtp_ssl'] else 'on'}
auth {a['smtp_auth']}
user {a['smtp_user']}
from {a['address']}
passwordeval "{SECRET} {a['id']} {a['secret'][1]}"
""")
    return "\n".join(out)


def notmuch(accts, maildir):
    others = ";".join(a["address"] for a in accts[1:])
    return f"""# Generated by mail-config.py; run it again instead of editing.
[database]
path={maildir}

[user]
name={next((a['name'] for a in accts if a['name']), '')}
primary_email={accts[0]['address']}
other_email={others}

[new]
tags=unread;inbox;new
ignore=.mbsyncstate;.mbsyncstate.journal;.mbsyncstate.new;.uidvalidity;.notmuch

[search]
exclude_tags=deleted;spam

[maildir]
synchronize_flags=true
"""


def from_header(a):
    """`Name <address>`, quoting the name when it holds RFC 5322 specials; GOA may give no name
    (Google) or the address itself, and aerc rejects an unquoted `@` in the display name."""
    name = a["name"].strip()
    if not name or name == a["address"]:
        return a["address"]
    if re.search(r'[()<>@,;:\\".\[\]]', name):
        name = '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return f"{name} <{a['address']}>"


def aerc_accounts(accts, maildir):
    out = ["# Generated by mail-config.py; run it again instead of editing.\n"]
    for a in accts:
        copy_to = "" if a["key"] == "google" else a["sent"]  # Gmail files sent mail itself
        out.append(f"""[{a['key']}]
source = maildir://{maildir / a['key']}
outgoing = /usr/bin/msmtp -a {a['key']}
default = INBOX
from = {from_header(a)}
copy-to = {copy_to}
postpone = {a['drafts']}
archive =
check-mail-cmd = {SYNC}
check-mail-timeout = 120s
""")
    return "\n".join(out)


AERC_CONF = """# Generated by mail-config.py; run it again instead of editing.
[ui]
index-columns = date<16,name<20,flags>4,subject<*
timestamp-format = 2006-01-02 15:04
threading-enabled = true
sort = -r date

[viewer]
alternatives = text/plain,text/html

[compose]
address-book-cmd = notmuch address --format=text --output=recipients --deduplicate=address "%s"

[filters]
text/plain = colorize
text/calendar = calendar
message/delivery-status = colorize
message/rfc822 = colorize
text/html = w3m -T text/html -I UTF-8 -O UTF-8 -dump -cols 100 -o display_link_number=1
.headers = colorize

[openers]
text/html = firefox {}
"""


def main():
    maildir = Path(sys.argv[1] if len(sys.argv) > 1 else
                   os.environ.get("SL7_MAIL_DIR", HOME / "workspace/mails")).expanduser()
    accts = accounts()
    if not accts:
        sys.exit("mail-config: no GNOME Online Accounts mail account found")
    maildir.mkdir(parents=True, exist_ok=True, mode=0o700)
    maildir.chmod(0o700)
    for a in accts:
        (maildir / a["key"]).mkdir(exist_ok=True, mode=0o700)
    write(CONFIG / "isyncrc", mbsync(accts, maildir))
    write(CONFIG / "msmtp/config", msmtp(accts))
    write(CONFIG / "notmuch/default/config", notmuch(accts, maildir))
    write(CONFIG / "aerc/accounts.conf", aerc_accounts(accts, maildir))
    aerc_conf = CONFIG / "aerc/aerc.conf"
    if not aerc_conf.exists() or aerc_conf.read_text().startswith("# Generated by mail-config.py"):
        write(aerc_conf, AERC_CONF)
    print("mail-config: accounts " + ", ".join(a["key"] for a in accts))


main()
