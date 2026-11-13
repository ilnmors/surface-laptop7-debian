# Alpine Lake / Fluent Teal Light

- Photo: Luca Bravo, **Boathouse on a mountain lake**, Lago di Braies. [Original](https://unsplash.com/photos/brown-house-near-body-of-water-zAjdgNXsMeg), [Unsplash License](https://unsplash.com/license).
- Offline image: `desktop/files/backgrounds/alpine-lake-luca-bravo.jpg`, 3200×2134 JPEG, close to the Surface 3:2 display ratio. Provider resize only; no local color edits or crop. Exact URL and SHA256: `alpine-theme.json`.
- Theme: `Fluent-teal-Light`, built from the existing archived Fluent source. GTK3 and GTK4 use the upstream teal accent (#009688). The new Shell variant was tried, then the previous Fluent-Light Shell and Open Bar colors were restored after the user reported an abnormal panel. GNOME's native accent is green, matching the forest/lake palette.
- Open Bar: use a continuous opaque 34px light Mainland panel, with CPU/RAM on the left and clock centered. The existing fixed bottom taskbar uses a matching pale green background and teal running indicators. Papirus icons and the terminal content palette are retained.

## Apply offline

Run `python3 setup.py --component desktop` or `bash desktop/setup.sh` through the bundle's documented entry point. The compiled theme is already included; installation does not rebuild it or fetch the image. The downloaded photo and build-tool DEBs are local offline payloads, excluded from Git; copy them with the complete bundle.

The live change required no administrator password: the photo is at `~/.local/share/backgrounds/`, and the theme is under `~/.themes/`. The full desktop installer puts the same photo under `/usr/share/backgrounds/` and restores the portable preset pointing there. This path difference does not change the image.

GTK4 is linked to `~/.themes/Fluent-teal-Light/gtk-4.0` when the existing config is managed by this bundle. A separate user-created GTK4 config directory is preserved. Existing GTK4 applications can require reopening to reread custom CSS; no session logout is required.

## Rebuild the exact theme

Extract `archive/desktop/fluent-source.tar.gz` into a temporary user-owned build directory. Extract `desktop/files/topbar/build-tools/{sassc,libsass1}_*_arm64.deb` there with `dpkg-deb -x`, and prepend the extracted `usr/bin` to PATH and `usr/lib/aarch64-linux-gnu` to LD_LIBRARY_PATH for this build only. Run the original `install.sh -d OUTPUT -t teal -c light -s standard`. Keep `COPYING` with the generated theme and append the maintained `desktop/files/dock/dock.css` to its `gnome-shell/gnome-shell.css`. Installed files are copied unchanged from this output, except for that documented dock CSS addition. Build tools add no resident service and are not needed to use the compiled theme.

## Validation and rollback

GTK3, GTK4 and Shell CSS all contain #009688; the previous blue accent is absent from those generated files. The live photo hash matches the offline photo, and the GTK4 symlink targets the new theme. The screen was locked during the final application, so Shell extensions were inactive for the lock-screen session; they are enabled and pick up the new settings on unlock. Final visual confirmation is pending.

Targeted rollback: `archive/alpine-theme-before-*/restore.sh`. It restores the prior wallpaper, selected GTK/Shell theme, panel/dock colors and previous managed GTK4 symlink. Earlier theme folders and wallpaper files remain available.

## Panel recovery

The newly generated Shell theme lacked the existing Surface panel CSS additions. This is a possible contributor, not a confirmed visual diagnosis. The active Shell is restored to the previously used `Fluent-Light`; Open Bar colors are restored from the pre-theme backup and the extension was fully disabled/enabled without logout. GTK3/GTK4, wallpaper and dock settings remain from the alpine palette. Open Bar, User Themes and Vitals report ACTIVE after restoration. User confirmation of the appearance is still pending. The desktop installer now selects the same restored Shell theme.
