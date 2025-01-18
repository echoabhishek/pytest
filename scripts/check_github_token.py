
import os

def check_github_token():
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        print(f"GITHUB_TOKEN is set: {github_token[:4]}...{github_token[-4:]}")
        return True
    else:
        print("GITHUB_TOKEN is not set")
        return False

if __name__ == "__main__":
    check_github_token()
