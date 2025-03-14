# Imports

import tkinter as tk
from tkinter import ttk
import json as js
import traceback

# Scrollable frame 
# as in www.geeksforgeeks.org/scrollable-frames-in-tkinter/
def create_scrollable_frame(parent, params, pack):
      
  # Step 4: Create a Canvas and Scrollbar
  canvas = tk.Canvas(parent)
  scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
  canvas.configure(yscrollcommand=scrollbar.set)

  # Step 5: Create a Frame for Scrollable Content
  content_frame = tk.Frame(canvas, **params)

  
  def onCanvasConfigure(e):
    canvas.itemconfig('frame', width=canvas.winfo_width())
    canvas.configure(scrollregion=canvas.bbox("all"))

  # Step 6: Configure the Canvas and Scrollable Content Frame
  content_frame.bind("<Configure>", onCanvasConfigure)
  # Step 9: Pack Widgets onto the Window
  canvas.pack(**pack)
  canvas.create_window((0, 0), window=content_frame, anchor="nw", tags="frame")
  scrollbar.pack(side="right", fill="y")
  canvas.itemconfig('frame', width=canvas.winfo_width())
  # Step 10: Bind the Canvas to Mousewheel Events
  def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

  canvas.bind_all("<MouseWheel>", _on_mousewheel)

  return content_frame

widgets = {}

# This file contains all the functions trigered by the buttons

def add_column():
  if not len(widgets['plack_place'].instance.winfo_children()) <= 12: return
  print("add column")
  open_json("config_plack", widgets["plack_place"])
  widgets["plack_name"].instance.config(text=f"Column #{len(widgets['plack_place'].instance.winfo_children())}")
  mainWindow.instance.update()


def create_db():
  open_json("config_workspace", widgets["tables"])


# List of all the commands available for button binds
comms = {
  "open_db":None,
  "create_db":create_db,
  "config_db":None,
  "close_db":None,
  "add_column":add_column,
  "save_changes":None
}



# List of suported Widgets
#~~Maybe add secondary window constructor later
w_type = {
  "notebook":ttk.Notebook,
  "frame":tk.Frame,
  "lable":ttk.Label,
  "button":ttk.Button,
  "entry":ttk.Entry,
  "menu":tk.Menu,
  "scrollable_frame":tk.Frame,
  "combobox":ttk.Combobox
}
# This file is responsible for generating tk widgets based on json files

class Widget:
  children = []
  def scroll_conf(self, *args):
    self.instance.configure(scrollregion=self.instance.bbox("all"))
  def __init__(self, json_string = None, parent = None):
    # Check if the root widget, if it is create Tk instance and return
    if parent == None:
      self.instance = tk.Tk()
      return
    # Tries to acces type, params and pack set in json for current widget, 
    # Creates its instance
    try:
      reference = w_type[json_string["type"]]
      if json_string["type"] == "scrollable_frame":
        self.instance = create_scrollable_frame(parent.instance, json_string["params"], json_string["pack"])
      elif json_string["type"] == "menu":
        self.instance = tk.Menu(parent.instance)
        for tab in json_string["tabs"]:
          buf = tk.Menu(self.instance, tearoff=0)
          self.instance.add_cascade(label=tab, menu=buf)
          for part in json_string["tabs"][tab]:
            if len(part) == 3:
              buf.add_command(label=part[0], command=comms[part[1]], state=part[2])
            else:
              buf.add_command(label=part[0], command=comms[part[1]])
        parent.instance.config(menu = self.instance)
        return
      else:
        self.instance = reference(parent.instance, **json_string["params"])
      if type(parent.instance) == ttk.Notebook:
        parent.instance.add(self.instance, **json_string["pack"])
      elif not json_string["type"]=="scrollable_frame":
        self.instance.pack(**json_string["pack"])
    except Exception as e:
      print(traceback.format_exc())
      print(f"Wrong widget constructor: {json_string}")
      return
    # Check if widget has command option, if has add according command
    try:
      json_string["command"]
      self.instance.configure(command=comms[json_string["command"]])
    except Exception as e:
      print(f"No command in {json_string['type']}")
    
    # Check if widget has to have children
    try:
      json_string["children"]
      # Create and append all the children
      for child in json_string["children"]:
        self.children.append(Widget(child, self))
    except: print(f"No children in {json_string['type']}")


    # Add self to parents children if not yet added
    if not self in parent.children:
      parent.children.append(self)
    
    # Remember widget if has name
    try:
      json_string["name"]
      widgets.update({json_string["name"]: self})
    except:
      print("No name. Don't remember")

  def findLable(self, match):
    if type(self.instance) == tk.Label and self.instance.get()==match:
      return self
    for child in self.children:
      if not child.findLable(match) == None:
        return child.findLable(match)
    return None


def open_json(file_name, parent):
  with open(f"json_files\\{file_name}.json") as json_file:
    json = js.load(json_file)
    for element in json:
      Widget(element, parent)


mainWindow = Widget()