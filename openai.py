import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def review_code(code):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Review the following code for any issues or improvements:\n\n{code}",
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Example usage
code_to_review = """
def add(a, b):
    return a + b
"""

review = review_code(code_to_review)
print("Review:", review)
