from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import PIL.Image
from typing import Optional, Tuple, Union
import customtkinter
from customtkinter import *
from tkinter import filedialog
import lexer, finalparser
import subprocess, sys, os

# FUNCTIONS
   # LIGHT SWITCH
def toggle():
     val = switch.get()
     if val:
         customtkinter.set_appearance_mode("Dark")
     else:
         customtkinter.set_appearance_mode("Light")
   # CLEAR
def clear_butt():
    input.delete(1.0, tk.END)
    output.delete(1.0, tk.END)
    symtab.delete(1.0, tk.END)
   # IMPORT
def import_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.cash")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            input.delete(1.0, tk.END) 
            input.insert(tk.END, content) 
# RUN
def on_run_pressed():
    output.delete(1.0, tk.END)
    symtab.delete(1.0, tk.END)
    
    # GET THE INPUT FROM TEXTBOX
    input_text = input.get("1.0", tk.END)

    # DISPLAY SYMBOL TABLE
    symbols = lexer.run(input_text)
    symtab.insert(tk.END, symbols)
    
    # DISPLAY OUTPUT 
    terminal = finalparser.lexer(input_text)
    output.insert(tk.END, terminal)

# MAIN COLORS
customtkinter.set_appearance_mode("Light")  
customtkinter.set_default_color_theme("green") 

# IMAGE ASSETS
logo_img = customtkinter.CTkImage(light_image=Image.open(r"PPL_logo.png"),
                                  dark_image=Image.open(r"PPL_logo.png"),
                                  size=(315,55))

# WINDOW
  # BASE
root = CTk()
root.title("CASH Compiler")
root.geometry(f"{1600}x{800}")
  # GRID LAYOUT
root.grid_columnconfigure((0), weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure((0,1,2), weight=0)
  # LOGO
logo = customtkinter.CTkLabel(root, text="", image=logo_img)
logo.grid(row=0, column=0, padx=30, pady=(30, 0), sticky="nw")

# INPUT BOX
lbl = customtkinter.CTkLabel(root, text="I N P U T", font=("",15))
lbl.grid(row=1, column=0, padx=30, pady=(20, 0), sticky="nw")
input = customtkinter.CTkTextbox(root, width=120, corner_radius=20, font=("", 15))
input.grid(row=1, column=0, rowspan=2, padx=(20, 20), pady=(50, 20), sticky="nsew")

# OUTPUT BOX
lbl = customtkinter.CTkLabel(root, text="O U T P U T", font=("",15))
lbl.grid(row=1, column=1, padx=30, pady=(20, 0), sticky="nw")
output = customtkinter.CTkTextbox(root, width=150, height=250, corner_radius=20, font=("",15))
output.grid(row=1, column=1, padx=(0, 20), pady=(50, 0), sticky="nsew")

# LEXEME / TOKEN PANEL
lbl = customtkinter.CTkLabel(root, text="S Y M B O L   T A B L E", font=("",15))
lbl.grid(row=2, column=1, padx=30, pady=(20, 0), sticky="nw")
symtab = customtkinter.CTkTextbox(root, width=150, height=250, corner_radius=20, font=("Courier",13))
#symtab = customtkinter.CTkScrollableFrame(root, width=150, height=250, corner_radius=20)
symtab.grid(row=2, column=1, padx=(0, 20), pady=(50, 20), sticky="nsew")
#symtab.tag_config("center", justify=customtkinter.CENTER)
#symtable = tk.Text(symtab, text="")

# BUTTONS
   # LIGHT SWITCH
switch = CTkSwitch(root, text = "Night Mode", onvalue=1, offvalue=0, command=toggle)
switch.grid(row=0, column=1, padx=(20, 40), pady=(40, 0), sticky="e")
   # RUN
runb = customtkinter.CTkButton(root, text="RUN", font=customtkinter.CTkFont(size=15, weight="bold"), command=on_run_pressed) #command=output_butt
runb.grid(row=3, column=0, padx=(20,30), pady=10, sticky="ne")
   # CLEAR
clrb = customtkinter.CTkButton(root, text="CLEAR", font=customtkinter.CTkFont(size=15, weight="bold"), command=clear_butt)
clrb.grid(row=3, column=1, padx=20, pady=10, sticky="n")
   # IMPORT
impb = customtkinter.CTkButton(root, text="IMPORT", font=customtkinter.CTkFont(size=15, weight="bold"), command=import_file)
impb.grid(row=3, column=0, padx=(0, 200), pady=10, sticky="ne")

# EXECUTE
root.mainloop()