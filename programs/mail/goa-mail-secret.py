#!/usr/bin/python3
"""Print a mail credential held by GNOME Online Accounts on stdout.

Usage: goa-mail-secret <account-id> <imap|smtp|token>

mbsync (PassCmd) and msmtp (passwordeval) call this at run time, so no
password or token is ever written to a file. `token` asks an OAuth2 account
(Google) for a fresh access token; `imap` and `smtp` read the password of an
IMAP/SMTP account from the keyring through GOA.
"""
import sys

import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

BUS = "org.gnome.OnlineAccounts"
KINDS = {
    "token": ("OAuth2Based", "GetAccessToken", None),
    "imap": ("PasswordBased", "GetPassword", "imap-password"),
    "smtp": ("PasswordBased", "GetPassword", "smtp-password"),
}


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in KINDS:
        sys.exit(__doc__.strip().splitlines()[2])
    account, kind = sys.argv[1], sys.argv[2]
    interface, method, secret_id = KINDS[kind]
    args = GLib.Variant("(s)", (secret_id,)) if secret_id else None
    bus = Gio.bus_get_sync(Gio.BusType.SESSION)
    try:
        reply = bus.call_sync(BUS, f"/org/gnome/OnlineAccounts/Accounts/{account}",
                              f"{BUS}.{interface}", method, args, None,
                              Gio.DBusCallFlags.NONE, 30000, None)
    except GLib.Error as error:
        sys.exit(f"goa-mail-secret: {account} {kind}: {error.message}")
    print(reply.unpack()[0])


main()
