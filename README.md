** Installation

```
brew install python
brew install pipx

python3 -m venv venv
source venv/bin/activate

pip install requests requests_oauthlib python-dotenv

crontab -e
* * * * * [PATH]/venv/bin/python [PATH]/icloud-sync.py