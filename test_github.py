from github import Github, Auth
import os
from dotenv import load_dotenv
import requests

# Load .env
load_dotenv()

# -------------------------
# Test GitHub
# -------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

# Get authenticated user
user = g.get_user()
print(f"👤 GitHub Authenticated as: {user.login}")

if user.login != USERNAME:
    print(f"⚠️ Warning: .env username ({USERNAME}) doesn't match actual login ({user.login})")

print("\n📂 Your first 5 GitHub repos:")
for repo in user.get_repos()[:5]:
    print("-", repo.name)

# -------------------------
# Test AIPipe (replaces OpenAI)
# -------------------------
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")

try:
    response = requests.post(
        "https://aipipe.org/openrouter/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPIPE_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4.1-nano",
            "messages": [
                {"role": "user", "content": "Say hello! This is an AIPipe test."}
            ],
        },
    )

    if response.status_code == 200:
        data = response.json()
        print("\n✅ AIPipe Authenticated. Model response:")
        print("-", data["choices"][0]["message"]["content"])
    else:
        print("\n❌ AIPipe API call failed:", response.text)

except Exception as e:
    print("\n❌ Error calling AIPipe API:", e)
