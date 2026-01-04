# Your Launch Checklist

Follow these steps exactly to enable the Auto-Update feature.

## Phase 1: GitHub Setup (Do this NOW)
1.  **Create a Folder**: Create a new folder on your Desktop called `cold-email-repo`.
2.  **Create Version File**: Inside that folder, create a file named `version.json` with this content:
    ```json
    {
      "version": "2.0.0",
      "downloadUrl": "",
      "releaseNotes": "Initial V2 Release"
    }
    ```
    *(We leave downloadUrl empty for now because V2 is the one checking, it doesn't need to download itself).*
3.  **Upload to GitHub**:
    *   Go to [GitHub.com](https://github.com) and sign in.
    *   Create a **New Repository** (Public). Name it `cold-email-system`.
    *   Upload your `version.json` file to this repository.
4.  **Enable GitHub Pages**:
    *   In your repo, go to **Settings** > **Pages**.
    *   Under "Build and deployment", select **Source** as `Deploy from a branch`.
    *   Select `main` branch and `/ (root)` folder. Click **Save**.
5.  **Get the URL**:
    *   After a minute, GitHub will show you a link like `https://<username>.github.io/cold-email-system/`.
    *   Add `version.json` to the end: `https://<username>.github.io/cold-email-system/version.json`
    *   **Test it**: Paste that link in your browser. You should see your JSON text.

## Phase 2: Final Build (Tell Me)
6.  **PASTE THE URL HERE**: Come back to this chat and paste that `version.json` URL.
    *   *Why?* I need to bake this URL into the application code so it knows where to look for updates in the future.

## Phase 3: Distribution (After I Build)
7.  **Distribute V2**: I will run the build one last time. You will then send `ColdEmailReachSetup.exe` to your users. This is **V2**.

## Phase 4: Releasing Updates (Future V3, V4...)
When you want to release an update later:
1.  I will give you a new installer (e.g., V3).
2.  You upload that `.exe` to **GitHub Releases**.
3.  You Edit `version.json` on GitHub to:
    *   Update `"version": "3.0.0"`
    *   Update `"downloadUrl": "link-to-v3-exe"`
4.  V2 users will automatically see the update banner!
