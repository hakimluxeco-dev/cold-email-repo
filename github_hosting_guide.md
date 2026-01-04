# How to Host Updates on GitHub

You can easily host your `version.json` and installer files on GitHub for valid auto-updates.

## Step 1: Create a Repository
1.  Create a **Public** repository on GitHub (e.g., `cold-email-app`).
2.  Push your code to it (optional, but good practice).

## Step 2: Enable GitHub Pages (For version.json)
We need a **stable URL** for the app to check. GitHub Pages is perfect for this.

1.  In your local project, create a file named `version.json` in the root (or a `docs` folder).
2.  Commit and push this file to GitHub.
3.  Go to your GitHub Repo -> **Settings** -> **Pages**.
4.  Under **Branch**, select `main` (and `/root` or `/docs` depending on where you put the file).
5.  Click **Save**.
6.  Your file will be available at: `https://<your-username>.github.io/<repo-name>/version.json`

## Step 3: Host the Installer (Releases)
When you have a new version (e.g., installer v2.1):

1.  Go to your GitHub Repo -> **Releases**.
2.  Click **Draft a new release**.
3.  Tag it (e.g., `v2.1.0`).
4.  **Upload** your `ColdEmailReachSetup.exe` file there.
5.  Publish the release.
6.  Copy the link to the uploaded `.exe`.

## Step 4: Update version.json
Edit your local `version.json`, update the version and paste the new download link from Step 3:

```json
{
  "version": "2.1.0",
  "downloadUrl": "https://github.com/<user>/<repo>/releases/download/v2.1.0/ColdEmailReachSetup.exe",
  "releaseNotes": "New features added!"
}
```

Commit and push this change. The app (checking the Pages URL) will now see the new version and link!
