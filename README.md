# 📧 Cold Email Generator

An AI-powered **Cold Email Generator** built with Python, Streamlit, LangChain, Groq, and ChromaDB. The application reads a job posting from a URL or pasted job-description text, extracts relevant job details, finds related portfolio entries, and generates a professional, personalized email expressing interest in the role.

The email-generation prompt is configured for an MSc Data Science and Artificial Intelligence student at Himachal Pradesh University (HPU), seeking job and internship opportunities.

## ✨ Features

- **Job-posting input:** Enter a careers-page URL or paste the job description manually.
- **Webpage extraction:** Uses LangChain's `WebBaseLoader` to retrieve page content when a URL is provided.
- **Text cleaning:** Removes HTML tags, URLs, and unwanted characters before processing.
- **Job information extraction:** Uses an LLM to extract job roles, experience, skills, and descriptions as structured JSON.
- **Portfolio matching:** Uses ChromaDB to retrieve portfolio links associated with relevant skills.
- **Personalized email generation:** Produces a concise, professional application email tailored to the job or internship.
- **Streamlit interface:** Displays generated emails in a simple web interface.

## 🧰 Tech Stack

| Technology | Role |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| Groq API | Hosted LLM inference |
| Llama model | Job extraction and email generation |
| LangChain | Prompting, model orchestration, and webpage loading |
| ChromaDB | Persistent vector storage and similarity search |
| Pandas | Loading portfolio data from CSV |
| python-dotenv | Loading API credentials from environment variables |

**Model note:** The current code configures `llama-3.3-70b-versatile` through Groq. This is the model identifier used in the source code.

## 🔄 How It Works

1. **Provide a job posting:** Enter a job URL or paste the job description into the text area.
2. **Extract the content:** The app loads the webpage when a URL is used, then cleans the extracted text.
3. **Extract job details:** The LLM identifies job titles, experience requirements, skills, and descriptions in JSON format.
4. **Find relevant portfolio links:** The app queries the ChromaDB collection using the extracted skills and retrieves matching portfolio entries.
5. **Generate the email:** The LLM writes a professional job-application or internship email using the job details.
6. **Review the result:** The generated email appears in the Streamlit app.

## 📁 Project Structure

```text
Cold-Email-Generator/
├── main.py             # Streamlit application
├── chain.py            # LLM setup, job extraction, and email generation
├── portfolio.py        # CSV portfolio loading and ChromaDB retrieval
├── utils.py            # Text-cleaning utility
├── my_portfolio.csv    # Portfolio tech stacks and related links
├── .env                # Local API credentials; do not commit
├── .gitignore          # Files excluded from version control
└── README.md
```

The `vectorstore/` directory is created by ChromaDB at runtime to persist the portfolio collection.

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Cold-Email-Generator.git
cd Cold-Email-Generator
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository URL if needed.

### 2. Create and activate a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit langchain-community langchain-core langchain-groq chromadb pandas numpy python-dotenv beautifulsoup4
```

If your environment requires additional packages for webpage loading, install the missing dependency shown by the error message.

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get a key from the [Groq Console](https://console.groq.com/).

**Important:** Never commit `.env` or publish your API key. If a real key has been exposed, revoke it and create a replacement.

### 5. Configure the portfolio CSV path

The `Portfolio` class in `portfolio.py` currently uses a machine-specific absolute Windows path. Update its default path so it works from the repository directory, for example:

```python
def __init__(self, file_path="my_portfolio.csv"):
```

Make sure `my_portfolio.csv` is in the project root and contains the expected columns:

```csv
Techstack,Links
"Python, Django, MySQL",https://example.com/python-portfolio
"Machine Learning, Python, TensorFlow",https://example.com/ml-python-portfolio
```

Replace the example portfolio entries and links with your own real projects and portfolio URLs.

### 6. Run the application

From the project root, run:

```bash
streamlit run main.py
```

Open the local URL printed in the terminal (usually `http://localhost:8501`).

## 🖥️ Using the App

1. Open the Streamlit application.
2. Paste a careers-page URL into **Enter a Job Posting URL**, or paste the job description into the text area.
3. Click **Submit**.
4. Review the generated job details and email output.
5. Edit the email as needed before sending it.

If a website blocks scraping or the extracted text is too short, paste the job description manually.

## 🧩 Main Modules

- **`main.py`** — Provides the Streamlit UI, accepts a URL or manual job description, and coordinates the workflow.
- **`chain.py`** — Configures the Groq chat model, extracts job details as JSON, and generates the email.
- **`portfolio.py`** — Loads portfolio records from CSV, stores their tech-stack descriptions in ChromaDB, and retrieves matching links.
- **`utils.py`** — Cleans scraped or pasted text before it is sent to the model.
- **`my_portfolio.csv`** — Supplies the tech-stack descriptions and associated portfolio links used for retrieval.

## ⚠️ Current Limitations

- Some career websites block automated requests or render content with JavaScript, which may prevent extraction. Manual job-description input is provided as a fallback.
- The quality of extracted job details and generated emails depends on the supplied text and the LLM response.
- The portfolio CSV should contain valid, relevant portfolio information. Placeholder links will need to be replaced.
- The current email-generation prompt is tailored to an MSc Data Science and AI student applying for jobs and internships.
- Review generated content for accuracy and personalize it before sending.

## 🔐 Security

- Keep API keys in `.env` or a secure environment-variable manager.
- Add `.env`, virtual environments, and generated local data to `.gitignore`.
- Never publish credentials, private data, or client information in the repository.

Example `.gitignore` entries:

```gitignore
.env
venv/
.venv/
__pycache__/
*.py[cod]
vectorstore/
```

## 🚀 Future Improvements

- Add email tone and length controls.
- Add copy-to-clipboard and download options.
- Improve structured-output validation and error handling.
- Add support for multiple portfolio profiles.
- Add tests for text cleaning, job extraction, and portfolio retrieval.

## 👨‍💻 Author

**Your Name**

- GitHub: `https://github.com/YOUR_USERNAME`
- LinkedIn: `https://www.linkedin.com/in/YOUR_PROFILE/`

---

If this project is useful, consider giving the repository a ⭐ on GitHub.
