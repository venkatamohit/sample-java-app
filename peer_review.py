import os
import requests
import openai
import base64
from github import Github, GithubIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_github_api_client():
    github_app_id = os.getenv('GITHUB_APP_ID')
    github_private_key_path = os.getenv('GITHUB_PRIVATE_KEY')
    repo_name = os.getenv('GITHUB_REPOSITORY')

    # Extract the owner and repository name
    owner, repo = repo_name.split('/')

    with open(github_private_key_path, 'r') as key_file:
        private_key = key_file.read()

    integration = GithubIntegration(github_app_id, private_key)

    # Get the installation ID for the repository
    installation = integration.get_repo_installation(owner, repo)
    access_token = integration.get_access_token(installation.id).token
    return Github(login_or_token=access_token)

def review_code(code, repo, pull_number, file_path):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Split the code into lines
    code_to_review = code.strip()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code review assistant. Only highlight issues in the code."},
            {"role": "user", "content": f"Review the following code for any issues:\n\n{code_to_review}"}
        ]
    )

    review_result = response['choices'][0]['message']['content'].strip()
    print(f"Review result for {file_path}:\n{review_result}")

    # Filter out non-issue lines
    issue_keywords = ["issue", "error", "bug", "problem", "fix", "improve", "incorrect", "mistake"]
    issue_lines = [line for line in review_result.split('\n') if any(keyword in line.lower() for keyword in issue_keywords)]

    filtered_review_result = '\n'.join(issue_lines)
    print(f"Filtered Result: {filtered_review_result}")

    # Check if issues were found and return the review result
    if "no issues found" in filtered_review_result.lower() or "code looks good" in filtered_review_result.lower() or "code looks well-written" in filtered_review_result.lower() or not issue_lines:
        return True  # No issues found
    else:
        # Post the review result as comments on the pull request
        post_issue_comments(repo, pull_number, file_path, review_result)
        post_issue_comments(repo, pull_number, file_path, filtered_review_result)
        return False  # Issues found

def post_issue_comments(repo_name, pull_number, file_path, review_result):
    github_client = get_github_api_client()
    repo_name = os.getenv('GITHUB_REPOSITORY')
    # Extract the owner and repository name from the repo_name string
    owner, repo = repo_name.split('/')
    # Get the repository object
    repo_obj = github_client.get_repo(repo_name)
    # Fetch the latest commit ID associated with the file
    commit_id = fetch_latest_commit_id(repo, pull_number, file_path)
    print(commit_id)
    # Parse the review result and extract issues
    issues = parse_review_result(review_result, file_path)

    for issue in issues:
        line_number = issue['line_number']
        comment = issue['comment']

        # If line_number is None, post a regular PR comment
        if line_number is None:
            try:
                pull_request = repo_obj.get_pull(pull_number)
                pull_request.create_issue_comment(comment)
                print(f"Successfully posted general comment on PR #{pull_number}")
            except Exception as e:
                print(f"Failed to post general comment on PR #{pull_number}: {str(e)}")
        else:
            # Construct the comment data with position if line_number is provided
            data = {
                "body": comment,
                "path": file_path,
                "commit_id": commit_id,
                "position": line_number
            }

            # Post the comment using PyGithub
            try:
                pull_request = repo_obj.get_pull(pull_number)
                pull_request.create_review_comment(data["body"], data["commit_id"], file_path, line_number)
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

def fetch_latest_commit_id(repo_name, pull_number, file_path):
    github_client = get_github_api_client()
    repo_name = os.getenv('GITHUB_REPOSITORY')
    # Extract the owner and repository name from the repo_name string
    owner, repo = repo_name.split('/')
    # Get the repository object
    repo_obj = github_client.get_repo(repo_name)
    # Get the pull request and commits
    pr = repo_obj.get_pull(pull_number)
    commits = pr.get_commits()
    
    if commits.totalCount > 0:
        return commits[commits.totalCount - 1].sha  # Use the latest commit's SHA
    else:
        raise Exception("No commits found in the pull request.")

def fetch_files_in_pull_request(repo_name, pull_number):
    github_client = get_github_api_client()
    repo_name = os.getenv('GITHUB_REPOSITORY')
    # Extract the owner and repository name from the repo_name string
    owner, repo = repo_name.split('/')
    # Get the repository object
    repo_obj = github_client.get_repo(repo_name)
    # Get the pull request and commits
    pr = repo_obj.get_pull(pull_number)
    files = pr.get_files()
    file_paths = [file.filename for file in files]
    return file_paths

def fetch_file_content(repo_name, commit_id, file_path):
    github_client = get_github_api_client()
    repo_name = os.getenv('GITHUB_REPOSITORY')
    owner, repo = repo_name.split('/')
    repo_obj = github_client.get_repo(repo_name)

    try:
        # Print debug info
        print(f"Fetching content of file: {file_path} at commit: {commit_id}")     
        # Fetch contents from GitHub
        contents = repo_obj.get_contents(file_path, ref=commit_id)
        # Print content for debugging
        print(f"Content fetched: {contents.content[:100]}")  # Print part of the content
        # Decode and return content
        return base64.b64decode(contents.content).decode('utf-8')
    except Exception as e:
        print(f"Error fetching file content: {str(e)}")
        raise  # Re-raise the exception for further troubleshooting

def main():
    repo = "venkatamohit/sample-java-app"
    pull_number = int(os.getenv('GITHUB_PULL_NUMBER'))

    # File extensions to skip during review
    skip_extensions = ['.md', '.txt', '.json', '.py', '.yml','.pem']

    # Fetch all files in the pull request
    file_paths = fetch_files_in_pull_request(repo, pull_number)

    all_reviews_passed = True
    reviewed_files = set()

    for file_path in file_paths:
        print(file_path)
        # Skip files with certain extensions
        if any(file_path.endswith(ext) for ext in skip_extensions):
            continue

        # Ensure each file is reviewed only once
        if file_path in reviewed_files:
            continue
        reviewed_files.add(file_path)

        try:
            # Fetch the latest file content
            github_client = get_github_api_client()   
            repo = github_client.get_repo(repo)
            pr = repo.get_pull(pull_number)
            commits = pr.get_commits()
            for commit in commits:
                commit_sha = commit.sha
                commit_id = fetch_latest_commit_id(repo, pull_number, file_path)
                # Fetch the file content using the commit SHA
                file_content = fetch_file_content(repo, commit_id, file_path)
                # Review the file content
                review_result = review_code(file_content, repo, pull_number, file_path)
                if not review_result:
                    print(f"Code review found issues in {file_path} at commit {commit_sha}.")
                    all_reviews_passed = False  # Mark that there were issues found
                    break  # No need to review further commits for this file
                else:
                    print(f"Code review passed for {file_path} at commit {commit_sha}.")

                # Assuming you only want to review the latest version of each file
                break  # Stop processing further commits for this file
        except Exception as e:
            print(f"Error in code review for {file_path}: {str(e)}")
            all_reviews_passed = False  # Mark that there were issues found

    if all_reviews_passed:
        # Post a success comment indicating no issues found
        try:
            github_client = get_github_api_client()
            repo = github_client.get_repo(repo)
            pull_request = repo.get_pull(pull_number)
            pull_request.create_issue_comment("Code review passed. No issues found.")
            print("Successfully posted comment indicating no issues found.")
        except Exception as e:
            print(f"Failed to post comment indicating no issues found: {str(e)}")
    else:
        print("Code review found issues. Failing PR check.")
        exit(1)  # Exit with non-zero status to fail the PR check

if __name__ == "__main__":
    main()
