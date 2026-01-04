# Deployment Instructions v2.0.1

> [!IMPORTANT]
> Follow these steps exactly to release the new version to your users.

## 1. Push Version Config (AI Assisted)
The AI is ready to push the updated `version.json` to your GitHub repository.
**Action Required**: Approve the AI's request in the chat.

## 2. Create GitHub Release
1.  Go to: [https://github.com/hakimluxeco-dev/cold-email-repo/releases/new](https://github.com/hakimluxeco-dev/cold-email-repo/releases/new)
2.  **Tag version**: `v2.0.1` (Must match exactly).
3.  **Release title**: `v2.0.1`
4.  **Description**:
    ```markdown
    ## What's New
    - Premium Splash Screen
    - Fixed Lead Import (CSV/TXT/MD)
    - Real-time Dashboard Stats
    - Installing to Program Files (Admin)
    ```
5.  **Attach binaries**: Drag and drop the file `dist/ColdEmailReachSetup.exe` into the upload box.
6.  Click **Publish release**.

## 3. Verify Update
1.  Wait about 1-2 minutes for GitHub Pages to update.
2.  Open your existing installed app (v2.0.0).
3.  It should detect the update and show the banner.
4.  Click "Update Now".
