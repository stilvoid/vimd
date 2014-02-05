import pygtk
pygtk.require("2.0")

import gtk, sys, os, webkit, pyinotify

VIM = "gvim -c 'set guioptions-=m' --socketid {socket} {md}"

if len(sys.argv) < 3:
    print "You must supply two file names"
    sys.exit()

md = sys.argv[1]
html = sys.argv[2]
url="file://{0}".format(html)

wm = pyinotify.WatchManager()
wdd = wm.add_watch(md, pyinotify.IN_MODIFY|pyinotify.IN_CLOSE_WRITE)

class ModifyHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        os.system("markdown {md} > {html}".format(md=md, html=html))
        browser.open(url)

        wm.add_watch(md, pyinotify.IN_MODIFY|pyinotify.IN_CLOSE_WRITE)

notifier = pyinotify.ThreadedNotifier(wm, ModifyHandler())
notifier.start()

def destroy_event(widget):
    notifier.stop()
    gtk.mainquit()
    sys.exit(0)

def quit_event(widget, event):
    destroy_event(widget)

# Window setup
window = gtk.Window()
window.set_default_size(800, 600)
window.set_title("ViMD")
window.connect("delete_event", quit_event)

# HBox
box = gtk.HBox(True, 0)
window.add(box)
box.show()

window.show()

# Set up the vim plug
socket = gtk.Socket()
socket.show()
box.pack_start(socket)
vim = VIM.format(socket=socket.get_id(), md=md)
os.system("{0} &".format(vim))
socket.connect("destroy", destroy_event)

# webview
browser = webkit.WebView()
box.pack_start(browser)
browser.show()
browser.open(url)

socket.grab_focus()

gtk.mainloop()
