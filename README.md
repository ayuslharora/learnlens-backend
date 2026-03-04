# LearnLens 🎓✨

LearnLens is a smart Chrome Extension powered by an AI backend that transforms how you study. 

By integrating directly into your browser, LearnLens allows you to instantly highlight complex concepts on any webpage for detailed AI explanations, instantly generate flashcards from PDFs, and take smart quizzes tailored to prioritize the topics you struggle with most.

---

## 🌟 Key Features

### 🖥️ Smart Dashboard
A fully responsive, dark-mode ready bento grid layout organizing your study planner, profile stats, and flashcard clusters into one seamless view.
![Dashboard UI](./dashboard-demo.png) *(UI Screenshot Placeholder)*

### 🔍 Instant Highlight Explanations
Highlight any text on any webpage. LearnLens intercepts the highlight and offers an interactive popup with instant AI-powered breakdowns of the concept.

### 📚 Auto-Generated Flashcards
Upload a PDF textbook or highlight web text to instantly generate intelligent flashcards. LearnLens automatically groups them by topic and features an integrated spaced-repetition tracking system right in your extension dashboard.

### 🧠 Smart Daily Quizzes
Prepare for exams with AI-generated multiple-choice tests. The built-in algorithm monitors your correct/incorrect ratios and actively focuses on prioritizing the topics you struggle with most. 

### 🔄 Anki Export Support
Seamlessly export all your AI-generated clustered flashcards into a `.csv` format ready for Anki ingestion.

---

## 🛠️ Tech Stack

### Frontend (Chrome Extension)
* **React** + **Vite**
* Custom Glassmorphic CSS Framework
* Chrome Manifest V3 APIs (Local Storage Sync)
* `react-markdown`

### Backend (API Server)
* **Python** + **FastAPI**
* Hosted on **Render** Cloud
* **Groq API** Integration for lightning-fast LLM processing
* PyMuPDF (fitz) for document parsing

---

## 📦 How to Install the Extension

The easiest way to use LearnLens is to download the compiled extension from our **Releases** page.

1. Go to the [Releases Tab](https://github.com/ayuslharora/learnlens-backend/releases) and download the `learnlens-extension-vX.X.X.zip` file attached to the latest release.
2. Unzip the downloaded file. It will contain an entire `dist` subfolder.
3. Open Google Chrome and type `chrome://extensions/` in the URL bar.
4. Toggle on **Developer mode** in the top-right corner.
5. Click **Load unpacked** in the top-left corner.
6. Select the extracted `dist` folder.
7. Click the extension puzzle piece icon in Chrome and **pin LearnLens** to your bar!

---

## 🚀 Running the Backend Locally

If you wish to run the FastAPI backend locally for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/ayuslharora/learnlens-backend.git
   cd learnlens-backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

*Thank you for exploring LearnLens! Enjoy smarter studying.*
