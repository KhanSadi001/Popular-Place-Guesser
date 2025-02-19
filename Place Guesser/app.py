import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import os
import google.generativeai as genai

# Ensure API key is set in your environment variables
genai.configure(api_key=os.environ['API_KEY'])

def start_app():
    global root, l2, tk_img, response_text

    root = tk.Tk()
    root.geometry("800x500")
    root.title("Place Guesser App")

    # Set Application Icon (Ensure 'icon.ico' exists)
    root.iconbitmap("icon.ico")  

    # Set Background Color
    root.configure(bg="#e0e0e0")  

    # Open file dialog to select an image file
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = filedialog.askopenfilename(filetypes=fileTypes)

    # If no file is selected, show an error message and exit
    if not path:
        error_label = tk.Label(root, text="You must upload a picture to run the app!", fg="red", font=("Helvetica", 14, "bold"))
        error_label.pack(pady=20)
        button_frame = tk.Frame(root, bg="#e0e0e0")
        button_frame.pack(pady=10)
        restart_button = tk.Button(button_frame, text="Restart", command=restart_app, 
                               bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                               padx=10, pady=5, relief="raised", cursor="hand2")
        restart_button.pack()
        root.mainloop()
        return
    
    messagebox.showinfo("", "Please Wait, Complex Processing is Underway.")
    
    # Load and process the image
    img = Image.open(path)
    img.thumbnail((200, 200))  # Resize image while maintaining aspect ratio

    # Add a border around the image
    img = ImageOps.expand(img, border=5, fill="black")
    
    try:
        # Generate AI model response based on the image
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(["Can you provide the location with coordinates?", img])
    except Exception as e:
        # Show error message if API call fails
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        root.destroy()
        return

    # Convert image to Tkinter format
    tk_img = ImageTk.PhotoImage(img)

    # Frame to hold the image
    img_frame = tk.Frame(root, bg="black", bd=2, relief="ridge")
    img_frame.pack(pady=10)

    l2 = tk.Label(img_frame, image=tk_img, bg="black")
    l2.pack()

    # Scrollable Response Frame to display AI response
    response_container = tk.Frame(root, bg="#e0e0e0")
    response_container.pack(pady=10, fill="both", expand=True)

    canvas = tk.Canvas(response_container, bg="#e0e0e0", height=150)
    scrollbar = ttk.Scrollbar(response_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#e0e0e0")

    # Update scrollable region when frame size changes
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Display AI-generated response text
    response_text = tk.Label(scrollable_frame, text=response.text if response else "No response received.", bg="#e0e0e0", font=("Helvetica", 14), wraplength=600, justify="left")
    response_text.pack(padx=10, pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Styled Restart Button
    button_frame = tk.Frame(root, bg="#e0e0e0")
    button_frame.pack(pady=10)

    restart_button = tk.Button(button_frame, text="Restart", command=restart_app, 
                               bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                               padx=10, pady=5, relief="raised", cursor="hand2")
    restart_button.pack()

    root.mainloop()

# Function to restart the application
def restart_app():
    root.destroy()
    start_app()

start_app()
