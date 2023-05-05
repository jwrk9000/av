# simple gui
# scan/tools
# help/support/etc
# 



import tkinter as tk

root = tk.Tk()
root.title("Security Scanner")
root.geometry("800x900")

# Define fonts and styles
title_font = ("Arial Bold", 20)
box_font = ("Arial Bold", 16)
button_font = ("Arial Bold", 18)
box_borderwidth = 10
box_relief = "ridge"
box_width = 250
box_height = 150

# Define function to handle box clicks
def box_clicked(box_number):
    box_names = {1: "Threats", 2: "Support"}
    print(f"{box_names[box_number]} box clicked!")

# Create scan rectangle
scan_rect = tk.Button(root, bg="#42a5f5", borderwidth=box_borderwidth+2, relief="raised", text="SCAN", font=title_font,
                      fg="white", command=lambda: print("Scan box clicked!"))
scan_rect.place(x=130, y=50, width=540, height=150)

# Create boxes
threats_box = tk.Button(root, text="Threats", font=box_font, command=lambda: box_clicked(1),
                        borderwidth=box_borderwidth, relief=box_relief, bg="#9b4dca", fg="white")
threats_box.place(x=50, y=250, width=box_width, height=box_height)

support_box = tk.Button(root, text="Support", font=box_font, command=lambda: box_clicked(2),
                        borderwidth=box_borderwidth, relief=box_relief, bg="#8bc34a", fg="white")
support_box.place(x=50, y=450, width=box_width, height=box_height//2)

root.mainloop()




#if scan is clicked:
#if threats is clicked:
#if support is clicked:








#threat tab
#clean machine options
#file/help/support
#



