import logging
import tkinter as tk
import pystray._win32 #To avoid error No module named 'pystray._win32'  Ref:https://stackoverflow.com/a/68607905/1740113
from pystray._base import MenuItem as item
from PIL import Image, ImageTk
import pystray

root = None

#System Tray Icon References
#https://www.pythonexample.org/gui/how-to-use-tkinters-protocol-handler-in-python/
#https://www.tutorialspoint.com/how-to-make-a-system-tray-application-in-tkinter

def exit (root, canvas):  
    label1 = tk.Label(root, text= 'Exiting!', fg='green', font=('helvetica', 12, 'bold'))
    canvas.create_window(150, 200, window=label1)
    logging.info("Exit button clicked")

# Define a function for quit the window
def quit_window(icon, item):
    icon.stop()
    root.destroy()

# Define a function to show the window again
def show_window(icon, item):
    icon.stop()
    root.after(0,root.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
    root.withdraw()
    image=Image.open("./images/lv.png")
    #menu=(item('Quit', quit_window), item('Show', show_window))
    menu1 = pystray.Menu(pystray.MenuItem("Show", show_window, default=True),
            pystray.MenuItem("Exit", quit_window))
    icon=pystray.Icon("lv", image, "LabVIEW", menu1
    )
    print(icon.HAS_DEFAULT_ACTION)
    icon.run()

class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.text.config(state='disabled')
        self.text.tag_config("INFO", foreground="black") # Ref Coloring textbox https://stackoverflow.com/a/37188648/1740113
        self.text.tag_config("DEBUG", foreground="grey")
        self.text.tag_config("WARNING", foreground="orange")
        self.text.tag_config("ERROR", foreground="red")
        self.text.tag_config("CRITICAL", foreground="red", underline=1)

        self.red = self.text.tag_configure("red", foreground="red")

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n', record.levelname)
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass

def user_interface(exit_event):
    logging.info("Loading UI Thread")
    format = '%(asctime)s|%(name)s|%(levelname)s|%(message)s\n\n'
    try:
        global root
        root = tk.Tk()
        root.title("LabVIEW Python Server")
        root.geometry('500x300')
        root.iconphoto(False, tk.PhotoImage(file='./images/lv.png'))

        import tkinter.scrolledtext as ScrolledText
        scrolltextbox =  ScrolledText.ScrolledText(root, state='disabled', width=100, height=100)
        scrolltextbox.configure(font='TkFixedFont')
        scrolltextbox.pack()

        # Create textLogger
        text_handler = TextHandler(scrolltextbox)
        # Create time and message formatting  Ref: https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/
        formatter = logging.Formatter(format)
        text_handler.setFormatter(formatter)

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)

        #canvas1.create_window(150, 200, window=scrolltextbox)
        #scrolltextbox.pack()

        logging.info("UI Thread: Info Loaded")

        '''
        # create instance of file like object
        pl = PrintLogger(scrolltextbox)
        # replace sys.stdout with our object
        sys.stdout = pl
        logging.info("UI Thread: Canvas Loaded")
        '''

        print("UI Thread printing")
        root.protocol('WM_DELETE_WINDOW', hide_window)
        root.mainloop()
    except Exception as e:
        logging.error("UI Thread Error", exc_info=True)

if __name__ == '__main__':
    user_interface(exit_event=None)