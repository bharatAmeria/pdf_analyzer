import json
import os
from src.logger import logging
from src.exception import MyException

class PromptLoader:
    """Class to load and format prompts from a JSON file."""
    def __init__(self, prompts_file):
        self.prompts_file = prompts_file
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load prompts from the JSON file."""
        try:
            logging.debug("Loading prompts from %s", self.prompts_file)
            if not os.path.exists(self.prompts_file):
                logging.error("Prompts file not found: %s", self.prompts_file)
                raise FileNotFoundError(f"Prompts file not found: {self.prompts_file}")
            with open(self.prompts_file, "r", encoding="utf-8") as f:
                prompts = json.load(f)
            logging.debug("Prompts loaded successfully")
            return prompts
        except MyException as e:
            logging.error("Error loading prompts: %s", str(e))
            raise MyException(f"Error loading prompts: {str(e)}")

    def get_prompt(self, prompt_key, **kwargs):
        """Fetch and format a prompt by key with provided variables."""
        try:
            if prompt_key not in self.prompts:
                logging.error("Prompt key not found: %s", prompt_key)
                raise KeyError(f"Prompt key not found: {prompt_key}")
            template = self.prompts[prompt_key]["template"]
            formatted_prompt = template.format(**kwargs)
            logging.debug("Prompt fetched and formatted for key: %s", prompt_key)
            return formatted_prompt
        except MyException as e:
            self.logger.error("Error formatting prompt %s: %s", prompt_key, str(e))
            raise MyException(f"Error formatting prompt {prompt_key}: {str(e)}")