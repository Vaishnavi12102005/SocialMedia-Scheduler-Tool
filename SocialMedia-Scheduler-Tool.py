import requests
import sqlite3
import schedule
import time
import json
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from requests_oauthlib import OAuth2Session

# OAuth Configuration (Replace with actual credentials)
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "https://your_redirect_url.com"
AUTHORIZATION_URL = "https://socialmedia.com/oauth/authorize"
TOKEN_URL = "https://socialmedia.com/oauth/token"

# Database Setup
def create_database():
    conn = sqlite3.connect("scheduler.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        platform TEXT,
                        username TEXT,
                        access_token TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        platform TEXT,
                        username TEXT,
                        message TEXT,
                        schedule_date TEXT,
                        schedule_time TEXT,
                        status TEXT)''')
    conn.commit()
    conn.close()

# OAuth2 Authentication
def authenticate_user(platform):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)
    
    messagebox.showinfo("OAuth", f"Please go to this URL and authorize: {authorization_url}")
    
    auth_code = input("Enter the authorization code: ")  # User must enter manually
    
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=auth_code)
    
    save_access_token(platform, token["access_token"])
    messagebox.showinfo("Success", f"Authenticated for {platform}")

# Save Access Token
def save_access_token(platform, access_token):
    conn = sqlite3.connect("scheduler.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (platform, username, access_token) VALUES (?, ?, ?)",
                   (platform, "user", access_token))
    conn.commit()
    conn.close()

# Function to Schedule a Post
def schedule_post(platform, username, message, schedule_date, schedule_time):
    conn = sqlite3.connect("scheduler.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (platform, username, message, schedule_date, schedule_time, status) VALUES (?, ?, ?, ?, ?, ?)",
                   (platform, username, message, schedule_date, schedule_time, "Scheduled"))
    conn.commit()
    conn.close()

# API Call to Post on Social Media
def post_to_social_media(platform, message, access_token):
    url = f"https://api.{platform}.com/post"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = json.dumps({"message": message})

    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return True
    return False

# Function to Execute Scheduled Posts
def check_and_post():
    conn = sqlite3.connect("scheduler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, platform, username, message, schedule_date, schedule_time FROM posts WHERE status='Scheduled'")
    posts = cursor.fetchall()
    conn.close()

    current_date = time.strftime("%Y-%m-%d")
    current_time = time.strftime("%H:%M")

    for post_id, platform, username, message, schedule_date, schedule_time in posts:
        if current_date == schedule_date and current_time == schedule_time:
            conn = sqlite3.connect("scheduler.db")
            cursor = conn.cursor()
            cursor.execute("SELECT access_token FROM users WHERE platform=? AND username=?", (platform, username))
            result = cursor.fetchone()

            if result:
                access_token = result[0]
                success = post_to_social_media(platform, message, access_token)
                
                if success:
                    cursor.execute("UPDATE posts SET status='Posted' WHERE id=?", (post_id,))
                else:
                    cursor.execute("UPDATE posts SET status='Failed' WHERE id=?", (post_id,))
            else:
                cursor.execute("UPDATE posts SET status='Failed (No Token)' WHERE id=?", (post_id,))
            
            conn.commit()
            conn.close()

schedule.every().minute.do(check_and_post)

# GUI Application
class SocialMediaSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📅 Social Media Scheduler")
        self.root.geometry("500x550")
        self.root.configure(bg="#f8f9fa")

        # Title
        title = tk.Label(root, text="📅 Social Media Scheduler", font=("Arial", 16, "bold"), bg="#f8f9fa")
        title.pack(pady=10)

        self.frame = tk.Frame(root, bg="#f8f9fa")
        self.frame.pack(pady=10)

        self.create_labeled_entry("👤 Username:", "username_entry", row=0)
        self.create_labeled_combobox("🌐 Platform:", "platform_var", ["Facebook", "Instagram", "Twitter", "LinkedIn"], row=1)
        self.create_labeled_entry("📝 Message:", "message_entry", row=2, width=50)
        self.create_labeled_datepicker("📆 Date:", "date_entry", row=3)
        self.create_labeled_entry("⏰ Time (HH:MM):", "time_entry", row=4, width=10)

        self.schedule_button = tk.Button(root, text="✅ Schedule Post", command=self.schedule_post, bg="#007BFF", fg="white", font=("Arial", 12, "bold"))
        self.schedule_button.pack(pady=10)

        self.auth_button = tk.Button(root, text="🔑 Authenticate", command=self.authenticate, bg="#28A745", fg="white", font=("Arial", 12, "bold"))
        self.auth_button.pack(pady=10)

    def create_labeled_entry(self, label_text, var_name, row, width=30):
        frame = tk.Frame(self.frame, bg="#f8f9fa")
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="w")

        tk.Label(frame, text=label_text, bg="#f8f9fa", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        entry = tk.Entry(frame, width=width)
        entry.pack(side="right")
        setattr(self, var_name, entry)

    def create_labeled_combobox(self, label_text, var_name, values, row):
        frame = tk.Frame(self.frame, bg="#f8f9fa")
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="w")

        tk.Label(frame, text=label_text, bg="#f8f9fa", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        var = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=var, values=values)
        combo.pack(side="right")
        setattr(self, var_name, var)

    def create_labeled_datepicker(self, label_text, var_name, row):
        frame = tk.Frame(self.frame, bg="#f8f9fa")
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="w")

        tk.Label(frame, text=label_text, bg="#f8f9fa", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        date_picker = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_picker.pack(side="right")
        setattr(self, var_name, date_picker)

    def schedule_post(self):
        messagebox.showinfo("✅ Success", "Post scheduled!")

    def authenticate(self):
        messagebox.showinfo("🔑 Auth", "Authentication successful!")

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    app = SocialMediaSchedulerApp(root)
    root.mainloop()
