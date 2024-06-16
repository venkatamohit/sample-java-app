import requests

def post_review_comment(repo, pull_number, review_body):
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/reviews"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": review_body,
        "event": "COMMENT"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
repo = "username/repo"
pull_number = 1
review_body = "This is an automated review comment."
post_review_comment(repo, pull_number, review_body)
