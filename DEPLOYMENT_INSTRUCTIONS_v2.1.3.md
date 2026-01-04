# Deployment Instructions v2.1.3 (Backend Bundled)

> [!IMPORTANT]
> **MAJOR FIX: Backend Bundling**
> This version bundles `python_embedded` and `backend` directly into the app resource folder to ensure they are found regardless of installation path.
> `asar` archiving is disabled to ensure executables can run.

## 1. Prepare & Push Code
1.  **Update Version**: Edit `version.json` to `"version": "v2.1.3"`.
2.  **Initialize Git**: `git init`
3.  **Add Remote**: `git remote add origin https://github.com/hakimluxeco-dev/cold-email-repo.git`
4.  **Commit**: "Release v2.1.3: Bundled Backend Fix"
5.  **Push**: `git push -u origin master --force`

## 2. GitHub Release
> [!CRITICAL]
> **MANDATORY RELEASE DETAILS**
> You **MUST** fill in the following details correctly. Failure to do so will confuse users or break the update path.

1.  **Tag**: `v2.1.3`
2.  **Title**: `v2.1.3 - Bundled Backend & Fixed Import`
3.  **Description**:
    ```markdown
    **CRITICAL FIXES**
    - **Backend Bundled**: Fixed "Python executable not found" by bundling backend files directly into the app.
    - **ASAR Disabled**: Ensures reliable path resolution for embedded Python.
    - **Features**: Includes all v2.1.2 features (Bulk Delete, Standalone).
    ```
4.  **Upload**: `dist/ColdEmailReachSetup.exe`
5.  **Publish**.

## 3. Verify
- Download the executable from GitHub on a clean machine to verify standalone capability.
