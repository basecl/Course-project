import tkinter as tk
from tkinter import scrolledtext
import threading


class GUI:
    def __init__(self, ai_chat_model, audio_transcriber):
        self.application_window = tk.Tk()
        self.application_window.title("Chat Application")
        self.conversation_display = scrolledtext.ScrolledText(self.application_window, width=60, height=20)
        self.conversation_display.pack(fill='both', expand=True, padx=10, pady=10)
        self.user_input_entry = tk.Entry(self.application_window, width=50)
        self.user_input_entry.pack(padx=10, pady=10)
        self.submit_button = tk.Button(self.application_window, text="Submit",
                                       command=self.generate_and_display_response)
        self.submit_button.pack(side='bottom', padx=10, pady=5)
        self.record_button = tk.Button(self.application_window, text="Record", command=self.start_recording)
        self.record_button.pack(side='bottom', padx=10, pady=5)
        self.application_window.bind("<F1>", self.f1_key_pressed)
        self.user_input_entry.bind("<Return>", self.generate_and_display_response)
        self.ai_chat_model = ai_chat_model
        self.audio_transcriber = audio_transcriber

    def generate_and_display_response(self, event=None):
        user_input = self.user_input_entry.get().strip()
        if user_input:
            self.conversation_display.insert(tk.END, "\nUser: " + user_input + "\n")
            self.user_input_entry.delete(0, tk.END)
            threading.Thread(target=self.ai_chat_model.generate_response, args=(user_input, self)).start()

    def update_conversation_display(self, text):
        self.conversation_display.insert(tk.END, text)
        self.conversation_display.see(tk.END)

    def start_recording(self):
        transcription = self.audio_transcriber.transcribe_audio()
        with self.ai_chat_model.chat_lock:
            self.ai_chat_model.message_history.append({'role': 'user', 'content': transcription})
        self.conversation_display.insert(tk.END, "\nUser: " + transcription + "\n")
        threading.Thread(target=self.ai_chat_model.generate_response, args=(transcription, self)).start()

    def f1_key_pressed(self, event):
        transcription = self.audio_transcriber.transcribe_audio()
        with self.ai_chat_model.chat_lock:
            self.ai_chat_model.message_history.append({'role': 'user', 'content': transcription})
        self.conversation_display.insert(tk.END, "\nUser: " + transcription + "\n")
        threading.Thread(target=self.ai_chat_model.generate_response, args=(transcription, self)).start()

    def run(self):
        self.application_window.mainloop()
