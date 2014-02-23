#!/usr/bin/python
# python imports
import os
import sys
import StringIO
import re

# pygtk imports
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk
import pango


def move_to_start_of_line(it):
    """Move a TextIter it to the start of a paragraph"""
    
    if not it.starts_line():
        if it.get_line() > 0:
            it.backward_line()
            it.forward_line()
        else:
            it = it.get_buffer().get_start_iter()
    return it

def move_to_end_of_line(it):
    """Move a TextIter it to the start of a paragraph"""
    it.forward_line()
    return it


class Stream (object):

    def __init__(self, callback):
        self._callback = callback

    def write(self, text):
        #ntext = text.split("\n")
        #for i in ntext:
            
            #self._callback(i)
        self._callback(text)

    def flush(self):
        pass



#class PythonDialog (object):
class PythonDialog ():
    """Python dialog"""
    
    #def __init__(self, main_window):
    def __init__(self):
        #self.main_window = main_window
        self.app = ""
        #self.app = main_window.get_app()

        self.outfile = Stream(self.output_text)
        self.errfile = Stream(lambda t: self.output_text(t, "error"))

        self.error_tag = gtk.TextTag()
        self.error_tag.set_property("foreground", "red")
        self.error_tag.set_property("weight", pango.WEIGHT_BOLD)

        self.info_tag = gtk.TextTag()
        self.info_tag.set_property("foreground", "blue")
        self.info_tag.set_property("weight", pango.WEIGHT_BOLD)

    
    def show(self):

        # setup environment
        

        # create dialog
        self.dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.dialog.connect("delete-event", lambda d,r: self.dialog.destroy())
        self.dialog.connect("destroy", gtk.main_quit)
        self.dialog.ptr = self
        
       
        
        self.dialog.set_default_size(400, 400)

        self.vpaned = gtk.VPaned()
        self.dialog.add(self.vpaned)
        self.vpaned.set_position(200)
        
        # editor buffer
        
        #buffer1 = gtk.TextBuffer()
        #siter = gtk.textbuffer_get_iter_at_line(1)
        #eiter = gtk.TextBuffer_get_iter_at_line(1000)
        buffer1 = gtk.TextBuffer()
        eiter = buffer1.get_end_iter()
        buffer1.text = ""
        #self.editor = gtk.TextView()
        self.editor = gtk.TextView()
        #self.editor = editor.set_buffer(buffer1)
        self.editor.connect("key-press-event", self.on_key_press_event)
        f = pango.FontDescription("Courier New")
        self.editor.modify_font(f)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.add(self.editor)
        self.vpaned.add1(sw)
        
        # output buffer
        #self.output = gtk.TextView()
        self.output = gtk.TextView(buffer=buffer1)
        self.output.set_wrap_mode(gtk.WRAP_WORD)
        f = pango.FontDescription("Courier New")
        self.output.modify_font(f)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.add(self.output)
        self.vpaned.add2(sw)
        
        self.output.get_buffer().tag_table.add(self.error_tag)
        self.output.get_buffer().tag_table.add(self.info_tag)
        
        self.env = {"app": self.app,
                    "window": self.output,
                    "info": "pypad"}
        #self.env = {"app": self.app,
                    #"window": self.output,
                    #"info": self.print_info}
        
        
        self.dialog.show_all()
        #self.dialog.show()
        print "test"

        self.output_text("Press Ctrl+Enter to execute. Ready...\n", "info")
    

    def on_key_press_event(self, textview, event):
        """Callback from key press event"""
        bdir = "/home/tun/perl/python/sps/"
        
        if (event.keyval == gtk.keysyms.Return and
            event.state & gtk.gdk.CONTROL_MASK):
            # execute
            self.execute_buffer()
            return True
            
        if (event.keyval == gtk.keysyms.Return and
            event.state & gtk.gdk.SHIFT_MASK):
            # execute
            
            self.output_text("1Press Ctrl+Enter to execute. Ready...\n", "info")
            buf = self.output.get_buffer()
            start = buf.get_start_iter()
            buf.insert(start, "ss")
            buffer1 = gtk.TextBuffer()
            self.output.set_buffer(buffer1)
            return True
        if (event.keyval == gtk.keysyms.s and
            event.state & gtk.gdk.CONTROL_MASK):
            # execute
            buf = self.editor.get_buffer()
            #buf.text
            end = buf.get_end_iter()
            start = buf.get_start_iter()
            text = start.get_text(end)
            
            sel = buf.get_selection_bounds()
            if len(sel) > 0:
            # get selection
                start1, end1 = sel
                text1 = start1.get_text(end1)
                text = re.sub(text1,"",text)
                text = re.sub("\n+$","", text)
                self.output_text("save to " + text1 + "\n", "info")
                self.output_text(text, "info")
                if os.path.exists(bdir+text1):
                    self.output_text(text1 + " is already existed\n", "info")
                else:
                    saves = open(bdir+text1,"w")
                    saves.write(text)
                    saves.close()
            else:
                self.output_text("not save, no file name\n", "info")

            
            return True
            
        if (event.keyval == gtk.keysyms.u and
            event.state & gtk.gdk.CONTROL_MASK):
            # execute
            buf = self.editor.get_buffer()
            #buf.text
            end = buf.get_end_iter()
            start = buf.get_start_iter()
            text = start.get_text(end)
            
            sel = buf.get_selection_bounds()
            if len(sel) > 0:
            # get selection
                start1, end1 = sel
                text1 = start1.get_text(end1)
                text = re.sub(text1,"",text)
                text = re.sub("\n+$","", text)
                self.output_text("updated to " + text1 + "\n", "info")
                self.output_text(text, "info")
                #if os.path.exists(bdir+text1):
                    #self.output_text(text1 + " is already existed\n", "info")
                #else:
                saves = open(bdir+text1,"w")
                saves.write(text)
                saves.close()
           

            
            return True

        if event.keyval == gtk.keysyms.Return:
            # new line indenting
            self.newline_indent()
            buf = self.editor.get_buffer()
            mark = buf.get_insert()
            self.editor.scroll_mark_onscreen(mark)
            return True


    def newline_indent(self):
        """Insert a newline and indent"""

        buf = self.editor.get_buffer()

        it = buf.get_iter_at_mark(buf.get_insert())
        start = it.copy()
        start = move_to_start_of_line(start)
        line = start.get_text(it)
        indent = []
        for c in line:
            if c in " \t":
                indent.append(c)
            else:
                break
        buf.insert_at_cursor("\n" + "".join(indent))
        
        
        

    def execute_buffer(self):
        """Execute code in buffer"""

        buf = self.editor.get_buffer()

        sel = buf.get_selection_bounds()
        if len(sel) > 0:
            # get selection
            start, end = sel
            self.output_text("executing selection:\n", "info")
        else:
            # get all text
            start = buf.get_start_iter()
            end = buf.get_end_iter()
            self.output_text("executing buffer:\n", "info")

        # get text in selection/buffer
        text = start.get_text(end)

        # execute code
        execute(text, self.env, self.outfile, self.errfile)


    def output_text(self, text, mode="normal"):
        """Output text to output buffer"""
        
        buf = self.output.get_buffer()

        # determine whether to follow
        
        mark = buf.get_insert()
        it = buf.get_iter_at_mark(mark)
        
        
        follow = it.is_end()
        #print text
        # add output text
        if mode == "error":
            buf.insert_with_tags(buf.get_end_iter(), text, self.error_tag)
        elif mode == "info":
            buf.insert_with_tags(buf.get_end_iter(), text, self.info_tag)
        else:
            #textn = text.split("\n")
            #for jj in textn:
                #jj = jj + "\n"
            buf.insert(buf.get_end_iter(), text)
            #buf.insert(buf.get_end_iter(), jj)
        
        if follow:
            buf.place_cursor(buf.get_end_iter())
            self.output.scroll_mark_onscreen(mark)
            
        #print text


 

def execute(code, vars, stdout, stderr):
    """Execute user's python code"""

    __stdout = sys.stdout
    __stderr = sys.stderr
    sys.stdout = stdout
    sys.stderr = stderr
    try:
        exec(code, vars)
    except Exception, e:
        #print "test"
        print e
        #keepnote.log_error(e, sys.exc_info()[2], stderr)
    sys.stdout = __stdout
    sys.stderr = __stderr
    #print sys.stdout

def list_commands(app):
    """List available commands"""
    
    commands = app.get_commands()
    commands.sort(key=lambda x: x.name)

    print
    print "available commands:"
    for command in commands:
        print " " + command.name,
        if command.metavar:
            print " " + command.metavar,            
        if command.help:
            print " -- " + command.help,
        print



o = PythonDialog()
o.show()
gtk.main()

