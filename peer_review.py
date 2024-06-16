import os
import requests
import openai
import base64

def review_code(code, repo, pull_number, file_path):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": f"Review the following code for any issues:\n\n{code}"}
        ]
    )

    review_result = response['choices'][0]['message']['content'].strip()
    print(f"Review result for {file_path}:\n{review_result}")

    # Post the review result as comments on the pull request
    post_issue_comments(repo, pull_number, file_path, review_result)

    # Check if issues were found and return the review result
    if "no issues found" in review_result.lower():
        return True  # No issues found
    else:
        return False  # Issues found

def post_issue_comments(repo, pull_number, file_path, review_result):
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the latest commit ID associated with the file
    commit_id = fetch_latest_commit_id(repo, pull_number, file_path)

    # Parse the review result and extract issues
    issues = parse_review_result(review_result)

    for issue in issues:
        line_number = issue['line_number']
        comment = issue['comment']

        # Construct the comment data
        data = {
            "body": comment,
            "path": file_path,
            "position": line_number,
            "commit_id": commit_id
        }
        url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/comments"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print(f"Successfully posted comment on Line {line_number} of PR #{pull_number}")
        else:
            print(f"Failed to post comment on Line {line_number} of PR #{pull_number}. Status code: {response.status_code}")
            print(f"Response body: {response.text}")

def parse_review_result(review_result):
    # Example parser for the review result
    issues = []

    # Split the review_result into individual reviews
    review_sections = review_result.split('\n\nReview result for ')

    for section in review_sections:
        if not section.strip():  # Skip empty sections
            continue

        # Extract the file path from the section header
        header_end_idx = section.find(':')
        if header_end_idx == -1:
            continue
        
        file_path = section[:header_end_idx].strip()
        issues_content = section[header_end_idx + 1:].strip()

        if issues_content.startswith('Overall'):
            continue

        # Extract individual issues and suggestions using "-" or ":"
        issues_list = []
        current_issue = ""
        for char in issues_content:
            if char == '-' or char == ':':
                issues_list.append(current_issue.strip())
                current_issue = ""
            else:
                current_issue += char
        issues_list.append(current_issue.strip())  # Append the last issue

        # Skip the first element as it contains the file path
        for issue in issues_list[1:]:
            if issue.strip():  # Check if the issue is not empty
                # Split the issue to get start line number and comment
                line_number = None
                issue_content = issue.strip()

                # Extract line number if available
                line_number_idx = issue_content.find('. ')
                if line_number_idx != -1:
                    line_number_str = issue_content[:line_number_idx].strip()
                    if line_number_str.isdigit():
                        line_number = int(line_number_str)

                issues.append({
                    "file_path": file_path,
                    "line_number": line_number,
                    "comment": issue_content
                })

    return issues

def fetch_latest_commit_id(repo, pull_number, file_path):
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/files"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file['filename'] == file_path:
                return file['sha']
        raise Exception(f"File {file_path} not found in the pull request.")
    else:
        raise Exception(f"Failed to fetch files for PR #{pull_number}. Status code: {response.status_code}")

def fetch_commit_ids(repo, pull_number):
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/commits"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        commit_ids = [commit['sha'] for commit in commits]
        if not commit_ids:
            raise Exception("No commits found in the pull request.")
        return commit_ids
    else:
        raise Exception(f"Failed to fetch commit details for PR #{pull_number}. Status code: {response.status_code}")

def fetch_files_in_commit(repo, commit_id):
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/commits/{commit_id}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json().get('files', [])
        file_paths = [file['filename'] for file in files]
        return file_paths
    else:
        raise Exception(f"Failed to fetch files in commit {commit_id}. Status code: {response.status_code}")

def fetch_file_content(repo, commit_id, file_path):
    headers = {
        "Authorization": f"token {os.getenv('MY_GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={commit_id}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json().get('content', '')
        content_bytes = base64.b64decode(content)
        return content_bytes.decode('utf-8')
    else:
        raise Exception(f"Failed to fetch content for file {file_path}. Status code: {response.status_code}")

def main():
    repo = "venkatamohit/sample-java-app"
    pull_number = os.getenv('GITHUB_PULL_NUMBER')

    # File extensions to skip during review
    skip_extensions = ['.md', '.txt', '.json', '.py', '.yml']

    # Fetch all commit IDs in the pull request
    commit_ids = fetch_commit_ids(repo, pull_number)

    all_reviews_passed = True
    reviewed_files = set()

    for commit_id in commit_ids:
        # Fetch all files in the commit
        file_paths = fetch_files_in_commit(repo, commit_id)

        for file_path in file_paths:
            # Skip files with certain extensions
            if any(file_path.endswith(ext) for ext in skip_extensions):
                continue

            # Ensure each file is reviewed only once
            if file_path in reviewed_files:
                continue
            reviewed_files.add(file_path)

            # Fetch the file content
            file_content = fetch_file_content(repo, commit_id, file_path)

            try:
                review_result = review_code(file_content, repo, pull_number, file_path)
                if not review_result:
                    print(f"Code review found issues in {file_path}.")
                    all_reviews_passed = False  # Mark that there were issues found
            except Exception as e:
                print(f"Error in code review for {file_path}: {str(e)}")
                all_reviews_passed = False  # Mark that there were issues found

    if not all_reviews_passed:
        print("Code review found issues. Failing PR check.")
        exit(1)  # Exit with non-zero status to fail the PR check
    else:
        print("Code review passed. No issues found.")

if __name__ == "__main__":
    main()
