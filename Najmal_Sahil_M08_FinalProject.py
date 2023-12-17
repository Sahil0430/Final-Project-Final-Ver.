import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, Listbox, MULTIPLE
from PIL import Image, ImageTk

# Database of recipes
recipes = {
     # Each recipe is a dictionary with ingredients, cooking time, steps, and calorie count.
    "Chicken Salad": {
        "ingredients": ["Chicken", "Lettuce", "Tomato", "Cucumber"],
        "time": "15 mins",
        "steps": ["Chop all ingredients", "Mix them with any available dressing", "Serve"],
        "calories": "300 kcal"
    },
    "Beef Stew": {
        "ingredients": ["Beef", "Potato", "Carrot", "Onion"],
        "time": "1 hour",
        "steps": ["Brown the beef", "Add vegetables and simmer", "Serve hot"],
        "calories": "450 kcal"
    },
    "Fish Tacos": {
        "ingredients": ["Fish", "Lettuce", "Tomato", "Onion"],
        "time": "20 mins",
        "steps": ["Grill fish", "Chop veggies", "Assemble tacos"],
        "calories": "350 kcal"
    },
    "Veggie Stir Fry": {
        "ingredients": ["Spinach", "Carrot", "Onion", "Cabbage"],
        "time": "15 mins",
        "steps": ["Chop veggies", "Stir fry with seasoning", "Serve"],
        "calories": "200 kcal"
    },
    # ... other recipes
}

# Function to open a window for ingredient selection (either proteins or veggies).
def open_selection_window(title, items, save_function, image_path):
     # Creates a new Toplevel window for ingredient selection.
    window = tk.Toplevel(root)
    window.title(title)

    # Loads and displays an image specific to the ingredient type in the window.
    load_and_display_image_for_window(window, image_path)

    # ListBox to list and select ingredients.
    listbox = Listbox(window, selectmode=MULTIPLE)
    listbox.pack()

    # Populate the ListBox with the provided ingredient items.
    for item in items:
        listbox.insert(tk.END, item)

    # Buttons for saving the selection and closing the window.
    tk.Button(window, text="Save", command=lambda: save_function(listbox, window)).pack()
    tk.Button(window, text="Back", command=window.destroy).pack()


# Function to save the selected proteins and close the selection window.
def save_protein(listbox, window):
    global selected_proteins # References the global variable to store selected proteins.
    selected_proteins = [listbox.get(i) for i in listbox.curselection()] # Retrieves selected items from the ListBox.
    messagebox.showinfo("Selection Saved", f"Selected proteins: {', '.join(selected_proteins)}") # Shows confirmation message.
    window.destroy() # Closes the selection window.


# Function to save the selected veggies and close the selection window.
def save_veggies(listbox, window):
    global selected_veggies # References the global variable to store selected veggies.
    selected_veggies = [listbox.get(i) for i in listbox.curselection()] # Retrieves selected items from the ListBox.
    messagebox.showinfo("Selection Saved", f"Selected veggies: {', '.join(selected_veggies)}") # Shows confirmation message.
    window.destroy() # Closes the selection window.


# Function to find a recipe based on selected ingredients.
def find_recipe():
    # Checks if no ingredients are selected and displays a message if so.
    if not selected_proteins and not selected_veggies:
        messagebox.showinfo("No Ingredients Selected", "Please select at least one ingredient.")
        return
    
    print("Finding recipe...")
    print("Selected proteins:", selected_proteins)
    print("Selected veggies:", selected_veggies)
    found = False

    # Loops through the recipes to find a match with selected ingredients.
    for recipe_name, details in recipes.items():
        # Check if all ingredients of the recipe are in the selected ingredients
        if all(ingredient in selected_proteins + selected_veggies for ingredient in details["ingredients"]):
            print("Recipe found:", recipe_name)
            display_recipe(recipe_name, details)
            found = True
            break  # Stop after finding the first matching recipe

    # If no recipe is found, displays a message.
    if not found:
        print("No matching recipe found.")
        messagebox.showinfo("No Recipe Found", "Sorry, no matching recipe found. Try selecting different ingredients.")


# Function to display the details of a recipe in a new window.
def display_recipe(name, details):
    recipe_window = Toplevel(root) # Creates a new window for displaying the recipe.
    recipe_window.title(name) # Sets the title of the window to the recipe name.

    # Displays recipe information (name, ingredients, time, calories, cooking steps).
    tk.Label(recipe_window, text=f"Recipe: {name}").pack()
    tk.Label(recipe_window, text=f"Ingredients: {', '.join(details['ingredients'])}").pack()
    tk.Label(recipe_window, text=f"Time to Cook: {details['time']}").pack()
    tk.Label(recipe_window, text=f"Calories: {details['calories']}").pack()
    tk.Label(recipe_window, text="Cooking Steps:").pack()
    for step in details['steps']:
        tk.Label(recipe_window, text=f"- {step}").pack()


# Main function to set up and run the Tkinter application.
def main():
    global root, selected_proteins, selected_veggies
    selected_proteins, selected_veggies = [], []  # Initialize lists to store selected ingredients.

    # Setting up labels and buttons on the main window.
    root = tk.Tk() # Main application window.
    root.title("GranRecipes")  # Sets window title.
    root.minsize(300, 200)  # Sets minimum size of the window.

    ttk.Label(root, text="Welcome to GranRecipes!", font=("Helvetica", 16, "bold")).pack(pady=10)
    load_and_display_image("mascot.jpg") # Loads and displays the main image.
    ttk.Label(root, text="Let Ol' Gran help you out here. What's left over in the kitchen?", font=("Helvetica", 10)).pack(pady=5)

    # Buttons for ingredient selection, recipe finding, and exiting the application.
    ttk.Button(root, text="Protein", command=lambda: open_selection_window("Select Protein", ["Chicken", "Beef", "Fish"], save_protein, 'protein.jpg')).pack(pady=5)
    ttk.Button(root, text="Veggies", command=lambda: open_selection_window("Select Veggies", ["Tomato", "Onion", "Carrot", "Potato", "Cucumber", "Lettuce", "Spinach", "Cabbage"], save_veggies, 'veggies.jpg')).pack(pady=5)
    ttk.Button(root, text="Find Recipe", command=find_recipe).pack(pady=10)
    ttk.Button(root, text="Exit", command=root.destroy).pack(pady=10) # Closes the application when clicked.
   

    root.mainloop() # Starts the Tkinter event loop.


# Function to load and display an image in the main window.
def load_and_display_image(image_path):
        image = Image.open(image_path).resize((400,400))  # Opens and resizes the image.
        photo = ImageTk.PhotoImage(image) # Converts the image for Tkinter compatibility.
        label = tk.Label(root, image=photo) # Creates a label to display the image.
        label.image = photo  # Keep a reference.
        label.pack(pady=10) # Adds the label to the main window.

        
# Function to load and display an image in a Toplevel window.
def load_and_display_image_for_window(window, image_path, size=(100, 100)):
        image = Image.open(image_path) # Opens the image.
        resized_image = image.resize(size) # Resizes the image.
        photo = ImageTk.PhotoImage(resized_image)  # Converts the image for Tkinter compatibility.
        label = tk.Label(window, image=photo)  # Creates a label to display the image in the window.
        label.image = photo  # Keep a reference
        label.pack(pady=10) # Adds the label to the window.


if __name__ == "__main__":
    main() # Starting point of the application.
