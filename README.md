 📅 Social Media Scheduler

 🚀 Overview
The Social Media Scheduler is a Python-based tool that allows users to schedule and post content across multiple social media platforms using API integration. It provides an easy-to-use GUI with Tkinter, supports OAuth authentication, and stores scheduled posts in an SQLite database.

---

 🔑 Features
- 🌍 Multi-Platform Support (Facebook, Instagram, Twitter, LinkedIn)
- 🔐 OAuth Authentication for secure access
- 📝 Schedule Posts with date and time
- 📤 Automatic Posting using API calls
- 📊 SQLite Database to manage posts and authentication tokens
- 🖥️ Graphical User Interface (GUI) built with Tkinter

---

 📦 Installation
 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/social-media-scheduler.git
cd social-media-scheduler
```

 2️⃣ Install Dependencies
Ensure you have Python installed, then install the required packages:
```bash
pip install requests requests-oauthlib tkcalendar schedule
```

 3️⃣ Run the Application
```bash
python scheduler.py
```

---

 ⚙️ Configuration
 1️⃣ Set Up OAuth Credentials
Replace the following placeholders in `scheduler.py` with your actual API credentials:
```python
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "https://your_redirect_url.com"
AUTHORIZATION_URL = "https://socialmedia.com/oauth/authorize"
TOKEN_URL = "https://socialmedia.com/oauth/token"
```

 2️⃣ Database Setup
The application automatically creates an SQLite database `scheduler.db` to store authentication tokens and scheduled posts.

---

 🎯 Usage
 ✅ Authenticate with a Platform
1. Click the "🔑 Authenticate" button in the GUI.
2. Follow the OAuth authorization link.
3. Enter the authorization code to save your access token.

 📅 Schedule a Post
1. Enter your Username and select the Platform.
2. Type your Message and pick a Date & Time.
3. Click "✅ Schedule Post".

 🚀 Automatic Posting
- The script runs a scheduled job to post at the specified time.
- Posts will be marked as "Posted" or "Failed" in the database.

---

 🛠️ Technologies Used
- Python (Core language)
- Tkinter (GUI Framework)
- SQLite (Database for storing posts and tokens)
- OAuth 2.0 (Authentication)
- Requests (API Integration)
- Schedule (Automated task scheduling)

---

 🏗️ Future Enhancements
- ✅ Support for more platforms (YouTube, Pinterest, etc.)
- 📊 Dashboard to view scheduled and posted content
- 🔔 Notifications for successful or failed posts
- 📂 Export post history to CSV

---

 📜 License
This project is licensed under the MIT License. Feel free to use and modify it!

---

 🤝 Contributing
1. Fork the repository.
2. Create a new branch (`feature-new-feature`).
3. Commit your changes.
4. Push to the branch.
5. Submit a Pull Request.

---

 📧 Contact
For any issues or suggestions, please open an issue on GitHub or reach out at (vaishnavick05@gmail.com).

