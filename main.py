import joblib
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requires Pillow library

# Load the saved model with error handling
try:
    model = joblib.load('crop_recommendation_model.pkl')
except FileNotFoundError:
    messagebox.showerror("Model Error", "Model file not found. Please check the file path.")
    exit()
except Exception as e:
    messagebox.showerror("Model Error", f"An error occurred while loading the model: {e}")
    exit()

# Crop dictionary for mapping numbers to crop names
crop_dict = {
    'rice': 1, 'maize': 2, 'jute': 3, 'cotton': 4, 'coconut': 5,
    'papaya': 6, 'orange': 7, 'apple': 8, 'muskmelon': 9, 'watermelon': 10,
    'grapes': 11, 'mango': 12, 'banana': 13, 'pomegranate': 14, 'lentil': 15,
    'blackgram': 16, 'mungbean': 17, 'mothbeans': 18, 'pigeonpeas': 19,
    'kidneybeans': 20, 'chickpea': 21, 'coffee': 22
}

# Define the recommendation function that uses the loaded model
def recommend_crop(n, p, k, temp, humidity, ph, rainfall):
    input_data = [[n, p, k, temp, humidity, ph, rainfall]]
    crop_number = model.predict(input_data)[0]
    for crop_name, number in crop_dict.items():
        if number == crop_number:
            return crop_name
    return "Unknown Crop"

# Function to handle the Recommend button click
def on_recommend():
    try:
        n = float(n_entry.get())
        p = float(p_entry.get())
        k = float(k_entry.get())
        temp = float(temp_entry.get())
        humidity = float(humidity_entry.get())
        ph = float(ph_entry.get())
        rainfall = float(rainfall_entry.get())

        if not (0 <= n <= 500 and 0 <= p <= 500 and 0 <= k <= 500 and 0 <= temp <= 50 and 0 <= humidity <= 100 and 0 <= ph <= 14 and 0 <= rainfall <= 5000):
            raise ValueError("Input values are out of the expected range.")

        crop = recommend_crop(n, p, k, temp, humidity, ph, rainfall)
        recommendation_label.config(text=f"Recommended Crop: {crop}")
    except ValueError as e:
        messagebox.showerror("Invalid input", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Crop Recommendation System")
title_label = tk.Label(root, text="Crop Recommendation Model", font=("Courier New", 16, "bold"))
title_label.pack(pady=10)

# Main frame to hold image and input frames
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Left frame for the image
image_frame = tk.Frame(main_frame)
image_frame.grid(row=0, column=0, padx=10, pady=10)

# Load and display the image using the specified file path
file_path = r'image.jpg'
img = Image.open(file_path)
img = img.resize((200, 200), Image.LANCZOS)  # Resize to fit the label
img = ImageTk.PhotoImage(img)
image_label = tk.Label(image_frame, image=img)
image_label.image = img  # Keep a reference to prevent garbage collection
image_label.pack()

# Right frame for the input and recommendation widgets
input_frame = tk.Frame(main_frame)
input_frame.grid(row=0, column=1, padx=10, pady=10)

# Define and place labels and entry widgets for each input in the input frame
tk.Label(input_frame, text="Nitrogen (N)").grid(row=0, column=0, padx=10, pady=5, sticky='e')
n_entry = tk.Entry(input_frame)
n_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Phosphorus (P)").grid(row=1, column=0, padx=10, pady=5, sticky='e')
p_entry = tk.Entry(input_frame)
p_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Potassium (K)").grid(row=2, column=0, padx=10, pady=5, sticky='e')
k_entry = tk.Entry(input_frame)
k_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Temperature (°C)").grid(row=3, column=0, padx=10, pady=5, sticky='e')
temp_entry = tk.Entry(input_frame)
temp_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Humidity (%)").grid(row=4, column=0, padx=10, pady=5, sticky='e')
humidity_entry = tk.Entry(input_frame)
humidity_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(input_frame, text="pH Level").grid(row=5, column=0, padx=10, pady=5, sticky='e')
ph_entry = tk.Entry(input_frame)
ph_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Rainfall (mm)").grid(row=6, column=0, padx=10, pady=5, sticky='e')
rainfall_entry = tk.Entry(input_frame)
rainfall_entry.grid(row=6, column=1, padx=10, pady=5)

# Add a label to display the recommendation
recommendation_label = tk.Label(input_frame, text="", font=("Arial", 12, "bold"))
recommendation_label.grid(row=8, column=0, columnspan=2, pady=10)

# Create and place the 'Recommend' button
recommend_button = tk.Button(input_frame, text="Recommend Crop", command=on_recommend)
recommend_button.grid(row=7, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
