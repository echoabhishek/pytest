
import os

def test_github_token_is_set():
    assert 'GITHUB_TOKEN' in os.environ, "GITHUB_TOKEN is not set in the environment"
    token = os.environ['GITHUB_TOKEN']
    assert token.startswith('ghp_'), "GITHUB_TOKEN does not have the expected format"
    assert len(token) > 10, "GITHUB_TOKEN seems too short"
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_github_token_is_set()
