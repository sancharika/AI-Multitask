---
title: AI Blogger
emoji: 👀
colorFrom: purple
colorTo: yellow
sdk: streamlit
sdk_version: 1.31.1
app_file: app.py
pinned: false
---
# AI MultiTask

AI MultiTask is a Streamlit-based application that offers multiple AI-powered functionalities including blogging, summarization, and applicant tracking system (ATS). It allows users to perform various tasks related to text processing and analysis using AI models.

## Features

### Blogging
- Generate blog posts on a given topic with desired tone and language.
- Options to specify writing style (for researchers, data scientists, common people).
- Automatic generation of blog content within a specified word limit.
- Ability to input text or dictate using voice.

### Summarization
- Generate summaries of input text with desired tone and language.
- Options to specify the writing style (for researchers, data scientists, common people).
- Automatic summarization within a specified word limit.
- Input text or dictate using voice.

### Applicant Tracking System (ATS)
- Evaluate resumes against job descriptions.
- Provide professional evaluations highlighting strengths and weaknesses.
- Calculate percentage match between the resume and job description.
- Input text or upload documents for analysis.

## Project Structure

- **app.py**: Main script for the Streamlit UI and integration of different functionalities.
- **blogger.py**: Module for generating blog posts using AI models.
- **gist.py**: Module for generating summaries of input text.
- **ats.py**: Module for evaluating resumes against job descriptions using AI models.

## Setup and Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/sancharika/AI-Blogger.git
    ```

2. Navigate to the project directory:

    ```bash
    cd AI-Blogger
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
   - Create a `.env` file and add your Google API key.

5. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

6. Interact with the application by selecting the desired task and providing input accordingly.

## Dependencies

- Streamlit
- python-dotenv
- google.generativeai
- pdfplumber
- docx
- speech_recognition

Feel free to contribute to this project by submitting pull requests or reporting issues. Happy multitasking with AI! 🤖📝🔍