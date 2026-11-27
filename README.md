# GDPR & AI Governance

Personal study for Dutch and EU higher education. Version 1.0: 17 lessons, 51 curated True/False questions. No AI API or university case data. English with Dutch terminology. Content is separate in curriculum.json. Primary legal sources are linked by article/recital; the first-release notes are educational summaries, not a fully reviewed legal textbook.

## Deploy separately from Napraten

1. Create a new GitHub repository named `gdpr-learning`. Upload the contents of this folder (including `.streamlit/config.toml` and `.gitignore` if possible). Do not upload secrets or progress backups.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create a new app from that repository, branch `main`, entrypoint `app.py`. Use a public app if the workspace's private-app allowance is used. A public app with a password gate is not equivalent to a private hosting environment.
3. Set the following in Advanced settings / Secrets (choose a long unique password, do not use the example literally):

```toml
app_password = "YOUR-UNIQUE-PASSWORD"
```

The app fails closed if no password is configured. Sign-in is session-based, so reconnecting may require a password again. Do not store confidential documents in this app.

## Durable learning history (optional but recommended)

Community Cloud local files can disappear on restart/redeployment. Without a database the app saves locally on a best-effort basis, warns you, and provides JSON export/restore under Progress. For automatic durable storage, use a dedicated PostgreSQL database (e.g. a managed EU-region instance if desired) and add a TLS-enabled connection URI to Secrets:

```toml
progress_dsn = "postgresql://USER:PASSWORD@HOST:5432/DB?sslmode=require"
```

Use a database/role dedicated to this app, with table creation, read and write permissions. The app creates `gdpr_learning_progress` on first use. This is a single-user design; don't share the password or study concurrently from multiple tabs because last save wins. If migrating from temporary storage, export first and restore after setting the DSN. No database or paid service is provisioned automatically. Back up periodically regardless.

## Local run

Python 3.11+ recommended. `pip install -r requirements.txt` then `streamlit run app.py`. Put the password in `.streamlit/secrets.toml` (ignored by Git). Local progress is stored in `.progress.json` (ignored by Git).

## Content maintenance

Edit `curriculum.json` directly (stable lesson/question IDs preserve progress), or use `build_content.py` to regenerate the initial content. Do not regenerate over later manual edits without reconciling changes. Update the version/review date when editing. The AI Act includes Regulation (EU) 2026/1744; official legal text takes precedence. The initial question bank repeats existing statements, not automatically generated variants; expand it with alternate scenarios later. All cases are fictional. No university-specific internal rules are asserted. Dutch laws should be checked in their official current versions before practical reliance.
