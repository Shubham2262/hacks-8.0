# PDF Text Summarizer & Translator

This is a Python application that allows users to upload PDF documents, extract text from them, 
generate summaries, and translate those summaries to Hindi. It also provides options to download the translated audio, 
non-translated audio, summary image, and summary text file.

## Features

- Extract text from uploaded PDF documents.
- Generate summaries based on extracted text.
- Translate summaries to Hindi.
- Download translated audio.
- Download non-translated audio.
- Create and download summary images.
- Download summary as a text file.

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- Python 3.x
- `PyPDF2` library for PDF processing.
- `nltk` library for natural language processing.
- `gtts` library for text-to-speech conversion.
- `googletrans` library for text translation.
- `Pillow` (PIL) library for image creation.

You can install these dependencies using pip:

```bash
pip install PyPDF2 nltk gtts googletrans pillow

