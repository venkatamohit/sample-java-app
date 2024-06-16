import openai
import os
import requests
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_pr_code(repo, pull_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/files"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    files = response.json()
    
    code_changes = []
    for file in files:
        if file['filename'].endswith('.java'):  # Adjust file extension as needed
            file_url = file['raw_url']
            file_content = requests.get(file_url, headers=headers).text
            code_changes.append(file_content)
    
    return '\n\n'.join(code_changes)

def review_code(code):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": f"Review the following code for any issues or improvements:\n\n{code}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

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
def main():
    repo = "venkatamohit/sample-java-app"
    pull_number = os.getenv('GITHUB_PULL_NUMBER')  # Assumes this environment variable is set by GitHub Actions
    
    code_to_review = fetch_pr_code(repo, pull_number)
    review = review_code(code_to_review)
    print("Review:", review)
    
    post_review_comment(repo, pull_number, review)

if __name__ == "__main__":
    main()
