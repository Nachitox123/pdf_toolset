import tkinter as tk
from tkinter import filedialog, messagebox
import os
import fitz # PyMuPDF

# Global variables to keep track of the PDF information
pdf_file = None
total_pages = 0
pages = []
thumbnails = []

# Function to open a PDF file
def open_pdf():
    global pdf_file, total_pages

    # Open the PDF file     initialdir=os.getcwd(), 
    file = filedialog.askopenfilename(title="Select a PDF", defaultextension=".pdf", filetype=(("PDF Files", "*.pdf"), ("All Files", "*.*")))

    if file:
        try: # Try to open the PDF file
            pdf_file = fitz.open(file)
            total_pages = pdf_file.page_count

            # Enable the buttons and set entry value to 1
            button_up.config(state=tk.NORMAL)
            button_down.config(state=tk.NORMAL)
            entry_integer.delete(0, tk.END)
            entry_integer.insert(0, "1")
            pages_label.config(text=f"/ {total_pages}")
            window.title(f"PDF Viewer - {os.path.basename(file)}")

            # Load thumbnails for all pages
            load_thumbnails()

            # Load all pages
            load_pages()

        except Exception as e:  # If it fails, show an error message
            messagebox.showerror("Error", f"Failed to open the PDF file: {str(e)}")
            return

# Function to load pages
def load_pages():
    if pdf_file:
        display_panel.delete("all")  # Clear the canvas

        pos_y = pos_x = 20
        widest_page = pos_x

        for page_num in range(0, total_pages):
            page = pdf_file[page_num]

            # Display preview in display_panel
            scale_factor = 1
            image = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor))
            tk_image = tk.PhotoImage(data=image.tobytes(), width=image.width, height=image.height)
            display_panel.create_image(pos_x, pos_y, anchor=tk.NW, image=tk_image)

            pages.append(tk_image)

            pos_y += image.height * 1.05

            if image.width > widest_page:
                widest_page = image.width

        # Update scroll regions
        display_panel.config(scrollregion=(0, 0, widest_page, pos_y))

# Function to load thumbnails
def load_thumbnails():
    thumbnail_panel.delete("all")  # Clear the canvas

    pos_y = pos_x = 6
    widest_thumbnail = 0

    for page_num in range(0, total_pages):
        page = pdf_file[page_num]

        # Thumbnail preview in thumbnails_panel
        scale_factor = 0.163
        thumbnail = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor))
        tk_thumbnail = tk.PhotoImage(data=thumbnail.tobytes(), width=thumbnail.width, height=thumbnail.height)
        thumbnail_panel.create_image(pos_x, pos_y, anchor=tk.NW, image=tk_thumbnail)

        thumbnails.append(tk_thumbnail)
        
        pos_y += thumbnail.height * 1.1

        if thumbnail.width > widest_thumbnail:
            widest_thumbnail = thumbnail.width

    # Adjust the scroll region for all thumbnails
    thumbnail_panel.config(scrollregion=(0, 0, widest_thumbnail, pos_y))

# Function to scroll vertically
def on_mousewheel(event, widget):
    widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Function to scroll horizontally
def on_control_mousewheel(event, widget):
    widget.xview_scroll(-1 * (event.delta // 120), "units")

# Function to show about
def show_about():
    messagebox.showinfo("About", "This is a simple To-Do List app.\nCreated by John Doe.")

# Function to exit
def exit_app():
    result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if result:
        window.destroy()

# Function to move to next page
def next_page():
    current_page = int(entry_integer.get())
    if 1 <= current_page < total_pages:
        entry_integer.delete(0, tk.END)
        entry_integer.insert(0, str(current_page + 1))
        load_pages(current_page + 1)

# Function to move to previous page
def previous_page():
    current_page = int(entry_integer.get())
    if 2 <= current_page <= total_pages:
        entry_integer.delete(0, tk.END)
        entry_integer.insert(0, str(current_page - 1))
        load_pages(current_page - 1)

# Create the main window
window = tk.Tk()
window.title("PDF Viewer")

# Set minimum size
window.minsize(width=475, height=550)

# Set default size
defaultWidth = 600
defaultHeight = 650

# Calculate the center of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = (screen_width - (defaultWidth)) // 2
y_coordinate = (screen_height - (defaultHeight)) // 3

# Set window position
window.geometry(f"{defaultWidth }x{defaultHeight }+{x_coordinate}+{y_coordinate}")

# # Set app icon dynamically
script_directory = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(script_directory, "pdf512.ico" if os.name == "nt" else "pdf512.icns")
window.iconbitmap(default=icon_path)

# Make rows and columns resizable
window.rowconfigure(1, weight=1)
window.columnconfigure(1, weight=1)

# Top Menu Bar
menu_bar = tk.Menu(window)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open...", command=open_pdf)
file_menu.add_command(label="Open Recent", command=exit_app)
file_menu.add_command(label="Close", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Tools Menu
tools_menu = tk.Menu(menu_bar, tearoff=0)
tools_menu.add_command(label="Select Area", command=exit_app)
tools_menu.add_command(label="Extract Page(s)...", command=exit_app)
menu_bar.add_cascade(label="Tools", menu=tools_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configuring the menu
window.config(menu=menu_bar)

# Canvas for thumbnails
thumbnail_panel = tk.Canvas(window, width=0, bg="gray", scrollregion=(0, 0, 0, 0))
thumbnail_panel.grid(row=0, column=0, rowspan=2, sticky="nsew")

# # Scroll for thumbnail_panel
thumbnail_panel.bind("<MouseWheel>", lambda event: on_mousewheel(event, thumbnail_panel))
# thumbnail_panel.bind("<Control-MouseWheel>", lambda event: on_control_mousewheel(event, thumbnail_panel))

# Frame for arrows, input, and label
nav_frame = tk.Frame(window, width=300)
nav_frame.grid(row=2, column=0, pady=(5, 5))

# Integer input entry
entry_integer = tk.Entry(nav_frame, width=5)
entry_integer.grid(row=0, column=0, padx=(0, 30))
entry_integer.insert(0, 0)

# Label for pages
pages_label = tk.Label(nav_frame, text=f"/ {total_pages}")
pages_label.grid(row=0, column=0, columnspan=2, padx=(30, 0))

# Buttons with arrows
button_up = tk.Button(nav_frame, text="Previous", command=previous_page)
button_up.grid(row=1, column=0, padx=(10, 50))

button_down = tk.Button(nav_frame, text="Next", command=next_page)
button_down.grid(row=1, column=0, columnspan=2, padx=(60, 0))

# Canvas for display
display_panel = tk.Canvas(window, width=0, bg="gray", scrollregion=(0, 0, 0, 0))
display_panel.grid(row=0, column=1, rowspan=3, columnspan=2, sticky="nsew") # Might change to rowspan=2

# Scroll for display_panel
display_panel.bind("<MouseWheel>", lambda event: on_mousewheel(event, display_panel))
display_panel.bind("<Control-MouseWheel>", lambda event: on_control_mousewheel(event, display_panel))

# Start the main loop
window.mainloop()
