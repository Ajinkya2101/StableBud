import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from authtoken import auth_token
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
import speech_recognition as sr
import threading

class StableBudApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("750x850")
        self.app.title("Speech-to-Image Generator")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.setup_ui()
        self.setup_model()

    def setup_ui(self):
        # Title Label
        title = ctk.CTkLabel(self.app, text="Speech-to-Image Generator", text_font=("Arial", 28, "bold"))
        title.pack(pady=20)

        # Prompt Input Frame
        input_frame = ctk.CTkFrame(self.app, fg_color="gray20", corner_radius=8)
        input_frame.pack(pady=15, padx=20, fill="x", anchor="center")

        # Text Entry for Prompt
        self.prompt = ctk.CTkEntry(input_frame, height=40, width=500, text_font=("Arial", 16), placeholder_text="Enter prompt or use the mic")
        self.prompt.grid(row=0, column=0, padx=(10, 5), pady=10)

        # Microphone Button
        mic_button = ctk.CTkButton(input_frame, text="🎤", width=50, height=40, command=self.record_audio, fg_color="gray30")
        mic_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        # Button Frame
        button_frame = ctk.CTkFrame(self.app, fg_color="gray20", corner_radius=8)
        button_frame.pack(pady=10)

        # Generate and Clear Buttons
        generate_button = ctk.CTkButton(button_frame, height=40, width=150, text="Generate Image", text_font=("Arial", 16), command=self.generate)
        generate_button.grid(row=0, column=0, padx=10, pady=10)

        clear_button = ctk.CTkButton(button_frame, height=40, width=150, text="Clear Prompt", text_font=("Arial", 16), command=self.clear_prompt)
        clear_button.grid(row=0, column=1, padx=10, pady=10)

        # Image Display Frame
        image_frame = ctk.CTkFrame(self.app, width=512, height=512, fg_color="gray20", corner_radius=8)
        image_frame.pack(pady=20)

        self.image_label = ctk.CTkLabel(image_frame, text="Generated image will appear here", text_font=("Arial", 14), text_color="gray70")
        self.image_label.pack(expand=True, fill="both")

        # Status Label
        self.status_label = ctk.CTkLabel(self.app, text="", text_font=("Arial", 12, "italic"), text_color="gray70")
        self.status_label.pack(pady=10)

    def setup_model(self):
        modelid = "CompVis/stable-diffusion-v1-4"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = StableDiffusionPipeline.from_pretrained(modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)
        self.pipe.to(device)

    def generate(self):
        self.status_label.configure(text="Generating image...", text_color="orange")
        prompt_text = self.prompt.get()
        
        def generate_image():
            with autocast("cuda"):
                image = self.pipe(prompt_text, guidance_scale=8.5)["sample"][0]
            
            image.save('generatedimage.png')
            img = Image.open("generatedimage.png")
            img = img.resize((512, 512))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk, text="")
            self.image_label.image = img_tk
            self.status_label.configure(text="Image generated!", text_color="green")

        threading.Thread(target=generate_image).start()

    def clear_prompt(self):
        self.prompt.delete(0, "end")
        self.status_label.configure(text="Prompt cleared", text_color="blue")

    def record_audio(self):
        self.status_label.configure(text="Listening...", text_color="orange")
        
        def record():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            
            try:
                text = r.recognize_google(audio)
                current_text = self.prompt.get()
                if current_text:
                    self.prompt.insert("end", " " + text)
                else:
                    self.prompt.insert(0, text)
                self.status_label.configure(text="Speech recognized!", text_color="green")
            except sr.UnknownValueError:
                self.status_label.configure(text="Could not understand audio", text_color="red")
            except sr.RequestError as e:
                self.status_label.configure(text=f"Request error: {e}", text_color="red")

        threading.Thread(target=record).start()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = StableBudApp()
    app.run()
