import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import hashlib

class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        # Configure root window for login
        self.root.title("Login - AI Assistant")
        self.root.geometry("500x650")
        self.root.configure(bg='#f5f5f5')
        
        # DeepSeek-inspired color palette
        self.colors = {
            "primary": "#1a73e8",
            "primary_light": "#e8f0fe",
            "text": "#202124",
            "text_secondary": "#5f6368",
            "background": "#ffffff",
            "card": "#ffffff",
            "border": "#dadce0",
            "error": "#d93025"
        }
        
        # User database
        self.users = {
            "admin": {
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "name": "Administrator"
            },
            "user": {
                "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
                "name": "Regular User"
            }
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container with shadow effect
        self.main_container = tk.Frame(self.root, bg=self.colors["background"])
        self.main_container.pack(fill='both', expand=True, padx=40, pady=60)
        
        # Card frame with elevation effect
        self.card = tk.Frame(
            self.main_container,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=30,
            pady=40
        )
        self.card.pack(fill='both', expand=True)

        
        
        # Logo/header
        self.header_frame = tk.Frame(self.card, bg=self.colors["card"])
        self.header_frame.pack(fill='x', pady=(0, 30))
        
        self.logo_label = tk.Label(
            self.header_frame,
            text="AI Assistant",
            font=('Arial', 24, 'bold'),
            bg=self.colors["card"],
            fg=self.colors["primary"]
        )
        self.logo_label.pack(side='left')
        
        # Welcome text
        self.welcome_label = tk.Label(
            self.card,
            text="Sign in to continue",
            font=('Arial', 14),
            bg=self.colors["card"],
            fg=self.colors["text_secondary"]
        )
        self.welcome_label.pack(anchor='w', pady=(0, 30))
        
        # Input fields container
        self.input_container = tk.Frame(self.card, bg=self.colors["card"])
        self.input_container.pack(fill='x')
        
        # Username field
        self.username_frame = tk.Frame(self.input_container, bg=self.colors["card"])
        self.username_frame.pack(fill='x', pady=(0, 20))
        
        self.username_label = tk.Label(
            self.username_frame,
            text="Username",
            font=('Arial', 12),
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        self.username_label.pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            self.username_frame,
            font=('Arial', 14),
            bg=self.colors["background"],
            fg=self.colors["text"],
            insertbackground=self.colors["primary"],
            relief=tk.FLAT,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            highlightthickness=1
        )
        self.username_entry.pack(fill='x', ipady=8)
        
        # Password field
        self.password_frame = tk.Frame(self.input_container, bg=self.colors["card"])
        self.password_frame.pack(fill='x', pady=(0, 30))
        
        self.password_label = tk.Label(
            self.password_frame,
            text="Password",
            font=('Arial', 12),
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        self.password_label.pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(
            self.password_frame,
            font=('Arial', 14),
            bg=self.colors["background"],
            fg=self.colors["text"],
            insertbackground=self.colors["primary"],
            relief=tk.FLAT,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            highlightthickness=1,
            show="•"
        )
        self.password_entry.pack(fill='x', ipady=8)
        
        # Login button
        self.login_button = tk.Button(
            self.card,
            text="Sign in",
            font=('Arial', 14, 'bold'),
            bg=self.colors["primary"],
            fg='white',
            activebackground=self.colors["primary"],
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            command=self.attempt_login
        )
        self.login_button.pack(fill='x', pady=(10, 0))
        
        # Error label
        self.error_label = tk.Label(
            self.card,
            text="",
            font=('Arial', 11),
            bg=self.colors["card"],
            fg=self.colors["error"]
        )
        self.error_label.pack(pady=(15, 0))
        
        # Footer
        self.footer_frame = tk.Frame(self.card, bg=self.colors["card"])
        self.footer_frame.pack(fill='x', pady=(20, 0))
        
        self.footer_label = tk.Label(
            self.footer_frame,
            text="New to AI Assistant? Contact admin for access",
            font=('Arial', 11),
            bg=self.colors["card"],
            fg=self.colors["text_secondary"]
        )
        self.footer_label.pack()
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.attempt_login())
        
        # Add hover effects
        self.login_button.bind("<Enter>", lambda e: self.login_button.config(bg="#0d5bba"))
        self.login_button.bind("<Leave>", lambda e: self.login_button.config(bg=self.colors["primary"]))
        
        # Focus on username field by default
        self.username_entry.focus_set()
    
    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.error_label.config(text="Please enter both username and password")
            return
        
        if username not in self.users:
            self.error_label.config(text="Invalid username or password")
            return
            
        # Verify password hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != self.users[username]["password_hash"]:
            self.error_label.config(text="Invalid username or password")
            return
        
        # Login successful - animate button click
        self.login_button.config(bg="#0a4b9e")
        self.root.after(100, lambda: self.complete_login(username))
    
    def complete_login(self, username):
        self.card.pack_forget()
        self.main_container.pack_forget()
        
        # Fade out animation
        for i in range(10, -1, -1):
            alpha = i/10
            self.root.attributes('-alpha', alpha)
            self.root.update()
            self.root.after(20)
        
        self.root.attributes('-alpha', 1)
        self.on_login_success(username)
        
class AnimatedChatBot:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"AI Assistant - Welcome {username}")
        self.root.geometry("1000x700")
        self.root.configure(bg='#343541')
        
        # Settings variables
        self.theme_var = tk.StringVar(value="dark")
        self.language_var = tk.StringVar(value="english")
        self.email_var = tk.StringVar(value=f"{username}@example.com")
        self.notifications_var = tk.BooleanVar(value=True)
        
        self.chat_sessions = []
        self.current_chat = []
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.recognizer = sr.Recognizer()
        
        self.create_widgets()
        self.start_new_chat()

    def create_widgets(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg='#343541')
        self.main_container.pack(fill='both', expand=True)
        
        # Sidebar (left)
        self.sidebar = tk.Frame(self.main_container, width=250, bg='#202123')
        self.sidebar.pack(side='left', fill='y', expand=False)
        self.sidebar.pack_propagate(False)
        
        # New Chat button
        self.new_chat_btn = tk.Button(
            self.sidebar, 
            text="+ New Chat", 
            font=('Arial', 12, 'bold'),
            bg='#40414F', 
            fg='white',
            relief=tk.FLAT,
            command=self.start_new_chat
        )
        self.new_chat_btn.pack(fill='x', padx=10, pady=10, ipady=8)
        
        # Chat history frame
        self.history_frame = tk.Frame(self.sidebar, bg='#202123')
        self.history_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Chat history scrollable area
        self.history_canvas = tk.Canvas(self.history_frame, bg='#202123', highlightthickness=0)
        self.history_scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_canvas.yview)
        self.history_scrollable_frame = tk.Frame(self.history_canvas, bg='#202123')
        
        self.history_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(
                scrollregion=self.history_canvas.bbox("all")
            )
        )
        
        self.history_canvas.create_window((0, 0), window=self.history_scrollable_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)
        
        self.history_canvas.pack(side="left", fill="both", expand=True)
        self.history_scrollbar.pack(side="right", fill="y")
        
        # Main chat area (right)
        self.chat_area = tk.Frame(self.main_container, bg='#343541')
        self.chat_area.pack(side='right', fill='both', expand=True)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_area,
            wrap=tk.WORD,
            font=('Consolas', 12),
            bg='#343541',
            fg='white',
            insertbackground='white',
            padx=20,
            pady=20,
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Input area
        self.input_frame = tk.Frame(self.chat_area, bg='#343541')
        self.input_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.input_field = tk.Entry(
            self.input_frame,
            font=('Consolas', 14),
            bg='#40414F',
            fg='white',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.input_field.pack(side='left', fill='x', expand=True, ipady=8)
        self.input_field.bind('<Return>', lambda e: self.process_input())
        
        self.send_button = tk.Button(
            self.input_frame,
            text="➤",
            font=('Arial', 14),
            bg='#19C37D',
            fg='white',
            relief=tk.FLAT,
            command=self.process_input
        )
        self.send_button.pack(side='right', padx=(10, 0), ipadx=10, ipady=2)
        
        # Voice button
        self.voice_button = tk.Button(
            self.input_frame,
            text="🎤",
            font=('Arial', 12),
            bg='#40414F',
            fg='white',
            relief=tk.FLAT,
            command=self.voice_command
        )
        self.voice_button.pack(side='right', padx=(0, 10), ipadx=5, ipady=2)
        
        # Bottom buttons in sidebar
        self.bottom_frame = tk.Frame(self.sidebar, bg='#202123')
        self.bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        # Profile button
        self.profile_button = tk.Button(
            self.bottom_frame,
            text="👤 Profile",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            relief=tk.FLAT,
            command=self.show_profile
        )
        self.profile_button.pack(fill='x', pady=(0, 5), ipady=5)
        
        # Logout button
        self.logout_button = tk.Button(
            self.bottom_frame,
            text="Logout",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            relief=tk.FLAT,
            command=self.logout
        )
        self.logout_button.pack(fill='x', ipady=5)
        
        # Responses dictionary
        self.responses = {
            "hello": ["Hey! How can I help you?", "Hello! 😊"],
            "how are you": ["I'm doing great, thanks!", "I'm good, how about you?"],
            "bye": ["Goodbye!", "See you later!", "Have a great day!"],
            "who are you": ["I'm ChatBot", "You can call me ChatBot or also Your ELIZA!"],
            "time": [f"It's currently {datetime.now().strftime('%I:%M %p')}"],
            "date":[f"Today is {datetime.now().strftime('%B %d, %Y')}"],
            "help": ["You can ask me about the time, date, or else!"],
            "what is": ["It is an interpreted, object-oriented, high-level programming language with dynamic semantics."],
            "mother": ["your mother is Uma Soni"],
            "father": ["your father is Tushar Soni"],
            "sister": ["your sister is Nidhi Soni"],
            "who is indian prime minister": ["your Prime Minister is Narendra Modi"],
            "link": ["https://www.google.com"],
            "write a python program": ["print('Hello, World!')"],
            "Made": ["This chatbot was made by Bhavya Soni"],
            "weather": ["It's a nice day today!", "The weather is perfect!"],
            "thanks": ["You're welcome!", "Anytime!", "My pleasure!"],
            "num": ["Let me calculate that for you..."],
            "default": ["I'm not sure about that.", "Could you rephrase that?", "Interesting, tell me more."]
        }
  
    def draw_robot_face(self):
        pass  # Not needed in this layout
    
    def start_new_chat(self):
        self.current_chat = []
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        self.add_message("AI Assistant", f"Welcome back, {self.username}! How can I help you today?", "#19C37D")
        
        # Add to chat sessions
        session_id = len(self.chat_sessions) + 1
        session_title = f"Chat {session_id}"
        self.chat_sessions.append({
            "id": session_id,
            "title": session_title,
            "messages": []
        })
        
        # Update history sidebar
        self.update_chat_history()
    
    def update_chat_history(self):
        # Clear existing history buttons
        for widget in self.history_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Add all chat sessions
        for session in reversed(self.chat_sessions):
            btn = tk.Button(
                self.history_scrollable_frame,
                text=session["title"],
                font=('Arial', 11),
                bg='#202123',
                fg='white',
                relief=tk.FLAT,
                anchor='w',
                command=lambda s=session: self.load_chat_session(s["id"])
            )
            btn.pack(fill='x', padx=5, pady=2, ipady=5)
    
    def load_chat_session(self, session_id):
        # Find the session
        session = next((s for s in self.chat_sessions if s["id"] == session_id), None)
        if not session:
            return
        
        # Load the chat
        self.current_chat = session["messages"]
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        
        for msg in self.current_chat:
            self.chat_display.insert(tk.END, f"{msg['sender']}: {msg['message']}\n", msg['color'])
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def add_message(self, sender, message, color='white'):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n", color)
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        # Add to current chat
        self.current_chat.append({
            "sender": sender,
            "message": message,
            "color": color
        })
        
        # Update the last session with this message
        if self.chat_sessions:
            self.chat_sessions[-1]["messages"] = self.current_chat
            self.chat_sessions[-1]["title"] = message[:30] + "..." if len(message) > 30 else message
            self.update_chat_history()
        
        if sender == "AI Assistant":
            self.speak(message)
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    

    def show_profile(self):
        # Create profile window
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title("Profile & Settings")
        self.profile_window.geometry("600x700")
        self.profile_window.configure(bg='#343541')
        self.profile_window.resizable(False, False)
        
        # Main container
        container = tk.Frame(self.profile_window, bg='#343541')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Profile header
        header_frame = tk.Frame(container, bg='#343541')
        header_frame.pack(fill='x', pady=(0, 20))
        
        profile_icon = tk.Label(
            header_frame,
            text="👤",
            font=('Arial', 24),
            bg='#343541',
            fg='white'
        )
        profile_icon.pack(side='left', padx=(0, 10))
        
        profile_title = tk.Label(
            header_frame,
            text="Profile & Settings",
            font=('Arial', 18, 'bold'),
            bg='#343541',
            fg='white'
        )
        profile_title.pack(side='left')
        
        # Notebook for tabs
        notebook = ttk.Notebook(container)
        notebook.pack(fill='both', expand=True)
        
        # Profile tab
        profile_tab = tk.Frame(notebook, bg='#343541')
        notebook.add(profile_tab, text="Profile")
        
        # Settings tab
        settings_tab = tk.Frame(notebook, bg='#343541')
        notebook.add(settings_tab, text="Settings")
        
        # About tab
        about_tab = tk.Frame(notebook, bg='#343541')
        notebook.add(about_tab, text="About")
        
        # Profile tab content
        self.create_profile_tab(profile_tab)
        
        # Settings tab content
        self.create_settings_tab(settings_tab)
        
        # About tab content
        self.create_about_tab(about_tab)
    
    def create_profile_tab(self, parent):
        # Profile info frame
        info_frame = tk.Frame(parent, bg='#40414F', padx=20, pady=20, relief=tk.RIDGE, bd=2)
        info_frame.pack(fill='x', pady=(0, 20))
        
        # Username
        tk.Label(
            info_frame,
            text="Username:",
            font=('Arial', 12),
            bg='#40414F',
            fg='#D1D5DB'
        ).grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        tk.Label(
            info_frame,
            text=self.username,
            font=('Arial', 12, 'bold'),
            bg='#40414F',
            fg='white'
        ).grid(row=0, column=1, sticky='w', pady=(0, 10))
        
        # Email
        tk.Label(
            info_frame,
            text="Email:",
            font=('Arial', 12),
            bg='#40414F',
            fg='#D1D5DB'
        ).grid(row=1, column=0, sticky='w', pady=(0, 10))
        
        email_entry = tk.Entry(
            info_frame,
            textvariable=self.email_var,
            font=('Arial', 12),
            bg='#565869',
            fg='white',
            relief=tk.FLAT
        )
        email_entry.grid(row=1, column=1, sticky='we', pady=(0, 10))
        
        # Member since
        tk.Label(
            info_frame,
            text="Member since:",
            font=('Arial', 12),
            bg='#40414F',
            fg='#D1D5DB'
        ).grid(row=2, column=0, sticky='w', pady=(0, 10))
        
        tk.Label(
            info_frame,
            text=datetime.now().strftime("%B %d, %Y"),
            font=('Arial', 12, 'bold'),
            bg='#40414F',
            fg='white'
        ).grid(row=2, column=1, sticky='w', pady=(0, 10))
        
        # Save button
        save_btn = tk.Button(
            parent,
            text="Save Changes",
            font=('Arial', 12, 'bold'),
            bg='#19C37D',
            fg='white',
            relief=tk.FLAT,
            command=lambda: self.save_profile(self.email_var.get())
        )
        save_btn.pack(fill='x', pady=(10, 0), ipady=8)
    
    def create_settings_tab(self, parent):
        # Theme settings
        theme_frame = tk.LabelFrame(
            parent,
            text="Appearance",
            font=('Arial', 12, 'bold'),
            bg='#40414F',
            fg='white',
            padx=15,
            pady=15
        )
        theme_frame.pack(fill='x', pady=(0, 20))
        
        # Theme selection
        tk.Radiobutton(
            theme_frame,
            text="Dark Mode",
            variable=self.theme_var,
            value="dark",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            selectcolor='#343541',
            activebackground='#40414F',
            activeforeground='white'
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Radiobutton(
            theme_frame,
            text="Light Mode",
            variable=self.theme_var,
            value="light",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            selectcolor='#343541',
            activebackground='#40414F',
            activeforeground='white'
        ).pack(anchor='w')
        
        # Language settings
        lang_frame = tk.LabelFrame(
            parent,
            text="Language",
            font=('Arial', 12, 'bold'),
            bg='#40414F',
            fg='white',
            padx=15,
            pady=15
        )
        lang_frame.pack(fill='x', pady=(0, 20))
        
        tk.Radiobutton(
            lang_frame,
            text="English",
            variable=self.language_var,
            value="english",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            selectcolor='#343541',
            activebackground='#40414F',
            activeforeground='white'
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Radiobutton(
            lang_frame,
            text="Hindi",
            variable=self.language_var,
            value="hindi",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            selectcolor='#343541',
            activebackground='#40414F',
            activeforeground='white'
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Radiobutton(
            lang_frame,
            text="Spanish",
            variable=self.language_var,
            value="spanish",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            selectcolor='#343541',
            activebackground='#40414F',
            activeforeground='white'
        ).pack(anchor='w')
        
        # Notification settings
        notif_frame = tk.LabelFrame(
            parent,
            text="Notifications",
            font=('Arial', 12, 'bold'),
            bg='#40414F',
            fg='white',
            padx=15,
            pady=15
        )
        notif_frame.pack(fill='x', pady=(0, 20))
        
        tk.Checkbutton(
            notif_frame,
            text="Enable notifications",
            variable=self.notifications_var,
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            selectcolor='#343541',
            activebackground='#40414F',
            activeforeground='white'
        ).pack(anchor='w')
        
        # Save settings button
        save_btn = tk.Button(
            parent,
            text="Save Settings",
            font=('Arial', 12, 'bold'),
            bg='#19C37D',
            fg='white',
            relief=tk.FLAT,
            command=self.save_settings
        )
        save_btn.pack(fill='x', pady=(10, 0), ipady=8)
    
    def create_about_tab(self, parent):
        # About info
        about_text = """
        AI Assistant

        Version: 1.0.0
        Developed by: Bhavya Soni
        
        This application is designed to help you with various tasks 
        through natural language processing and AI capabilities.
        
        Features:
        - Chat with AI
        - Voice commands
        - Math calculations
        - Personal assistance
        
        Privacy Policy:
        Your data is kept secure and private. We do not share 
        your conversations or personal information with third parties.
        
        Terms of Use:
        This application is provided as-is for educational purposes.
        """
        
        about_label = tk.Label(
            parent,
            text=about_text,
            font=('Arial', 11),
            bg='#343541',
            fg='white',
            justify='left',
            padx=20,
            pady=20
        )
        about_label.pack(fill='both', expand=True)
        
        # Contact button
        contact_btn = tk.Button(
            parent,
            text="Contact Support",
            font=('Arial', 11),
            bg='#40414F',
            fg='white',
            relief=tk.FLAT,
            command=self.contact_support
        )
        contact_btn.pack(fill='x', pady=(0, 10), ipady=5)
    
    def save_profile(self, new_email):
        # In a real app, you would save this to a database
        self.email_var.set(new_email)
        messagebox.showinfo("Success", "Profile updated successfully!")
    
    def save_settings(self):
        # In a real app, you would save these settings
        messagebox.showinfo("Success", "Settings saved successfully!")
        
        # Apply theme change immediately
        if self.theme_var.get() == "light":
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
    
    def apply_light_theme(self):
        self.root.configure(bg='#f5f5f5')
        self.main_container.configure(bg='#f5f5f5')
        self.sidebar.configure(bg='#ffffff')
        self.history_frame.configure(bg='#ffffff')
        self.history_canvas.configure(bg='#ffffff')
        self.history_scrollable_frame.configure(bg='#ffffff')
        self.chat_area.configure(bg='#f5f5f5')
        self.chat_display.configure(bg='white', fg='black')
        self.input_frame.configure(bg='#f5f5f5')
        self.input_field.configure(bg='white', fg='black')
    
    def apply_dark_theme(self):
        self.root.configure(bg='#343541')
        self.main_container.configure(bg='#343541')
        self.sidebar.configure(bg='#202123')
        self.history_frame.configure(bg='#202123')
        self.history_canvas.configure(bg='#202123')
        self.history_scrollable_frame.configure(bg='#202123')
        self.chat_area.configure(bg='#343541')
        self.chat_display.configure(bg='#343541', fg='white')
        self.input_frame.configure(bg='#343541')
        self.input_field.configure(bg='#40414F', fg='white')
    
    def contact_support(self):
        messagebox.showinfo("Contact", "Please email support@aiassistant.com for assistance.")
    
    def process_input(self):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        self.add_message("You", user_input, "#89B4FA")
        self.input_field.delete(0, tk.END)
        
        response = None
        for key in self.responses:
            if key in user_input.lower():
                response = random.choice(self.responses[key])
                break
        
        if not response:
            response = random.choice(self.responses["default"])
        
        self.add_message("AI Assistant", response, "#19C37D")
   
    def calculate_expression(self, expr):
        """Safely evaluate a mathematical expression and return the result."""
        try:
            # Replace ^ with ** for exponentiation
            expr = expr.replace('^', '**')
            
            # Security: Only allow basic math operations and numbers
            allowed_chars = set('0123456789+-*/.()% ')
            if not all(c in allowed_chars for c in expr):
                return "Invalid math expression. Only numbers and + - * / ^ % ( ) are allowed."
            
            # Evaluate the expression safely
            result = eval(expr, {'__builtins__': None}, {})
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Error: Division by zero!"
        except Exception as e:
            return f"Error: {str(e)}"

    def process_input(self):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        self.add_message("You", user_input, "#89B4FA")
        self.input_field.delete(0, tk.END)
        
        response = None
        
        # Check if the input is a math expression (contains operators)
        math_operators = ['+', '-', '*', '/', '^', '%']
        if any(op in user_input for op in math_operators):
            response = self.calculate_expression(user_input)
        else:
            # Default responses (existing logic)
            for key in self.responses:
                if key in user_input.lower():
                    response = random.choice(self.responses[key])
                    break
            
            if not response:
                response = random.choice(self.responses["default"])
        
        self.add_message("AI Assistant", response, "#19C37D")
        
        if user_input.lower() == 'bye':
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.root.destroy()

    # ... (keep all other methods unchanged) ...    
        
    def voice_command(self):
        with sr.Microphone() as source:
            self.add_message("AI Assistant", "Listening...", "#19C37D")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                self.add_message("You", command, "#89B4FA")
                self.process_voice_command(command)
            except sr.UnknownValueError:
                self.add_message("AI Assistant", "Sorry, I couldn't understand. Please try again.", "#FF6B6B")
            except sr.RequestError:
                self.add_message("AI Assistant", "Could not request results, check your connection.", "#FF6B6B")
    
    def process_voice_command(self, command):
        response = None
        for key in self.responses:
            if key in command.lower():
                response = random.choice(self.responses[key])
                break
        
        if not response:
            response = random.choice(self.responses["default"])
        
        self.add_message("AI Assistant", response, "#19C37D")
    
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            LoginPage(self.root, self.on_login_success)

if __name__ == "__main__":
    root = tk.Tk()
    
    def on_login_success(username):
        for widget in root.winfo_children():
            widget.destroy()
        AnimatedChatBot(root, username)
    
    LoginPage(root, on_login_success)
    root.mainloop()
