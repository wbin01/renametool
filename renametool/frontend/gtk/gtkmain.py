import sys
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import backend.title as title
import backend.utils.file as file
import frontend.gtk.header as header
import frontend.gtk.preview as preview
import frontend.gtk.base as base


class MyWindow(Gtk.Window):
    def __init__(self, list_files: list = list):
        Gtk.Window.__init__(
            self, window_position=Gtk.WindowPosition.CENTER,
            icon_name='document-edit-symbolic')
        self.status_error = None
        self.list_files = list_files
        self.markup_template = {
            '[1, 2, 3]': '[1, 2, 3]',
            '[01, 02, 03]': '[01, 02, 03]',
            '[001, 002, 003]': '[001, 002, 003]',
            '[original-name]': '[Original filename]'
        }

        # Window title
        title_obj = title.Title(self.list_files)
        self.set_title(title_obj.get_title())

        # Main box
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        # Header
        self.header = header.StackHeader(markup_template=self.markup_template)
        self.main_box.pack_start(self.header, True, True, 0)

        # Preview
        self.preview = preview.Preview(
            header=self.header, markup_template=self.markup_template, list_files=self.list_files)
        self.main_box.pack_start(self.preview, True, True, 0)

        self.base = base.Base(preview=self.preview, list_files=self.list_files)
        self.main_box.pack_start(self.base, True, True, 0)

        # Focus
        self.activate_focus()
        self.set_focus(self.header.tab_rename.entry)


if __name__ == '__main__':
    del (sys.argv[0])
    ls = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    l_files = list(file.File(x) for x in sys.argv)

    win = MyWindow(l_files)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
