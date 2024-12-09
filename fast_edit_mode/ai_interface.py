# ai_interface.py

from openai import OpenAI, APIError
import logging

logger = logging.getLogger(__name__)

class AIModelInterface:
    def __init__(self, config):
        self.api_key = config['api_keys']['openai']
        self.model_name = config['model']['name']
        self.temperature = config['model']['temperature']
        self.client = OpenAI(api_key=self.api_key)

    def edit_code(self, code, instruction):
        if not code or not code.strip():
            logger.error("Empty code received")
            return code
            
        # Use AI model to perform specific code editing based on the instruction
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a code improvement assistant. You will receive Python code and instructions for improving it. Return ONLY the improved code without any explanation, conversation, or markdown formatting."},
                    {"role": "user", "content": f"Instructions: {instruction}\n\nCode:\n{code}"}
                ],
                temperature=self.temperature,
                max_tokens=2048
            )
            improved_code = response.choices[0].message.content.strip()
            
            # Validate the response
            if not improved_code or "I'd be happy to help" in improved_code or "Here's" in improved_code:
                logger.warning("Invalid AI response received. Keeping original code.")
                return code
                
            # Basic validation that we got Python code back
            if not any(keyword in improved_code for keyword in ['def ', 'class ', '=', 'return']):
                logger.warning("Response may not be valid Python code. Keeping original.")
                return code
                
            return improved_code
        except APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            # Log additional details about the error
            logger.error(f"Model used: {self.model_name}")
            logger.error(f"Error details: {str(e)}")
            return code  # Return original code instead of raising exception
        except Exception as e:
            logger.error(f"Unexpected AI processing error: {e}")
            return code  # Return original code instead of raising exception

    def correct_syntax(self, code):
        return self.edit_code(code, instruction="Fix these syntax and style issues in the code:\n1. Add proper spacing around operators and after commas\n2. Fix indentation\n3. Add blank lines between functions and classes\n4. Fix any PEP 8 style issues")

    def optimize_code(self, code):
        return self.edit_code(code, instruction="Optimize this code while maintaining its functionality:\n1. Improve variable names\n2. Fix operator spacing\n3. Use more efficient operations where possible")

    def refactor_code(self, code):
        return self.edit_code(code, instruction="Refactor this code to improve readability:\n1. Use better variable names\n2. Add proper spacing\n3. Follow Python best practices\n4. Maintain the same functionality")

    def add_documentation(self, code):
        return self.edit_code(code, instruction="Add documentation to this code:\n1. Add docstrings to functions and classes\n2. Add inline comments for complex logic\n3. Follow PEP 257 for docstrings\n4. Keep the code functionality unchanged")
