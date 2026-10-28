import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("GROQ_API_KEY loaded successfully")
else:
    print("GROQ_API_KEY not found")
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException



class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            You are a data extraction assistant. I will provide you with raw scraped text from a careers web page.

Your task is to extract all job postings from the text and return them strictly as a valid JSON array of objects.

Each JSON object in the array must contain the following keys:
- "role": The title/name of the job position.
- "experience": The required experience level or type (e.g., Internship, Entry Level, Senior, etc.).
- "skills": An array of required/relevant skills, tech stack, or job categories mentioned.
- "description": A concise summary or details provided (e.g., location, job program name, or short summary).

### Output Constraints:
1. Output ONLY valid JSON (no markdown explanation outside the JSON code block, no conversational text).
2. Ensure all strings and special characters are properly escaped for valid JSON syntax.

Here is the scraped text:
[INSERT YOUR SCRAPED TEXT HERE]
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are a Master's student pursuing an MSc in Data Science and Artificial Intelligence at Himachal Pradesh University (HPU). You are looking for opportunities to apply your academic knowledge and practical skills in Data Science, Artificial Intelligence, Machine Learning, and related technologies.

Your job is to write a professional and personalized cold email to the company regarding the job or internship opportunity mentioned above. Express your interest in applying for the position and explain how your academic background, technical skills, projects, and willingness to learn can contribute to the organization.

If the posting is for a full-time/part-time job, write the email as a job application. If it is an internship opportunity, write the email specifically expressing interest in an internship.

Use the job description to identify the most relevant skills and requirements, and connect them naturally with the candidate's background. Keep the email concise, professional, confident, and personalized.

Remember that you are an MSc Data Science and AI student at Himachal Pradesh University (HPU) seeking a job or internship opportunity.

Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content



