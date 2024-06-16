import openai
import os
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

def review_code(code):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Review the following code for any issues or improvements:\n\n{code}",
        max_tokens=500
    )
    return response.choices[0].text.strip()

def post_review_comment(repo, pull_number, review_body):
    url = f"https://api.github.com/repos/{repo}/issues/{pull_number}/comments"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": review_body
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
code_to_review = """
def add(a, b):
    return a + b
"""

review = review_code(code_to_review)
print("Review:", review)

repo = "username/repo"
pull_number = 1
post_review_comment(repo, pull_number, review)