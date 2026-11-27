#!/usr/bin/python3
"""Write mbsync, msmtp, notmuch and Alpine configs for the GNOME Online Accounts mail accounts.

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
ignore=.mbsyncstate;.mbsyncstate.journal;.mbsyncstate.new;.mbsyncstate.lock;.uidvalidity;/(^|[/])[.]uid(last|temp)/;.notmuch

[search]
exclude_tags=deleted;spam

[maildir]
synchronize_flags=true
"""


def from_header(a):
    """`Name <address>`, quoting the name when it holds RFC 5322 specials; GOA may give no name
    (Google) or the address itself, and an unquoted `@` in a display name is not a valid address."""
    name = a["name"].strip()
    if not name or name == a["address"]:
        return a["address"]
    if re.search(r'[()<>@,;:\\".\[\]]', name):
        name = '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return f"{name} <{a['address']}>"


def md(maildir, *parts):
    """Alpine Maildir folder name: `#md/` plus a path under the home directory, or an absolute path."""
    path = maildir.joinpath(*parts)
    try:
        return "#md/" + str(path.relative_to(HOME))
    except ValueError:
        return "#md/" + str(path)


def pat(value):
    """Escape a value inside an Alpine rule (pattern/action) string."""
    return value.replace("\\", "\\\\").replace("/", "\\/").replace('"', '\\"')


def pinerc_values(accts, maildir):
    """The Alpine settings this script owns; everything else in ~/.pinerc stays as the user set it."""
    first = accts[0]
    roles = []
    for a in accts:
        action = f"/ROLE=1/FROM={pat(from_header(a))}"
        if a["key"] != "google" and a["sent"]:  # Gmail files sent mail itself
            action += "/FCC=" + pat(md(maildir, a["key"], a["sent"]))
        action += "/RTYPE=NC/FTYPE=NC/CTYPE=YES"
        roles.append(f'LIT:pattern="/NICK={pat(a["key"])}/TO={pat(a["address"])}" action="{action}"')
    return {
        "personal-name": next((a["name"] for a in accts if a["name"]), ""),
        "customized-hdrs": [f"From: {from_header(first)}"],
        "maildir-location": str(maildir.joinpath(first["key"], "INBOX").relative_to(HOME))
        if maildir.is_relative_to(HOME) else str(maildir / first["key"] / "INBOX"),
        "inbox-path": md(maildir, first["key"], "INBOX"),
        "incoming-folders": [f'{a["key"]} {md(maildir, a["key"], "INBOX")}' for a in accts[1:]],
        "folder-collections": [f'{a["key"]} {md(maildir, a["key"])}/[]' for a in accts],
        "default-fcc": '""' if first["key"] == "google" or not first["sent"] else md(maildir, first["key"], first["sent"]),
        "postponed-folder": md(maildir, first["key"], first["drafts"] or "Drafts"),
        "sendmail-path": "/usr/bin/msmtp --read-envelope-from -t",
        "url-viewers": ["/usr/bin/firefox"],
        "feature-list": ["enable-incoming-folders", "enable-incoming-folders-checking",
                         "enable-multiple-newmail-in-status", "quell-user-lookup-in-passwd-file"],
        "patterns-roles": roles,
    }


def pinerc(path, values):
    """Set the owned variables in an existing ~/.pinerc (a value may continue on indented lines)."""
    lines = path.read_text().splitlines() if path.exists() else [
        "# Alpine configuration. mail-config.py sets the mail account variables it owns; Alpine keeps the rest."]
    def render(key, value):
        if isinstance(value, list):
            if not value:
                return [f"{key}="]
            return [f"{key}={value[0]}" + ("," if len(value) > 1 else "")] + [
                "\t" + v + ("," if i < len(value) - 1 else "") for i, v in enumerate(value[1:], 1)]
        return [f"{key}={value}"]
    out, i, seen = [], 0, set()
    while i < len(lines):
        key = lines[i].split("=", 1)[0] if "=" in lines[i] and not lines[i][:1].isspace() and not lines[i].startswith("#") else None
        j = i + 1
        while j < len(lines) and lines[j][:1] in (" ", "\t"):
            j += 1
        if key in values:
            out += render(key, values[key]); seen.add(key)
        else:
            out += lines[i:j]
        i = j
    for key, value in values.items():
        if key not in seen:
            out += render(key, value)
    write(path, "\n".join(out) + "\n")


MAILCAP = """# Generated by mail-config.py: Alpine opens HTML parts and links in Firefox.
text/html; /usr/bin/firefox %s; nametemplate=%s.html; test=test -n "$DISPLAY$WAYLAND_DISPLAY"
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
    pinerc(HOME / ".pinerc", pinerc_values(accts, maildir))
    mailcap = HOME / ".mailcap"
    if not mailcap.exists() or mailcap.read_text().startswith("# Generated by mail-config.py"):
        write(mailcap, MAILCAP)
    print("mail-config: accounts " + ", ".join(a["key"] for a in accts))


main()
