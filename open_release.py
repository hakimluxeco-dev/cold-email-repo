import urllib.parse
import os

base = 'https://github.com/hakimluxeco-dev/cold-email-repo/releases/new'
params = {
    'tag': 'v2.1.1',
    'title': 'v2.1.1 - Stability & Persistence',
    'body': '## What\'s New\n* **Settings Persistence:** Your credentials and leads are now preserved across updates.\n* **Stability:** Fixed the "error saving settings" issue.\n* **Diagnostics:** Added detailed error reporting.'
}
url = base + '?' + urllib.parse.urlencode(params)
os.system(f'start "" "{url}"')
