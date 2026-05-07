# AI Website Summarizer

An intelligent web application that uses Playwright and Google's Gemini AI to crawl websites, extract meaningful content, and generate concise, insightful summaries in real-time.

## 🚀 Features

- **Real-Time Streaming**: Watch the AI summary generate word-by-word as it streams directly from the Gemini model.
- **Deep Web Crawling**: Uses Playwright to render JavaScript-heavy websites, allowing it to see exactly what a real user sees.
- **Multi-Page Support**: Capable of crawling multiple pages within the same domain to gather comprehensive context.
- **Smart Link Extraction**: Extracts and verifies real links from the website to provide accurate references without hallucinating URLs.
- **Modern UI**: A sleek, responsive frontend built with React, Vite, and Tailwind CSS (or custom CSS).
- **Dockerized for Production**: Pre-configured Dockerfile optimized for deployment on Hugging Face Spaces or other containerized environments.

## 🛠️ Tech Stack

### Backend
- **Python 3**
- **FastAPI**: High-performance API framework for serving endpoints and handling streaming responses.
- **Playwright**: Headless browser automation for robust web scraping, scrolling, and rendering JS-heavy sites.
- **BeautifulSoup4**: HTML parsing and cleaning to extract raw text content.
- **Gemini 2.5 Flash**: Google's LLM (via OpenAI SDK compatibility) for fast, intelligent summarization.

### Frontend
- **React 19**: Modern frontend framework.
- **Vite**: Lightning-fast build tool and development server.
- **React Markdown**: For rendering the AI-generated markdown summaries with proper formatting.

## 📋 Prerequisites

- Node.js (v18+)
- Python (3.9+)
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/website-summarizer.git
cd website-summarizer
```

### 2. Backend Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Set up your environment variables:
Create a `.env` file in the root directory and add your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the backend server:
```bash
python main.py
```
*The API will run on http://127.0.0.1:8000*

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```
*The React app will be available on http://localhost:5173*

## 🐳 Docker Deployment (Hugging Face Spaces)

This project is configured out-of-the-box for deployment on Hugging Face Spaces or any Docker-compatible platform. The provided `Dockerfile` uses the official Playwright image and handles permission requirements.

```bash
# Build the Docker image
docker build -t website-summarizer .

# Run the container locally (maps port 7860)
docker run -p 7860:7860 website-summarizer
```

## 📝 Usage

1. Open the frontend application in your browser.
2. Enter the URL of the website you want to summarize.
3. Configure settings like `max_pages` to control how deep the crawler should go.
4. Click "Summarize" and watch the AI process the website and stream the results back to you!

## 📜 License

This project is open-source and available under the MIT License.
