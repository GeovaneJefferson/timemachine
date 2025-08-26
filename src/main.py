import os

from server import *
from ui import BackupWindow


class BackupApp(Adw.Application):   
    def __init__(self):
        super().__init__(application_id=server.ID,
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
    def do_activate(self):
        # Load CSS
        provider = Gtk.CssProvider()
        css_file = os.path.join(os.path.dirname(__file__), "style.css")
        provider.load_from_path(css_file)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        win = BackupWindow(application=self)
        win.present()


def main():
    app = BackupApp()
    return app.run(sys.argv)
    

if __name__ == "__main__":
    server = SERVER()  # <-- Instantiate first!
    main()

