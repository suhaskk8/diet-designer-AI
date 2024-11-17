import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import time
import threading

# Configure Google Generative AI (using a valid API key)
api_key = "AIzaSyCYJll1AEGvcvT-9WJb2CnIcMcxiogeMb4"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def recipe(inp):
    prop = f"{inp}"
    response = model.generate_content(prop)
    return response.text

# Typing animation function
def type_message(text, chatbox, delay=0.01):
    for char in text:
        chatbox.insert(tk.END, char)
        chatbox.yview(tk.END)  # Scroll to the end
        chatbox.update()
        time.sleep(delay)
    chatbox.insert(tk.END, "\n\n")  # Add an extra line break for spacing
    chatbox.yview(tk.END)  # Ensure the chatbox scrolls to the bottom

# Display loading message until the bot replies
def show_loading_message(chatbox):
    loading_msg = "Bot is Processing..."
    chatbox.insert(tk.END, f"Bot: {loading_msg}\n\n")  # Add extra spacing
    chatbox.yview(tk.END)
    chatbox.update()

# Send message function
def send_message():
    user_message = user_input.get()
    if not user_message.strip():
        return
    
    # Display user message in the chatbox with some padding
    chatbox.insert(tk.END, f"You: {user_message}\n\n")  # Add extra space between exchanges
    user_input.delete(0, tk.END)
    
    # Show loading message while the bot is processing
    show_loading_message(chatbox)
    
    # Get the bot's response and display it with animation
    def get_bot_reply():
        try:
            bot_reply = recipe(user_message)
        except Exception as e:
            bot_reply = f"Error: {e}"
        
        # Clear the "loading" message and animate bot's reply
        chatbox.delete("end-3l", tk.END)  # Remove the last 3 lines (loading message + previous space)
        
        # Animate typing effect for the bot's reply
        chatbox.insert(tk.END, "\n\n")
        type_message(bot_reply, chatbox)
    
    # Run the bot reply in a separate thread to avoid freezing the UI
    threading.Thread(target=get_bot_reply).start()

# Send welcome message function
def send_welcome_message():
    welcome_message = "I am Diet Designer, what would you like to know?"
    type_message(welcome_message, chatbox)

# Create the main Tkinter window
root = tk.Tk()
root.title("Diet Designer")

# Set window background color
root.configure(bg='#f4f4f9')

# Chatbox (Scrolled Text)
chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=50, state='normal', bg="#fafafa", fg="#333", font=("Arial", 12))
chatbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
chatbox.tag_configure("user", foreground="blue")
chatbox.tag_configure("bot", foreground="green")

# User Input Entry
user_input = tk.Entry(root, width=40, font=("Arial", 12), relief="solid", bd=2, bg="#fff", fg="#333")
user_input.grid(row=1, column=0, padx=10, pady=10)

# Send Button with Hover Effect
def on_enter(e):
    send_button.config(bg="#4CAF50", fg="white")

def on_leave(e):
    send_button.config(bg="#f0f0f0", fg="black")

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12), relief="solid", bg="#f0f0f0", fg="black", width=10)
send_button.grid(row=1, column=1, padx=10, pady=10)
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

# Send the welcome message when the app starts
send_welcome_message()

# Run the Tkinter event loop
root.mainloop()
