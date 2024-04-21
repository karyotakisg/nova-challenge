import tkinter as tk
from tkinter import scrolledtext
import claude_api
class GPTChatterApp:
    def __init__(self, master):
        self.master = master
        master.title("GPT Chatter")

        # Title
        self.title_label = tk.Label(master, text="Chatter of News", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame to contain the chat history
        self.chat_frame = tk.Frame(master)
        self.chat_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Text area for displaying chat history
        self.chat_history = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, width=60, height=20)
        self.chat_history.pack(expand=True, fill='both')
        self.chat_history.configure(state='disabled')

        # Label for the user input
        self.input_label = tk.Label(master, text="Ask a Question:")
        self.input_label.pack()

        # Entry widget for user input
        self.user_input = tk.Text(master, wrap="word", width=60, height=3)
        self.user_input.pack()

        # Submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.get_response)
        self.submit_button.pack(pady=9)



    def get_user_input(self):
        return self.user_input.get("1.0", tk.END).strip()
    
    def get_response(self):
        question = self.get_user_input()
        response = claude_api.call_api(question)  # Replace with actual response logic

        # Display question and response in the chat history
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, "\nYou: " + question)
        self.chat_history.insert(tk.END, "\nGPT Chatter: " + str(response))
        self.chat_history.configure(state='disabled')

        # Clear the input field after submitting
        self.user_input.delete("1.0", tk.END)

def main():
    root = tk.Tk()
    app = GPTChatterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
