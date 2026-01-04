import urllib.parse
import os

base = 'https://github.com/hakimluxeco-dev/cold-email-repo/releases/new'
params = {
    'tag': 'v2.1.2',
    'title': 'v2.1.2 - Import Fix',
    'body': '## What\'s New\n* **Fixed Lead Import:** Resolved an issue where leads were not imported if the Email column was the first column in the file.\n* **Settings Persistence:** User settings are now preserved during updates.'
}
url = base + '?' + urllib.parse.urlencode(params)
os.system(f'start "" "{url}"')
