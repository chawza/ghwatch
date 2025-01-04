import os
from github import Github, Auth

def get_github_client(token: str | None= None):
    token = token or os.getenv('GITHUB_TOKEN')

    if not token:
        raise ValueError("GitHub token is required")

    auth = Auth.Token(token) 

    return Github(auth=auth)
