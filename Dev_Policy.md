# Deployment & Git Policy

> [!CRITICAL]
> **DEPLOYMENT FORBIDDEN**
> The Coding Agent (Anti-Gravity) is **FORBIDDEN** from performing deployments.
> All deployments are handled by a separate **Deployment Agent**.

1.  **NO PUSHES**: Do not run `git push`.
2.  **PREPARATION ONLY**: This agent's responsibility is to:
    - Write code.
    - Run tests.
    - Build the installer (`dist` folder).
    - Update documentation (`WALKTHROUGH.md`, `DEPLOYMENT_INSTRUCTIONS`).
3.  **HANDOFF**: Once the build is verified, notify the user that the "Deployment Agent" can take over.
