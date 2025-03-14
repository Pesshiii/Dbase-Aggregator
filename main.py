# Imports

from json_to_tk import *
import os
import time
from threading import Thread


def run():
  print("change")
  for child in mainWindow.children:
    child.instance.destroy()
  mainWindow.children = []
  open_json("window", mainWindow)


#Function that checks if gui files have been modified as in
#www.geeksforgeeks.org/how-to-detect-file-changes-using-python
def detect_file_changes(folder_path = "json_files", func = run, interval=1):
  folder = [f'{folder_path}\\{i}' for i in os.listdir(folder_path)]
  last_modified = {}
  for file in folder:
    last_modified.update({file:os.path.getmtime(file)})
  while True:
    for file_path in folder:
      current_modified = os.path.getmtime(file_path)
      if current_modified != last_modified[file_path]:
          func()
          last_modified[file_path] = current_modified
      time.sleep(interval)



# This file create Window of the aplitcation and monitors it
# Creating Widget object for main window
mainWindow.instance.geometry("750x600")
open_json("window", mainWindow)

# developer mode checks if source files have changed, then refreshes the programm
Thread(target=detect_file_changes, daemon=True).start()


mainWindow.instance.mainloop()
