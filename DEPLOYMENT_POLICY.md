# Deployment & Git Policy

> [!CRITICAL]
> **STRICT APPROVAL REQUIRED**

1.  **NO AUTOMATIC PUSHES**: The AI Agent is **FORBIDDEN** from pushing code, configuration variables, or releases to GitHub automatically.
2.  **EXPLICIT APPROVAL**: Every `git push` command must be explicitly approved by the user in the chat before execution.
3.  **VERSION CONTROL**: The `version.json` file controls the live update path. Changes to this file effectively deploy code to users. TREAT IT WITH CAUTION.
    > **RATIONALE**: We may need to test the build locally or bundle more features into a version *before* it goes live. Pushing too early breaks this workflow.
4.  **POST-DEPLOYMENT ACTION**: After every granted deployment (push), the AI Agent **MUST** automatically:
    - Open the `dist` folder (`explorer dist`).
    - Open the GitHub Release page (`start https://...`) with **Tag, Title, and Description PRE-FILLED**.
    - Guide the user to perform the manual upload.
