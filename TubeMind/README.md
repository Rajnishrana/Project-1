TubeMind: AI-Powered YouTube Conversation Partner
Have you ever wanted to just "ask" a video for the information you need instead of scrubbing through the timeline? TubeMind makes that possible. It uses RAG (Retrieval-Augmented Generation) to pull transcripts, save them into a local memory, and let you have a real-time conversation with the content. Everything is powered by Google's Gemini 2.5 Flash Lite for a fast, grounded, and reliable experience.


What makes it special
•	Smart Transcript Extraction: Automatically grabs subtitles using updated 2026 protocols so you don't have to worry about broken scrapers.
•	Lite AI Engine: By using gemini-2.5-flash-lite, the app stays snappy and handles many more requests without hitting quota limits.
•	Reliable Memory: Uses FAISS and HuggingFace Embeddings to make sure the AI actually sticks to what was said in the video rather than making things up.
•	Modular Build: The code is organized into a clean 2026 design, keeping the data scraping, text processing, and AI logic strictly separated.


The Tech Stack
•	Frontend: Streamlit for a clean, easy-to-use interface.
•	Brain: LangChain (2026 Modular Build) orchestrating the flow.
•	Model: Google Gemini 2.5 Flash Lite.
•	Language Understanding: HuggingFace (all-mpnet-base-v2).
•	Storage: FAISS (Local Vector DB).


Setup & Installation
Follow these steps to get TubeMind up and running on your local machine.

1. Prerequisites
•	Python 3.10 or higher.
•	A Google AI Studio API Key (you can grab one for free at the Google AI Studio website).
2. Clone the Project First, grab the code from GitHub:

Bash
git clone https://github.com/Rajnishrana/Project-1/tree/main/TubeMind
cd YT_Summarizer

3. Set up a Virtual Environment Keep your dependencies organized:
Bash

# For Windows users:
python -m venv venv
.\venv\Scripts\activate

# For Mac/Linux users:
python3 -m venv venv
source venv/bin/activate
4. Install Dependencies Install all the necessary libraries in one go:
Bash
pip install -r requirements.txt
5. Configure Your Environment Create a file named .env in your root directory and drop in your API key:
Plaintext
GOOGLE_API_KEY=your_actual_key_here
How to Run
Launch the app with a simple command:
Bash

streamlit run app.py
1.	Paste your favorite YouTube URL into the input box.
2.	Hit Process Video to let the AI "read" the transcript.
3.	Once the "Analysis Complete" message pops up, you’re ready! Start asking questions in the chat box.

