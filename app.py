import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from gtts import gTTS
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Create the main application window
app = tk.Tk()
app.title("PDF Text Summarizer & Translator")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    total_pages = len(pdf_reader.pages)

    for i, page in enumerate(pdf_reader.pages):
        text += page.extract_text()
        # Update the progress bar
        progress = (i + 1) / total_pages * 100
        progress_bar["value"] = progress
        app.update_idletasks()

    return text

# Function to summarize text
def generate_summary(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_text = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Calculate word frequencies
    word_freq = nltk.FreqDist(filtered_text)

    # Get the most common words (you can adjust the number)
    most_common_words = [word for word, freq in word_freq.most_common(10)]

    # Extract sentences containing the most common words
    summary_sentences = [sentence for sentence in sentences if any(word in sentence.lower() for word in most_common_words)]

    # Join the summary sentences
    summary = " ".join(summary_sentences)

    return summary

# Function to translate text to Hindi
def translate_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi').text
    return translated_text

# Function to handle PDF file upload
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        text = extract_text_from_pdf(file_path)
        summary = generate_summary(text)
        translated_text = translate_to_hindi(summary)

        # Display the summary and translated text
        text_widget.delete(1.0, "end")  # Clear previous content
        text_widget.insert("end", summary)
        translated_text_widget.delete(1.0, "end")  # Clear previous content
        translated_text_widget.insert("end", translated_text)

        # Enable the download audio and image buttons
        download_audio_button.config(state="normal")
        download_image_button.config(state="normal")
        download_summary_button.config(state="normal")
        download_non_translated_audio_button.config(state="normal")

# Function to download translated audio to a file
def download_translated_audio():
    translated_text = translated_text_widget.get("1.0", "end-1c")  # Get translated text
    if translated_text:
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            tts = gTTS(translated_text)
            tts.save(file_path)
            messagebox.showinfo("Download Complete", "Translated audio has been saved to the selected file.")

# Function to download non-translated audio to a file
def download_non_translated_audio():
    summary_text = text_widget.get("1.0", "end-1c")  # Get summary text
    if summary_text:
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            tts = gTTS(summary_text)
            tts.save(file_path)
            messagebox.showinfo("Download Complete", "Non-translated audio has been saved to the selected file.")

# Function to create an image from text
def create_text_image(text, output_image_path):
    image_width = 800
    image_height = 600
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Break the text into lines to fit in the image
    max_text_length = 100  # Maximum characters per line
    lines = [text[i:i + max_text_length] for i in range(0, len(text), max_text_length)]
    
    line_height = 30
    y = 50  # Initial y-coordinate

    for line in lines:
        draw.text((50, y), line, fill=text_color, font=font)
        y += line_height

    image.save(output_image_path)

# Function to create and download an image
def create_and_download_image():
    summary_text = text_widget.get("1.0", "end-1c")  # Get text from the text widget
    if summary_text:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image Files", "*.png")])
        if file_path:
            create_text_image(summary_text, file_path)
            messagebox.showinfo("Download Complete", "Image has been saved to the selected file.")

# Function to download the summary as a text file
def download_summary_as_text():
    summary_text = text_widget.get("1.0", "end-1c")  # Get text from the text widget
    if summary_text:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(summary_text)
            messagebox.showinfo("Download Complete", "Summary has been saved as a text file.")

# Create and configure widgets
label = tk.Label(app, text="Upload a PDF file to summarize and translate:")
label.pack(pady=10)

upload_pdf_button = tk.Button(app, text="Upload PDF", command=upload_pdf)
upload_pdf_button.pack(pady=10)

progress_bar = ttk.Progressbar(app, mode='determinate', length=300)
progress_bar.pack(pady=10)

# Text widget for displaying the summary
text_widget = tk.Text(app, height=10, width=50)
text_widget.pack(pady=10)

# Button to download translated audio
download_audio_button = tk.Button(app, text="Download Translated Audio", command=download_translated_audio, state="disabled")
download_audio_button.pack(pady=10)

# Button to download non-translated audio
download_non_translated_audio_button = tk.Button(app, text="Download Non-Translated Audio", command=download_non_translated_audio, state="disabled")
download_non_translated_audio_button.pack(pady=10)

# Button to create and download an image
download_image_button = tk.Button(app, text="Download Image", command=create_and_download_image, state="disabled")
download_image_button.pack(pady=10)

# Button to download the summary as a text file
download_summary_button = tk.Button(app, text="Download Summary as Text", command=download_summary_as_text, state="disabled")
download_summary_button.pack(pady=10)

# Text widget for displaying the translated text
translated_text_widget = tk.Text(app, height=10, width=50)
translated_text_widget.pack(pady=10)

# Start the main loop
app.mainloop()
