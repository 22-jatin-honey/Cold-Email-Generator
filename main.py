'''import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            requests_kwargs = {"timeout": 15}
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)'''

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # Input tabs or layout for URL vs Raw Text fallback
    url_input = st.text_input("Enter a Job Posting URL:", value="https://jobs.nike.com/job/R-33460")

    # Optional text area fallback for sites that completely block web scraping
    manual_jd = st.text_area("Or paste the Job Description text directly (if the URL gets blocked):", height=150)

    submit_button = st.button("Submit")

    if submit_button:
        try:
            data = ""

            # 1. Use manual text input if provided
            if manual_jd.strip():
                data = clean_text(manual_jd)

            # 2. Otherwise, scrape using WebBaseLoader with custom User-Agent headers
            elif url_input.strip():
                # Define a standard browser User-Agent header to bypass basic anti-bot blocks
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/122.0.0.0 Safari/537.36"
                    ),
                    "Accept-Language": "en-US,en;q=0.9",
                }

                loader = WebBaseLoader(
                    web_paths=[url_input],
                    header_template=headers
                )
                loader.requests_kwargs = {"timeout": 15}

                scraped_docs = loader.load()
                if not scraped_docs:
                    st.error("Could not fetch content from the URL. Please paste the job description manually.")
                    return

                data = clean_text(scraped_docs.pop().page_content)

            else:
                st.warning("Please provide either a URL or paste a job description.")
                return

            # Check if extracted text is empty or minimal
            if len(data.strip()) < 50:
                st.warning(
                    "The extracted text is too short or empty. The website might be blocking scrapers or using JavaScript rendering. Try pasting the text manually above.")
                return

            # Process with LLM & Portfolio
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.error("No job details could be parsed from the provided text.")
                return

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)