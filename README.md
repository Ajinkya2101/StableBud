# StableBud
StableBud is an interactive desktop application that generates images from text prompts using the Stable Diffusion model. The app also includes speech-to-text functionality, allowing users to input prompts via voice commands.

![Screenshot 2024-10-31 192138](https://github.com/user-attachments/assets/efdb2736-ccc9-4c6d-be2c-791467410a6e)


Features:

Speech-to-Image Generation: Convert spoken descriptions into image prompts using Google Speech Recognition.

Custom Prompt Entry: Type or dictate the prompt you wish to convert into an image.

Stable Diffusion Integration: Leverages Hugging Face's Stable Diffusion model for high-quality image generation.

Responsive UI: User-friendly and visually appealing interface built with customtkinter.

Prerequisites:

Before running the app, ensure you have the following installed:

Python 3.7+

torch and torchvision for model inference

customtkinter for the UI

Hugging Face Transformers and Diffusers libraries

PIL (Pillow) for image handling

SpeechRecognition and PyAudio for speech-to-text functionality

Install these dependencies using:

bash

pip install torch torchvision customtkinter diffusers transformers Pillow SpeechRecognition pyaudio

Setup and Usage:

1. Set Up Authentication
  
2. Obtain your Hugging Face API token and place it in a file named authtoken.py with the following content:
  python
  auth_token = "<your_hugging_face_token>"

3. Run the App
   
Start the application by running:

bash

  python app.py

How to Use

Enter Prompt: Type a prompt or use the microphone button to dictate a description.

Generate Image: Click Generate Image to create an image based on the prompt.

Clear Prompt: Click Clear Prompt to reset the input field.

Viewing Generated Images

The generated images appear in the display area. Images are also saved locally as generatedimage.png.

File Structure:

app.py: Main application code.

authtoken.py: File storing Hugging Face API token.

generatedimage.png: Generated image output file.

Libraries Used:

customtkinter for the enhanced tkinter-based UI

torch, diffusers for Stable Diffusion model inference

SpeechRecognition for voice input

Pillow for image manipulation
