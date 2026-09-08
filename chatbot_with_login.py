import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

# Load credentials from JSON file
def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"username": "admin", "password": "1234"}

class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.credentials = load_credentials()
        self.root.title("Login ELIZA.Ai")
        self.root.geometry("400x300")
        self.root.configure(bg='black')
        
        tk.Label(root, text="Login ELIZA.Ai", font=('Arial', 20, 'bold'), bg='black', fg='white').pack(pady=20)
        
        tk.Label(root, text="Username:", font=('Arial', 12), bg='black', fg='white').pack()
        self.username_entry = tk.Entry(root, font=('Arial', 12))
        self.username_entry.pack(pady=5)
        
        tk.Label(root, text="Password:", font=('Arial', 12), bg='black', fg='white').pack()
        self.password_entry = tk.Entry(root, font=('Arial', 12), show='*')
        self.password_entry.pack(pady=5)
        
        self.login_button = tk.Button(root, text="Login", font=('Arial', 12, 'bold'), bg='#89B4FA', fg='black', command=self.check_login)
        self.login_button.pack(pady=20)
        
        self.root.bind('<Return>', lambda event: self.check_login())
    
    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == self.credentials["username"] and password == self.credentials["password"]:
            messagebox.showinfo("Success", "Login Successful!")
            self.root.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password")

class AnimatedChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("500x700")
        self.root.configure(bg='black')

        # Chat history storage
        self.chat_history = []

        # Create main frame 
        self.main_frame = tk.Frame(root, bg='black')          
        self.main_frame.pack(fill='both', expand=True)

        # Title with glow effect
        self.title_label = tk.Label(self.main_frame, 
                                  text="Hello, ELIZA", 
                                  font=('Arial', 19, 'bold'),
                                  bg='black', 
                                  fg='#89B4FA')
        self.title_label.pack(pady=10)

        # Robot face canvas
        self.canvas = tk.Canvas(self.main_frame, width=300, height=300,
                              bg='black', highlightthickness=0)
        self.canvas.pack(pady=20)

        # Chat display
        self.chat_frame = tk.Frame(self.main_frame, bg='black')
        self.chat_frame.pack(fill='both', expand=True, padx=20)

        # Create chat display with scrollbar
        self.chat_display = tk.Text(self.chat_frame, 
                                  height=10,
                                  width=30,
                                  bg='black',
                                  fg='white',
                                  font=('Consolas', 11),
                                  wrap=tk.WORD,
                                  padx=20,
                                  pady=10)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack chat display and scrollbar
        self.chat_display.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.chat_display.config(state='disabled')

        # Configure message styles
        self.chat_display.tag_configure("user_msg", 
                                      background='#343541',
                                      font=('Consolas', 15, 'bold'),  
                                      justify='right',
                                      lmargin1=100,
                                      lmargin2=100)
        
        self.chat_display.tag_configure("bot_msg", 
                                      background='#444654',
                                      font=('Helvetica', 12, 'bold'),  
                                      justify='left',
                                      lmargin1=20,
                                      lmargin2=20)

        # Input area
        self.input_frame = tk.Frame(self.main_frame, bg='black')
        self.input_frame.pack(fill='x', padx=20, pady=(0, 20))

        self.input_field = tk.Entry(self.input_frame,
                                  font=('Consolas', 14),  
                                  bg='#343541',
                                  fg='white',
                                  insertbackground='white',
                                  relief=tk.FLAT)
        self.input_field.pack(side='left', fill='x', expand=True, ipady=10)  

        self.send_button = tk.Button(self.input_frame,
                                   text="Send",
                                   font=('Arial', 11, 'bold'),  
                                   bg='#89B4FA',
                                   fg='#1E1E2E',
                                   relief=tk.FLAT,
                                   command=self.process_input)
        self.send_button.pack(side='right', padx=(10, 0), ipadx=20, ipady=5)

        self.input_field.bind('<Return>', lambda e: self.process_input())

        # Clear chat history button
        self.clear_button = tk.Button(self.main_frame,
                                    text="Clear History",
                                    font=('Arial', 11, 'bold'),
                                    bg='#FF6B6B',
                                    fg='#1E1E2E',
                                    relief=tk.FLAT,
                                    command=self.clear_chat_history)
        self.clear_button.pack(pady=10)

        # Initialize robot animation
        self.eye_position = 0
        self.eye_direction = 1
        self.blink_state = 0
        self.draw_robot()
        self.animate()
  
        self.responses = {
            "hello": ["Hey! How can I help you?", "Hello! 😊"],
            "how are you": ["I'm doing great, thanks!", "I'm good, how about you?"],
            "bye": ["Goodbye!", "See you later!", "Have a great day!"],
            "who are you": ["I'm ChatBot", "You can call me ChatBot or also Your ELIZA!"],
            "time": [f"It's currently {datetime.now().strftime('%I:%M %p')}"],
            "date":[f"Today is {datetime.now().strftime('%B %d, %Y')}"],
            "help": ["You can ask me about the time, date, or else!"],
            "what is": ["It is  an interpreted, object-oriented, high-level programming language with dynamic semantics. Its high-level built in data structures. Python's simple, easy to learn syntax emphasizes readability and therefore reduces the cost of program maintenance."],
            "mother" :["your mother  is Uma Soni"],
            "father" :["your father is Tushar Soni"],
            "sister" :["your sister is Nidhi Soni"],
            "who is indian prime minister" :["your Prime Minister is Narendra Modi"],
            "link" :["https://www.google.com"],
            "write a python program" :["print('Hello, World!')" ],
            "Made" : ["This chatbot was made by Bhavya Soni"],
            "weather": ["It's a nice day today!", "The weather is perfect!"],
            "thanks": ["You're welcome!", "Anytime!", "My pleasure!"],
            "num": ["Let me calculate that for you..."],
            "default": ["I'm not sure about that.", "Could you replace that?", "Interesting, tell me more."]
        }

    def draw_robot(self):
        self.canvas.delete("all")
        
        # Create glowing background effect
        for i in range(3):
            self.canvas.create_oval(
                40-i*5, 40-i*5, 260+i*5, 260+i*5,
                fill='', outline='#89B4FA',
                width=2, stipple='gray50'
            )
        
        # Main face plate - hexagonal shape
        face_coords = [
            100, 50,  # top
            200, 50,
            230, 150,  # right
            200, 250,  # bottom
            100, 250,
            70, 150   # left
        ]
        self.canvas.create_polygon(face_coords, 
                                 fill='#313244', 
                                 outline='#89B4FA',
                                 width=2)
        
        # Secondary face plate
        inner_coords = [
            110, 70,
            190, 70,
            210, 150,
            190, 230,
            110, 230,
            90, 150
        ]
        self.canvas.create_polygon(inner_coords,
                                 fill='#1E1E2E',
                                 outline='#89B4FA',
                                 width=1)
        
        # Glowing energy core
        core_y = 150
        for i in range(3):
            self.canvas.create_oval(
                145-i*2, core_y-5-i*2,
                155+i*2, core_y+5+i*2,
                fill='' if i > 0 else '#F38BA8',
                outline='#89B4FA',
                width=1
            )
        
        # Eyes with high-tech look
        eye_y = 120 + self.eye_position
        for side in [-1, 1]:
            x = 150 + side * 35
            
            # Eye frame
            self.canvas.create_rectangle(x-20, eye_y-15,
                                      x+20, eye_y+15,
                                      fill='#1E1E2E',
                                      outline='#89B4FA',
                                      width=2)
            
            # Eye glow
            if self.blink_state == 0:
                # Main eye light
                self.canvas.create_rectangle(x-15, eye_y-10,
                                          x+15, eye_y+10,
                                          fill='#89B4FA',
                                          outline='')
                
                # Eye shine
                self.canvas.create_rectangle(x-12, eye_y-8,
                                          x+12, eye_y+8,
                                          fill='#74C7EC',
                                          outline='')
                
                # Center dot
                self.canvas.create_oval(x-3, eye_y-3,
                                      x+3, eye_y+3,
                                      fill='#F38BA8',
                                      outline='')
            
            # Eye scan lines
            if self.blink_state == 0:
                for i in range(3):
                    scan_y = eye_y - 10 + i * 10
                    self.canvas.create_line(x-15, scan_y,
                                          x+15, scan_y,
                                          fill='#89B4FA',
                                          width=1)
        
        # Mouth/Speaker
        mouth_y = 190
        # Speaker grill
        for i in range(3):
            y = mouth_y + i * 10
            self.canvas.create_rectangle(120, y, 180, y+5,
                                      fill='#89B4FA',
                                      outline='#89B4FA',
                                      width=1)
        
        # Side vents
        for side in [-1, 1]:
            x = 150 + side * 70
            for i in range(3):
                vent_y = 130 + i * 20
                self.canvas.create_rectangle(x-10, vent_y,
                                          x+10, vent_y+10,
                                          fill='#313244',
                                          outline='#89B4FA',
                                          width=1)
                # Vent glow
                if random.random() < 0.5:
                    self.canvas.create_rectangle(x-8, vent_y+2,
                                              x+8, vent_y+8,
                                              fill='#F38BA8',
                                              outline='')
        
        # Top antenna
        self.canvas.create_line(150, 50, 150, 30,
                              fill='#89B4FA', width=2)
        self.canvas.create_oval(145, 25, 155, 35,
                              fill='#F38BA8',
                              outline='#89B4FA',
                              width=2)
        
        # Circuit patterns
        for i in range(4):
            start_x = 90 + i * 40
            self.canvas.create_line(start_x, 250,
                                  start_x + 20, 250,
                                  start_x + 20, 240,
                                  fill='#89B4FA', width=1)

    def animate(self):
        # Enhanced eye animation
        self.eye_position += 0.5 * self.eye_direction
        if abs(self.eye_position) > 5:
            self.eye_direction *= -1
        
        # More natural blinking
        if random.random() < 0.02:  # 2% chance to blink each frame
            self.blink_state = 1
        else:
            self.blink_state = 0
        
        # Add subtle head movement
        self.canvas.move("all", random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.draw_robot()
        self.canvas.after(50, lambda: self.canvas.move("all", 0, 0))  # Reset position
        
        self.root.after(50, self.animate)

    def create_assistant_logo(self, canvas, x, y, size=30):
        # Create circular background
        canvas.create_oval(
            x, y,
            x + size, y + size,
            fill='#444654',
            outline='#89B4FA',
            width=2
        )
        
        # Create AI text
        canvas.create_text(
            x + size/2,
            y + size/2,
            text="AI",
            font=('Arial', int(size/3), 'bold'),
            fill='#89B4FA'
        )

    def add_message(self, message, sender, color='white'):
        self.chat_display.config(state='normal')
        self.chat_display.insert('end', f"{sender}: ", ("bold",))
        self.chat_display.insert('end', f"{message}\n", ("color",))
        self.chat_display.tag_config("bold", font=("Consolas", 12, "bold"))
        self.chat_display.tag_config("color", foreground=color)
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')

        # Add message to chat history
        self.chat_history.append({"sender": sender, "message": message})

    def process_input(self):
        user_input = self.input_field.get().strip().lower()
        if not user_input:
            return

        self.add_message(user_input, "You", "#89B4FA")
        self.input_field.delete(0, 'end')

        # Check for calculation request
        if "calculate" in user_input:
            response = self.calculate(user_input)
            self.add_message(response, "Bot")
            return
        
        response = None
        for key in self.responses:
            if key in user_input:
                response = random.choice(self.responses[key])
                if callable(response):
                    response = response()
                break
        
        if not response:
            response = random.choice(self.responses["default"])
        
        self.add_message(response, "Bot", "#FFD700")

        if user_input == 'bye':
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.root.destroy()

    def clear_chat_history(self):
        # Clear chat history and display
        self.chat_history.clear()
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, 'end')
        self.chat_display.config(state='disabled')

    def calculate(self, expression):
        try:
            # Remove the word "calculate" and trim whitespace
            expression = expression.replace("calculate", "").strip()
            
            # Split the expression into parts
            parts = expression.split()
            
            if len(parts) != 3:
                return "Please use the format: number operator number (e.g., 5 + 3)"
            
            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])
            
            result = None
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Cannot divide by zero!"
                result = num1 / num2
            else:
                return "Supported operators are: +, -, *, /"
            
            # Format result to avoid long decimal places
            if result.is_integer():
                return f"{expression} = {int(result)}"
            return f"{expression} = {result:.2f}"
            
        except ValueError:
            return "Please provide valid numbers (e.g., calculate 5 + 3)"
        except Exception as e:
            return "Sorry, I couldn't calculate that. Please try again."
        
        

if __name__ == "__main__":
    login_root = tk.Tk()
    def open_chat():
        chat_root = tk.Tk()
        AnimatedChatBot(chat_root)
        chat_root.mainloop()
    
    LoginPage(login_root, open_chat)
    login_root.mainloop()