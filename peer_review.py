import openai
import os
import requests
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_pr_code(repo, pull_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/files"
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR files: {response.text}")
    files = response.json()
    
    code_changes = []
    for file in files:
       if file.get('filename', '').endswith('.java'):  # Adjust file extension as needed
            file_url = file['raw_url']
            file_content = requests.get(file_url, headers=headers).text
            code_changes.append(file_content)
    
    return '\n\n'.join(code_changes)

def review_code(code, repo, pull_number):
    openai.api_key = os.getenv('OPENAI_API_KEY')  # Set your OpenAI API key

    # Request code review using ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": f"Review the following code for any issues or improvements:\n\n{code}"}
        ]
    )

    # Extract content from the response
    review_result = response['choices'][0]['message']['content'].strip()

    # Post the review result as a comment on the pull request
    post_issue_comment(repo, pull_number, "Automated Code Review", review_result)

    # Check if issues were found and return the review result
    if "no issues found" in review_result.lower():
        return True  # No issues found
    else:
        return False  # Issues found


def post_issue_comment(repo, pull_number, comment_title, comment_body):
    url = f"https://api.github.com/repos/{repo}/issues/{pull_number}/comments"
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": f"### {comment_title}\n\n{comment_body}"  # Customize comment title format here
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Successfully posted comment to PR #{pull_number}")
    else:
        print(f"Failed to post comment to PR #{pull_number}. Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        
def check_code_quality(code_to_review):
    # Simplified example: Check if code_to_review meets quality standards
    if "bad_code_pattern" in code_to_review:
        raise Exception("Code review failed due to bad code pattern.")

# Example usage
def main():
    repo = "venkatamohit/sample-java-app"
    pull_number = os.getenv('GITHUB_PULL_NUMBER')  # Assumes this environment variable is set by GitHub Actions
    
    comment_title = "Automated Peer Review"
    code_to_review = fetch_pr_code(repo, pull_number)
    try:
        review_result = review_code(code_to_review, repo, pull_number)
        if not review_result:
            print("Code review found issues. Failing PR check.")
            exit(1)  # Exit with non-zero status to fail the PR check
        else:
            print("Code review passed. No issues found.")
    except Exception as e:
        print(f"Error in code review: {str(e)}")
        exit(1)  # Exit with non-zero status in case of error


if __name__ == "__main__":
    main()
