import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tkinter as tk
from tkinter import simpledialog, messagebox, Scrollbar, Text
from PIL import Image, ImageTk  # To handle image in Tkinter
import sys

# Load the dataset from the specified file path
file_path = r"C:\Users\USER\Desktop\RECOMENDATION\hyderabad.csv"  # Raw string to handle backslashes
df = pd.read_csv(file_path)

# Data Preprocessing
df['Price'] = df['Price'].replace(r'[\$,]', '', regex=True).astype(float)
df['Tax'] = df['Tax'].replace(r'[\$,]', '', regex=True).fillna(0).astype(float)
df['Star Rating'] = df['Star Rating'].fillna(df['Star Rating'].median())
df['Price After Tax'] = df['Price'] + df['Tax']
df.drop(['Nearest Landmark', 'Distance to Landmark'], axis=1, inplace=True)

# Normalize the 'Rating' and 'Reviews' columns using MinMaxScaler
scaler = MinMaxScaler()
df[['Rating', 'Reviews']] = scaler.fit_transform(df[['Rating', 'Reviews']])

# Compute Popularity Score
df['Popularity Score'] = 0.7 * df['Rating'] + 0.3 * df['Reviews']

# Function to get hotel recommendations based on user choice
def get_hotel_recommendations(df):
    while True:
        filter_choice = simpledialog.askstring("Filter Choice", "Do you want to filter by 'rating', 'price', or 'both'?").strip().lower()
        
        try:
            if filter_choice == 'rating':
                while True:
                    try:
                        min_rating = float(simpledialog.askstring("Minimum Rating", "Enter the minimum rating you prefer (1-5, e.g., 4): "))
                        if 1 <= min_rating <= 5:
                            break
                        else:
                            messagebox.showinfo("Invalid Input", "Rating should be between 1 and 5.")
                    except ValueError:
                        messagebox.showinfo("Invalid Input", "Please enter a valid number for rating.")
                
                recommended_hotels = df[df['Star Rating'] >= min_rating].sort_values(by='Rating', ascending=False)

            elif filter_choice == 'price':
                while True:
                    try:
                        max_price = float(simpledialog.askstring("Maximum Price", "Enter the maximum price you are willing to pay (e.g., 10000): "))
                        if max_price >= 0:
                            break
                        else:
                            messagebox.showinfo("Invalid Input", "Price should be a positive number.")
                    except ValueError:
                        messagebox.showinfo("Invalid Input", "Please enter a valid number for price.")
                
                recommended_hotels = df[df['Price After Tax'] <= max_price].sort_values(by='Price', ascending=True)

            elif filter_choice == 'both':
                while True:
                    try:
                        min_rating = float(simpledialog.askstring("Minimum Rating", "Enter the minimum rating you prefer (1-5, e.g., 4): "))
                        if 1 <= min_rating <= 5:
                            break
                        else:
                            messagebox.showinfo("Invalid Input", "Rating should be between 1 and 5.")
                    except ValueError:
                        messagebox.showinfo("Invalid Input", "Please enter a valid number for rating.")
                
                while True:
                    try:
                        max_price = float(simpledialog.askstring("Maximum Price", "Enter the maximum price you are willing to pay (e.g., 10000): "))
                        if max_price >= 0:
                            break
                        else:
                            messagebox.showinfo("Invalid Input", "Price should be a positive number.")
                    except ValueError:
                        messagebox.showinfo("Invalid Input", "Please enter a valid number for price.")
                
                recommended_hotels = df[(df['Star Rating'] >= min_rating) & (df['Price After Tax'] <= max_price)].sort_values(by='Popularity Score', ascending=False)

            else:
                messagebox.showinfo("Invalid Choice", "Invalid choice. Please choose either 'rating', 'price', or 'both'.")
                continue

        except ValueError:
            messagebox.showinfo("Invalid Input", "Invalid input. Please enter a valid number.")
            continue

        if recommended_hotels.empty:
            messagebox.showinfo("No Results", "No hotels match your criteria. Please adjust your preferences.")
            return None
        else:
            hotel_names = recommended_hotels['Hotel Name'].tolist()
            return hotel_names

# Function to get similar destinations
def get_similar_destinations(input_destination):
    recommendations = {
        1: ["Charminar", "Golconda Fort", "Chowmahalla Palace", "Qutb Shahi Tombs"],
        2: ["Salar Jung Museum", "Birla Planetarium", "Laad Bazaar"],
        3: ["Hussain Sagar Lake", "Necklace Road", "Hyderabad Botanical Garden"],
    }
    input_destination = input_destination.lower()

    # Flatten the recommendations into a dictionary
    destination_to_category = {destination.lower(): category for category, destinations in recommendations.items() for destination in destinations}

    if input_destination in destination_to_category:
        category = destination_to_category[input_destination]
        similar_destinations = recommendations[category]
        similar_destinations = [d for d in similar_destinations if d.lower() != input_destination]
        return similar_destinations
    else:
        return None

# Function to reset the UI and restart the application
def reset_ui():
    root.destroy()  # Close the current instance of the Tkinter window
    main()  # Restart the application

# Function to show UI with a background image
def main():
    global root, text  # Make text and root accessible in reset_ui function

    # Create the root window for tkinter
    root = tk.Tk()
    root.title("Hotel and Destination Recommendations")
    
    # Set window size
    root.geometry("1000x600")
    
    # Load background image
    bg_image = Image.open(r'C:\Users\USER\Desktop\RECOMENDATION\Background_img.jpg')  # Path to background image
    bg_image = bg_image.resize((1000, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Load logo image
    logo_image = Image.open(r'C:\Users\USER\Desktop\RECOMENDATION\Background_img.jpg')  # Path to logo image
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    # Create canvas for background image
    canvas = tk.Canvas(root, width=1000, height=600)
    canvas.pack(fill="both", expand=True)
    
    # Add background image to canvas
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    
    # Add logo to top right
    canvas.create_image(900, 20, image=logo_photo, anchor="ne")
    
    # Create frames for displaying the results
    frame = tk.Frame(root, bg="white")
    frame.place(x=50, y=100, width=900, height=400)
    
    # Create a Text widget with a Scrollbar
    text = Text(frame, wrap=tk.WORD, font=("Helvetica", 12), bg="white")
    scrollbar = Scrollbar(frame, command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Create a reset button
    reset_button = tk.Button(root, text="Reset", command=reset_ui, bg="lightblue")
    reset_button.place(x=450, y=520, anchor="center")
    
    # Get hotel recommendations
    hotel_names = get_hotel_recommendations(df)
    
    if hotel_names:
        # Ask for destination input
        while True:
            input_destination = simpledialog.askstring("Destination Input", "Enter a destination you're interested in (e.g., Charminar):").strip()
            if input_destination:
                similar_destinations = get_similar_destinations(input_destination)
                if similar_destinations:
                    break
                else:
                    messagebox.showinfo("No Results", "No similar destinations found. Please enter a different destination.")
            else:
                messagebox.showinfo("Invalid Input", "Please enter a valid destination.")
        
        destination_message = f"Since you like {input_destination}, you might also enjoy:\n" + "\n".join(similar_destinations)
        combined_message = f"Recommended Hotels:\n" + "\n".join(hotel_names) + "\n\nRecommended Destinations:\n" + destination_message
    else:
        combined_message = "No hotel recommendations were found based on your criteria."
    
    # Display results in the Text widget
    text.insert(tk.END, combined_message)
    text.config(state=tk.DISABLED)  # Make the text widget read-only
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
