# Deployment Instructions v2.1.2 (Standalone Release)

> [!IMPORTANT]
> **MAJOR UPDATE: Standalone Architecture**
> This version bundles Python and changes the database path.

## 1. Initialize & Push Code
Since the previous git history seems lost/disconnected, we will initialize a new repo state.
1.  **Initialize Git**: `git init`
2.  **Add Remote**: `git remote add origin https://github.com/marcio1002/cold-email-repo.git` (Assuming this is the repo, verifiable via previous context or user input).
3.  **Commit**: "Release v2.1.2: Embedded Python & Bulk Delete"
4.  **Push**: `git push -u origin master --force` (Force might be needed if overwriting old history, or we just push to a new branch).

## 2. GitHub Release
> [!CRITICAL]
> **MANDATORY RELEASE DETAILS**
> You **MUST** fill in the following details correctly. Failure to do so will confuse users or break the update path.
> An auto-generated link may be provided by the system, or fill them manually:

1.  **Tag**: `v2.1.2`
2.  **Title**: `v2.1.2 - Standalone & Bulk Delete`
3.  **Description**:
    ```markdown
    **MAJOR UPDATE**
    - **Standalone**: No Python installation required!
    - **Bulk Delete**: Select and delete multiple leads.
    - **Fixes**: Import duplicate prevention and network error fixes.
    - **Database**: Now stored in installation folder.
    ```
4.  **Upload**: `dist/ColdEmailReachSetup.exe`
5.  **Publish**.

## 3. Verify
- Download the executable from GitHub on a clean machine to verify standalone capability.
