from src.logger import logging
from src.exception import MyException

class ResumeAnalyzer:
    """Class to analyze resumes using GroqHandler."""
    def __init__(self, groq_handler, prompt_loader):
        self.grok = groq_handler
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        """Analyze resume text."""
        logging.debug("Starting resume analysis for designation: %s, experience: %s, domain: %s",
                         designation, experience, domain)
        try:
            prompt = self.prompt_loader.get_prompt(
                "resume_analysis",
                designation=designation,
                experience=experience,
                domain=domain
            )
            result = self.grok.analyze_text(prompt, text, max_tokens=1500)
            logging.debug("Resume analysis completed")
            return result
        except MyException as e:
            logging.error("Error analyzing resume: %s", str(e))
            raise MyException(f"Error analyzing resume: {str(e)}")