#!/usr/bin/env python3
import time
import six
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from Xlib.display import Display
from Xlib.protocol import event
from Xlib import XK, X, ext
from threading import Timer
import cairo

log_file = None

def log(*args):
    # Enable for debugging
    if False:
        global log_file
        if log_file is None:
            log_file = open('/tmp/gtk-emoji-chooser.log', 'a')
        print(*args, file=log_file)
        log_file.flush()

class EmojiPicker(object):
    def __init__(self):
        self.display = Display()
        self.update_last_focus()
        self.win = Window(cb=self.emoji_picked)

    def update_last_focus(self):
        self.focus = self.display.get_input_focus().focus
        log(self.focus, self.focus.get_wm_name())

    def focus_last(self):
        self.display.set_input_focus(self.focus.id, X.RevertToParent, X.CurrentTime)

    def key_press(self, k):
        c = self.display.keysym_to_keycode(XK.string_to_keysym(k))
        ext.xtest.fake_input(self.display, X.KeyPress, c)

    def key_release(self, k):
        c = self.display.keysym_to_keycode(XK.string_to_keysym(k))
        ext.xtest.fake_input(self.display, X.KeyRelease, c)

    def keys(self, ks):
        for k in ks:
            self.key_press(k)
            self.key_release(k)

    def emoji_picked(self, emoji):
        emoji_to_print = emoji
        if six.PY2:
            emoji_to_print = emoji.encode('utf-8')
        log('emoji picked', emoji_to_print, hex(ord(emoji)))
        h = hex(ord(emoji)).lstrip('0x')
        hs = [str(hdigit) for hdigit in h]
        self.focus_last()
        self.key_press('Shift_L')
        self.key_press('Control_L')
        self.keys(['u'])
        self.key_release('Shift_L')
        self.key_release('Control_L')
        time.sleep(0.1)
        self.keys(hs + ['Return'])
        time.sleep(0.1)
        self.display.sync()
        self.display.close()
        Gtk.main_quit()

    def main(self):
        self.win.connect('destroy', Gtk.main_quit)
        self.win.show_all()
        self.win.open_picker()
        Gtk.main()

class Window(Gtk.Window):

    def __init__(self, cb):
        Gtk.Window.__init__(self, title='Standalone emoji picker')
        self.callback = cb

        self.set_default_size(500, 500)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.set_decorated(False)
        self.connect('notify::is-active', self.is_active_changed)
        self.stick()

        # Make the window transparent
        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_app_paintable(True)
        self.set_visual(rgba)
        self.connect('draw', self.draw)

        # Load the CSS
        gtk_provider = Gtk.CssProvider()
        gtk_context = Gtk.StyleContext()
        gtk_context.add_provider_for_screen(Gdk.Screen.get_default(), gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        gtk_provider.load_from_data(b'''
        .hidden { background: #000; opacity: 0; }
        ''')

        # Setup the text view
        self.textview = Gtk.TextView()
        self.textview.get_style_context().add_class('hidden')
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.connect('changed', self.emoji_picked)
        self.textview.connect('focus_in_event', self.focus_in)
        self.textview.connect('focus_out_event', self.focus_out)
        box = Gtk.Box()
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.END)
        box.add(self.textview)
        self.add(box)

    def emoji_picked(self, buf):
        log('emoji picked')
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(start_iter, end_iter, True)
        if six.PY2:
            text = text.decode('utf-8')
        # TODO: check is one char, emoji
        self.callback(text[0])

    def open_picker(self):
        log('open picker')
        self.textview.grab_focus()
        self.textview.emit('insert-emoji')

    def draw(self, widget, event):
        cr = widget.get_window().cairo_create()
        # Sets the operator to clear the window background
        cr.set_source_rgba(.0, .0, .0, .0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        # Set the compositing operator back to the default
        cr.set_operator(cairo.OPERATOR_OVER)
        return False

    def is_active_changed(self, widget, event):
        if not self.props.is_active:
            log('window unactive, closing...')
            self.close()

    def focus_in(self, widget, event):
        log('focus_in')
        self.hide()

    def focus_out(self, widget, event):
        log('focus_out')
        return True


picker = EmojiPicker()
picker.main()
