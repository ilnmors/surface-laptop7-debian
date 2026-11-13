import GObject from 'gi://GObject';
import Gio from 'gi://Gio';
import St from 'gi://St';
import Clutter from 'gi://Clutter';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

// Same counting rule as the shell's own MessagesIndicator (ui/dateMenu.js):
// unseen notifications of every source minus the ones still queued as banners.
const NotificationButton = GObject.registerClass(
class NotificationButton extends PanelMenu.Button {
    _init() {
        super._init(0.5, 'Notifications', true);
        this.accessible_name = 'Notifications';

        const box = new St.BoxLayout({style_class: 'surface-notifications-box'});
        this._icon = new St.Icon({style_class: 'system-status-icon'});
        this._badge = new St.Label({
            style_class: 'surface-notifications-badge',
            y_align: Clutter.ActorAlign.CENTER,
            visible: false,
        });
        box.add_child(this._icon);
        box.add_child(this._badge);
        this.add_child(box);

        this._sourceSignals = new Map();
        this._settings = new Gio.Settings({schema_id: 'org.gnome.desktop.notifications'});
        this._settingsId = this._settings.connect('changed::show-banners', () => this._sync());

        const tray = Main.messageTray;
        this._trayIds = [
            tray.connect('source-added', (_t, source) => this._addSource(source)),
            tray.connect('source-removed', (_t, source) => this._removeSource(source)),
            tray.connect('queue-changed', () => this._sync()),
        ];
        tray.getSources().forEach(source => this._addSource(source));
        this._sync();
    }

    _addSource(source) {
        if (this._sourceSignals.has(source))
            return;
        this._sourceSignals.set(source, source.connect('notify::count', () => this._sync()));
        this._sync();
    }

    _removeSource(source) {
        const id = this._sourceSignals.get(source);
        if (id !== undefined)
            source.disconnect(id);
        this._sourceSignals.delete(source);
        this._sync();
    }

    _sync() {
        let count = 0;
        for (const source of this._sourceSignals.keys())
            count += source.unseenCount;
        count = Math.max(0, count - Main.messageTray.queueCount);

        const dnd = !this._settings.get_boolean('show-banners');
        this._icon.icon_name = dnd
            ? 'notifications-disabled-symbolic'
            : 'preferences-system-notifications-symbolic';
        this._badge.text = count > 99 ? '99+' : String(count);
        this._badge.visible = count > 0;
    }

    vfunc_event(event) {
        const type = event.type();
        if (type === Clutter.EventType.BUTTON_PRESS || type === Clutter.EventType.TOUCH_BEGIN) {
            Main.panel.statusArea.dateMenu?.menu.toggle();
            return Clutter.EVENT_STOP;
        }
        return Clutter.EVENT_PROPAGATE;
    }

    destroy() {
        for (const [source, id] of this._sourceSignals)
            source.disconnect(id);
        this._sourceSignals.clear();
        this._trayIds.forEach(id => Main.messageTray.disconnect(id));
        this._trayIds = [];
        this._settings.disconnect(this._settingsId);
        this._settings = null;
        super.destroy();
    }
});

export default class SurfaceNotificationsExtension extends Extension {
    enable() {
        this._button = new NotificationButton();
        // Leftmost slot of the right box, just before the system indicators.
        Main.panel.addToStatusArea(this.uuid, this._button, 0, 'right');
    }

    disable() {
        this._button?.destroy();
        this._button = null;
    }
}
