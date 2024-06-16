import os
import requests
import openai
import base64
from dotenv import load_dotenv
from github import Github, GithubIntegration

def get_github_api_client():
    github_app_id = os.getenv('GITHUB_APP_ID')
    github_installation_id = os.getenv('GITHUB_INSTALLATION_ID')
    github_private_key_path = os.getenv('GITHUB_PRIVATE_KEY_PATH')

    # Read private key file contents
    with open(github_private_key_path, 'r') as key_file:
        private_key = key_file.read()

    # Create GitHub Integration
    integration = GithubIntegration(github_app_id, private_key)

    # Get installation access token
    installation_id = int(github_installation_id)
    installation = integration.get_repo_installation(repo_id=installation_id)

    # Create installation access token
    access_token = installation.create_access_token()

    # Create GitHub client with access token
    github_client = Github(access_token)

    return github_client

def review_code(code, repo, pull_number, file_path):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Split the code into lines
    lines = code.splitlines()
    non_commented_lines = []

    # Filter out commented lines
    for line_number, line in enumerate(lines, start=1):
        if not line.strip().startswith('//') and not line.strip().startswith('/*'):
            non_commented_lines.append(line)

    # Join non-commented lines back into code
    code_to_review = '\n'.join(non_commented_lines)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": f"Review the following code only for any issues:\n\n{code_to_review}"}
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
    github_client = get_github_api_client()

    # Fetch the latest commit ID associated with the file
    commit_id = fetch_latest_commit_id(repo, pull_number, file_path)

    # Parse the review result and extract issues
    issues = parse_review_result(review_result, file_path)

    for issue in issues:
        line_number = issue['line_number']
        comment = issue['comment']

        # Construct the comment data
        data = {
            "body": comment,
            "path": file_path,
            "commit_id": commit_id
        }
        if line_number:
            data["position"] = line_number

        # Post comment using PyGithub
        try:
            repo_obj = github_client.get_repo(repo)
            pull_request = repo_obj.get_pull(int(pull_number))
            pull_request.create_review_comment(body=data['body'], commit_id=data['commit_id'],
                                               path=data['path'], position=data.get('position', None))
            print(f"Successfully posted comment on Line {line_number} of PR #{pull_number}")
        except Exception as e:
            print(f"Failed to post comment on Line {line_number} of PR #{pull_number}: {str(e)}")

def parse_review_result(review_result, file_path):
    issues = []

    # Split the review_result into individual reviews
    review_sections = review_result.split('\n\n')

    for section in review_sections:
        if not section.strip():  # Skip empty sections
            continue

        # Extract line number if available
        line_number = None
        issue_content = section.strip()

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
    github_client = get_github_api_client()

    try:
        repo_obj = github_client.get_repo(repo)
        pull_request = repo_obj.get_pull(int(pull_number))
        commits = pull_request.get_commits()
        if commits:
            return commits[-1].sha  # Use the latest commit's SHA
        else:
            raise Exception("No commits found in the pull request.")
    except Exception as e:
        raise Exception(f"Failed to fetch commit details for PR #{pull_number}: {str(e)}")

def fetch_files_in_pull_request(repo, pull_number):
    github_client = get_github_api_client()

    try:
        repo_obj = github_client.get_repo(repo)
        pull_request = repo_obj.get_pull(int(pull_number))
        files = pull_request.get_files()
        file_paths = [file.filename for file in files]
        return file_paths
    except Exception as e:
        raise Exception(f"Failed to fetch files in pull request #{pull_number}: {str(e)}")

def fetch_file_content(repo, commit_id, file_path):
    github_client = get_github_api_client()

    try:
        repo_obj = github_client.get_repo(repo)
        file_content = repo_obj.get_contents(file_path, ref=commit_id)
        content = base64.b64decode(file_content.content).decode('utf-8')
        return content
    except Exception as e:
        raise Exception(f"Failed to fetch content for file {file_path}: {str(e)}")

def main():
    repo = "venkatamohit/sample-java-app"
    pull_number = os.getenv('GITHUB_PULL_NUMBER')

    # File extensions to skip during review
    skip_extensions = ['.md', '.txt', '.json', '.py', '.yml']

    # Fetch all files in the pull request
    file_paths = fetch_files_in_pull_request(repo, pull_number)

    all_reviews_passed = True
    reviewed_files = set()

    for file_path in file_paths:
        # Skip files with certain extensions
        if any(file_path.endswith(ext) for ext in skip_extensions):
            continue

        # Ensure each file is reviewed only once
        if file_path in reviewed_files:
            continue
        reviewed_files.add(file_path)

        try:
            # Fetch the latest file content
            file_content = fetch_file_content(repo, 'HEAD', file_path)

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
