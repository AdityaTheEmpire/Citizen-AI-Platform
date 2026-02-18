# Civil Engineering Insight Studio

A Streamlit app that analyzes uploaded civil engineering structure images with Gemini Vision.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create your environment file:
   ```bash
   cp .env.example .env
   ```
3. Update `.env` with your API key:
   ```env
   GOOGLE_API_KEY="YOUR_API_KEY_HERE"
   ```

## Run

```bash
streamlit run App.py
```

The app is typically available at <http://localhost:8501>.
