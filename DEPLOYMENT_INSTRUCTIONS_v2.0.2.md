# Deployment Instructions v2.0.2 (HOTFIX)

> [!WARNING]
> **CRITICAL INFO FOR v2.0.1 USERS**
> Users on v2.0.1 **CANNOT** auto-update to v2.0.2 because the "Download" feature is broken in v2.0.1.
> They will see the update banner, but clicking "Update Now" will fail.
> **You must tell these users to download the installer manually.**
> Future updates (v2.0.2 -> v2.1.0) will work correctly.

## 1. Push Version Config
I need to push `version.json` (pointing to v2.0.2) to GitHub.
**Action Required**: Approve the push in the chat.

## 2. Release on GitHub
1.  **Tag**: `v2.0.2`
2.  **Title**: `v2.0.2 - Hotfix`
3.  **Description**:
    ```markdown
    **HOTFIX**: Fixed critical bug where auto-update downloads would fail.
    NOTE: If you are on v2.0.1, you MUST download and run this installer manually.
    ```
4.  **Upload**: `dist/ColdEmailReachSetup.exe`
5.  **Publish**.

## 3. Verify
Install v2.0.2 manually. Future updates will be smooth.
