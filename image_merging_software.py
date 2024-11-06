import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

# Function to browse and select the input folder
def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_var.set(folder_selected)

# Function to browse and select the output folder
def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_var.set(folder_selected)

# Function to process images as per your original logic
def process_images(eye_image_path, wavefront_image_path, output_file_path):
    try:
        # Load the eye image and wavefront image
        eye_image = Image.open(eye_image_path).convert("RGBA")
        wavefront_image = Image.open(wavefront_image_path).convert("RGBA")

        # Resize wavefront image to match the size of the eye image
        wavefront_image = wavefront_image.resize(eye_image.size)

        # Set transparency level for wavefront image
        wavefront_image.putalpha(128)

        # Overlay the wavefront image onto the keratometer eye image
        eye_image.paste(wavefront_image, (0, 0), wavefront_image)

        # Create a draw object to draw the grid on the image
        draw = ImageDraw.Draw(eye_image)

        # Get the center coordinates of the image
        center_x = eye_image.width // 2
        center_y = eye_image.height // 2

        # Draw the horizontal and vertical lines through the center
        draw.line([(0, center_y), (eye_image.width, center_y)], fill=(0, 255, 0, 255), width=1)
        draw.line([(center_x, 0), (center_x, eye_image.height)], fill=(0, 255, 0, 255), width=1)

        # Save the processed image
        eye_image.save(output_file_path)
        print(f"Processed and saved: {output_file_path}")

    except Exception as e:
        print(f"Error processing images: {e}")

# Function to start processing based on user input
def start_processing():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()

    if not input_folder or not output_folder:
        messagebox.showwarning("Missing Folder", "Please select both input and output folders.")
        return

    # Organize images by type
    keratometer_images = {}
    wavefront_images = {}

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                file_path = os.path.join(root, filename)

                if 'keratometer' in filename:
                    keratometer_images[filename] = file_path
                elif 'wavefront' in filename:
                    wavefront_images[filename] = file_path

    # Match keratometer and wavefront images and process them
    for keratometer_filename in keratometer_images:
        eye_key = keratometer_filename.replace('keratometer', 'wavefront')

        if eye_key in wavefront_images:
            keratometer_path = keratometer_images[keratometer_filename]
            wavefront_path = wavefront_images[eye_key]

            # Define the output filename and path
            output_filename = f"processed_{keratometer_filename}"
            output_file_path = os.path.join(output_folder, output_filename)

            # Process and merge the images
            process_images(keratometer_path, wavefront_path, output_file_path)
        else:
            print(f"No matching wavefront image found for: {keratometer_filename}")

    messagebox.showinfo("Completed", "Image processing completed.")

# Function to merge two images with grid and transparency (your new task)
def merge_images():
    # Ask user to select the two images
    eye_image_path = filedialog.askopenfilename(title="Select Eye Image", filetypes=[("Image files", "*.jpg;*.png")])
    wavefront_image_path = filedialog.askopenfilename(title="Select Wavefront Image",
                                                      filetypes=[("Image files", "*.jpg;*.png")])

    if not eye_image_path or not wavefront_image_path:
        messagebox.showwarning("Missing Images", "Please select both an eye image and a wavefront image.")
        return

    # Load the images
    try:
        eye_image = Image.open(eye_image_path).convert("RGBA")
        wavefront_image = Image.open(wavefront_image_path).convert("RGBA")

        # Resize wavefront image to match the size of the eye image
        wavefront_image = wavefront_image.resize(eye_image.size)

        # Set transparency level for wavefront image
        transparency = 128
        wavefront_image.putalpha(transparency)

        # Overlay the wavefront image onto the keratometer eye image
        eye_image.paste(wavefront_image, (0, 0), wavefront_image)

        # Create a draw object to draw the grid on the image
        draw = ImageDraw.Draw(eye_image)

        # Get the center coordinates of the image
        center_x = eye_image.width // 2
        center_y = eye_image.height // 2

        # Draw the horizontal and vertical lines through the center
        grid_color = (0, 255, 0, 255)  # Green
        draw.line([(0, center_y), (eye_image.width, center_y)], fill=grid_color, width=1)
        draw.line([(center_x, 0), (center_x, eye_image.height)], fill=grid_color, width=1)

        # Save the merged image and open it separately
        output_file_path = "merged_image.png"
        eye_image.save(output_file_path)
        eye_image.show()  # Display the image in the default image viewer

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while merging images: {e}")

# Create the GUI window
root = tk.Tk()
root.title("Image Processing Software")

# Load and set the custom icon
icon_image = Image.open('C:/forus data/PROJECT 3/Image-Merging/forus logo 2.png')
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# Set window size and background color
root.geometry("500x400")
root.configure(bg="#f0f0f0")

# Font styles
title_font = ("Helvetica", 16, "bold")
button_font = ("Helvetica", 12, "bold")

# Title Label
title_label = tk.Label(root, text="Image Processing Software", font=title_font, bg="#f0f0f0")
title_label.pack(pady=20)

# Create variables to store folder paths
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()

# Input folder selection
tk.Label(root, text="Input Folder:", font=button_font, bg="#f0f0f0").pack(pady=5)
input_folder_entry = tk.Entry(root, textvariable=input_folder_var, width=40)
input_folder_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_input_folder, font=button_font, bg="#4CAF50", fg="white").pack(pady=5)

# Output folder selection
tk.Label(root, text="Output Folder:", font=button_font, bg="#f0f0f0").pack(pady=5)
output_folder_entry = tk.Entry(root, textvariable=output_folder_var, width=40)
output_folder_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_output_folder, font=button_font, bg="#4CAF50", fg="white").pack(pady=5)

# Start Processing button
tk.Button(root, text="Start Processing", command=start_processing, font=button_font, bg="#2196F3", fg="white").pack(
    pady=20)

# Merge Images button
tk.Button(root, text="Merge Images", command=merge_images, font=button_font, bg="#FF5722", fg="white").pack(pady=10)

# Run the application
root.mainloop()
