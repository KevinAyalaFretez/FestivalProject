import tkinter as tk
from tkinter import messagebox
from tkinter import *
from Database_Connection import get_db_connection
import Database_Connection
from PIL import Image,ImageTk


#Creating a global default variable for check if the user is logged in, 
# inside of the function "existing user" I have the result True
is_logged_in = False

# Function for menu commands
def show_about():
    messagebox.showinfo("About",'This is a simple menu bar example')

def exit_app():
    root.quit()

def new_user():
    login_window = tk.Toplevel(root)
    login_window.title("New user registration")
    login_window.geometry("300x300")
    login_window.resizable(True, True)

    #center in window
    login_window.grab_set()

    # Creating labels and entry fields
    Label(login_window, text="new user", font=("Arial", 14)).pack(pady=5)
    Label(login_window, text="username").pack(pady=5)
    username_entry = tk.Entry(login_window, width=25)
    username_entry.pack(pady=5)

    Label(login_window, text="password").pack(pady=5)
    password_entry = tk.Entry(login_window, width=25, show="*")
    password_entry.pack(pady=5)

    Label(login_window, text="confirm password").pack(pady=5)
    confirm_password_entry = tk.Entry(login_window, width=25, show="*")
    confirm_password_entry.pack(pady=5)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
    
    # conditions
        if not username or not password:
            messagebox.showerror("Error","Please fill in all fields")
        elif password != confirm_password:
            messagebox.showerror("Password error","Password doesn't match")
        else:
            #Inserting the database
            conn = Database_Connection.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Insert into Users table
                    query = "INSERT INTO Users (username, password) VALUES (?, ?)"
                    cursor.execute(query, (username, password))
                    conn.commit()
                    messagebox.showinfo("Success", "User registered successfully")
                    login_window.destroy()
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to register: {e}")
                finally:
                    conn.close()
            else:
                messagebox.showinfo("Success","Account created succesfully")
                login_window.destroy()

#Button
    button_frame = Frame(login_window)
    button_frame.pack(pady=15)

    Button(button_frame, text="Register", command=register_user, bg=("green")).pack(side=LEFT,padx=5)

    Button(button_frame, text="Cancel", command=login_window.destroy, bg=("green")).pack(side=RIGHT, padx=5)

def existing_user():
    login_window = Toplevel(root)
    login_window.title("Existing user")
    login_window.geometry("300x300")
    login_window.resizable(True, True)

    # Creating labels and entry fields
    Label(login_window, text="Existing user", font=("Arial", 14)).pack(pady=5)
    Label(login_window, text="username").pack(pady=5)
    username_entry = tk.Entry(login_window, width=25)
    username_entry.pack(pady=5)

    Label(login_window, text="password").pack(pady=5)
    password_entry = tk.Entry(login_window, width=25, show="*")
    password_entry.pack(pady=5)

    Label(login_window, text="You don't have an account?", font=("Arial roma", 8)).pack(pady=5)

    def login_user():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        # Connect to database
        conn = Database_Connection.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM Users WHERE username = ? AND password = ?"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                if result:
                    #Creating global variables to check if the user is logged in or not
                    #Doesn't matter in which window or function we are
                    global is_logged_in, current_user
                    is_logged_in = True
                    current_user = username
                    messagebox.showinfo("Success", f"Welcome back, {username}",)
                    login_window.destroy()
                    open_mainpage()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
            except Exception as e:
                messagebox.showerror("Database Error", f"Login failed: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Connection Error", "Could not connect to database")

#Button
    button_frame = Frame(login_window)
    button_frame.pack(pady=15)

    Button(button_frame, text="Register", command=new_user, bg=("green")).pack(side=TOP,pady=10)

    Button(button_frame, text="Login", command=login_user, bg=("green")).pack(side=LEFT,padx=5)

    Button(button_frame, text="Cancel", command=login_window.destroy, bg=("green")).pack(side=RIGHT, padx=5)

def profile_button():
    if is_logged_in == True:
        Button6 = Button(mainpage,text="Profile",command=profile)
        Button6.pack(pady=5)

def open_mainpage():
    #Use destroy method to close the previous window
    root.destroy()
    
    #Creating global variable to call it in another functions
    global mainpage
    #Create the new window, this will be the new root because we destroyed the welcome screen
    mainpage = tk.Tk()
    mainpage.title("Main page")
    mainpage.geometry("800x500")

    #Load image
    bg_image = Image.open("Festival Main Page.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    mainpage.bg_photo = bg_photo

    # Set image as background
    bg_label = tk.Label(mainpage, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(mainpage, text="Main menu", font=("Arial", 14)).pack()

    #Create a frame
    frame = tk.Frame(mainpage, padx=100, pady=100)
    frame.pack(pady=150)

    Button3 = tk.Button(mainpage, text="Schedules",command=schedules)
    Button3.pack(pady=5)

    Button4 = tk.Button(mainpage, text="Buy tickets",command=buy_ticket)
    Button4.pack(pady=5)

    Button5 = tk.Button(mainpage, text="Festival's map",command=festival_map)
    Button5.pack(pady=5)

    #Calling the function to check if the user is logged in or not, depend of that will show this button or not
    profile_button()

def schedules():
    #We use toplevel because we want to open a window without close the previous one
    schedules = tk.Toplevel()
    schedules.title("Main page")
    schedules.geometry("800x500")

    #Load image
    image = Image.open("Timetable.jpg")
    #Resize the image
    resized_image = image.resize((800,500))
    photo = ImageTk.PhotoImage(resized_image)
    schedules.photo = photo

    #Creating the label for the image
    image_label = tk.Label(schedules, image=photo)
    image_label.pack()

def festival_map():
    #We use toplevel because we want to open a window without close the previous one
    festivalmap = tk.Toplevel()
    festivalmap.title("Main page")
    festivalmap.geometry("800x500")

    #Load image
    image = Image.open("Festival's map.jpg")
    #Resize the image
    resized_image = image.resize((800,500))
    photo = ImageTk.PhotoImage(resized_image)
    schedules.photo = photo

    #Creating the label for the image
    image_label = tk.Label(festivalmap, image=photo)
    image_label.pack()

def buy_ticket():
    buy_tickets = tk.Toplevel()
    buy_tickets.title("Buy tickets")
    buy_tickets.geometry("300x300")
    buy_tickets.resizable(True, True)

    #center in window
    buy_tickets.grab_set()

    # Creating labels and entry fields
    Label(buy_tickets, text="Checkout", font=("Arial", 14)).pack(pady=5)
    Label(buy_tickets, text="Name").pack(pady=5)
    if is_logged_in:
        #Creating a label for the current user if it's logged in
        current_user_label = Label(buy_tickets,text= f"{current_user}",font="Times").pack(pady=5)
    else:
        username_entry = tk.Entry(buy_tickets, width=25)
        username_entry.pack(pady=5)

    Label(buy_tickets, text="Quantity").pack(pady=5)
    #Creating stringvar for the menu of tickets
    string_var = StringVar()
    string_var.set('Select option')
    option_menu = OptionMenu(buy_tickets,string_var,'1 ticket','2 tickets','3 tickets','4 tickets').pack()

    def register_tickets():
        #Creating an if again to take the username from the current user or from the user that is not logged in
        if is_logged_in:
            username = current_user
            quantity = string_var.get()
        else:
            username = username_entry.get()
            quantity = string_var.get()
    
    # conditions
        if not username or not quantity:
            messagebox.showerror("Error","Please fill in all fields")
        else:
            #Inserting the database
            conn = Database_Connection.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Insert into Tickets table
                    query = "INSERT INTO Tickets (username, quantity) VALUES (?, ?)"
                    cursor.execute(query, (username, quantity))
                    conn.commit()
                    #Creating global variables to check if the user is logged in or not
                    #Doesn't matter in which window or function we are
                    global number_of_tickets
                    number_of_tickets = quantity
                    messagebox.showinfo("Success", "Tickets purchased correctly")
                    buy_tickets.destroy()
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to register: {e}")
                finally:
                    conn.close()
            else:
                messagebox.showinfo("Error","Try again")

#Button
    button_frame = Frame(buy_tickets)
    button_frame.pack(pady=15)

    Button(button_frame, text="Buy", command=register_tickets, bg=("green")).pack(side=LEFT,padx=5)

    Button(button_frame, text="Cancel", command=buy_tickets.destroy, bg=("red")).pack(side=RIGHT, padx=5)

def get_total_tickets_for_user(username):
        conn = Database_Connection.get_db_connection()  
        total_tickets = 0  # Default to 0 if no tickets found or error occurs
        if conn:
            try:
                cursor = conn.cursor()
                # SQL query to sum the 'quantity' for a specific 'username'
                # SUM helps us to ad together all the tickets
                # We use CAST AS INT because in my case I have the column in NVARCHAR instead of INT because I wanted to write 'tickets'
                # LEFT take the first values before the first space and CHARINDEX finds the position of the first space
                cursor.execute("SELECT SUM(CAST(LEFT(quantity , CHARINDEX(' ', quantity + ' ') - 1) AS INT)) FROM Tickets WHERE username = ? AND ISNUMERIC(LEFT(quantity , CHARINDEX(' ', quantity + ' ') - 1)) = 1", (username,))
                result = cursor.fetchone()
                # If result is not None and the first element is not None (meaning a sum was returned)
                if result and result[0] is not None:
                    total_tickets = result[0]
            except Exception as e:
                print(f"Error fetching ticket count for {username}: {e}")
                messagebox.showerror("Database Query Error", f"Failed to retrieve ticket count: {e}")
            finally:
                conn.close() # Always close the connection
        return total_tickets

def profile():
    profile1= tk.Toplevel()
    profile1.title("Profile")
    profile1.geometry("300x300")
    profile1.resizable(True, True)

    #center in window
    profile1.grab_set()

    Label(profile1, text="Username:").pack(pady=5)

    if is_logged_in:
        #Creating a label for the current user already logged in
        current_user_label = Label(profile1,text= f"{current_user}",font="Times")
        current_user_label.pack(pady=5)

    Label(profile1, text="Number of tickets:").pack(pady=5)

    if is_logged_in:  
        number_of_tickets = get_total_tickets_for_user(current_user)
        #Creating a label for the tickets of the user logged in
        number_of_tickets_label = Label(profile1,text= f"{number_of_tickets}",font="Times")
        number_of_tickets_label.pack(pady=5)



## Create the Welcome Screen window
root = tk.Tk()
root.title("Welcome Screen")
root.geometry("800x500")

#Load image
bg_image = Image.open("Festival Welcome Screen1.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Set image as background
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Create a frame
frame = tk.Frame(root, padx=100, pady=100)
frame.pack(pady=150)

Button1 = tk.Button(root, text="Continue as guest",command=open_mainpage)
Button1.pack(pady=5)

Button2 = tk.Button(root, text="Login",command=existing_user)
Button2.pack(pady=5)

#Create a menu bar
menu_bar = tk.Menu(root)

#Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit",command=exit_app)
file_menu.add_separator()
menu_bar.add_cascade(label="File",menu=file_menu)

#Create a Login menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Create account",command=new_user)
file_menu.add_separator()
file_menu.add_command(label="Existing user",command=existing_user)  
menu_bar.add_cascade(label="Login",menu=file_menu)

#Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

#Create a Contact menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Contact us",command=lambda:messagebox.showinfo("Contact us", "+44 123456780"))
file_menu.add_separator()
menu_bar.add_cascade(label="Contact",menu=file_menu)

# Attach the menu bar to the window
root.config(menu=menu_bar)

root.mainloop()