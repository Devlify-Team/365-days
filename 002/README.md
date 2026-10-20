# 002 — Setup GitHub Pages portfolio

**Topic:** GitHub Setup  
**Challenge month:** Month 1: Foundations & GitHub Basics  
**Source workbook:** `365_Days_GitHub_Challenge_Tracker.xlsx`, All Projects, Day 2  
**Suggested repository name:** `setup-github-pages-portfolio`  
**Primary platform:** GitHub Pages  
**Backups:** Netlify, Vercel

## Goal

Publish a dependency-free static portfolio from `002/site/` with GitHub Actions and GitHub Pages. The workflow at `.github/workflows/002-pages.yml` is scoped to this day's site: it uploads only `002/site` and deploys when relevant paths change on `main` or when manually dispatched.

## Source mapping

- `002/site/index.html` — portfolio structure and content.
- `002/site/styles.css` — presentation and responsive styling.
- `.github/workflows/002-pages.yml` — packages only `002/site` and deploys it to GitHub Pages.
- Official guidance: [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Run locally

From the repository root:

```bash
python3 -m http.server 8000 --directory 002/site
```

Open <http://localhost:8000> in a browser. Stop the server with `Ctrl+C`.

## Enable publishing

1. Push the repository and this workflow to the `main` branch.
2. In the repository, open **Settings > Pages**.
3. Under **Build and deployment**, select **GitHub Actions** as the source.
4. Run the workflow automatically from an eligible `main` change, or use **Actions** to select the workflow and choose **Run workflow**.
5. After a successful run, the expected project URL is <https://devlify-team.github.io/365-days/>.

Publishing depends on the organization's repository and Pages policies, permissions, and Actions settings. The URL above is the expected destination; it has not been verified live yet.

**Current status:** Portfolio files and deployment workflow are prepared. The connected GitHub integration returned HTTP 403 (`Resource not accessible by integration`) when enabling Pages, so an administrator must complete steps 2–4 above. The site is not confirmed live. No other repository or hosting account was created.

## Customize

Edit `002/site/index.html` for your name, bio, projects, links, and contact details. Update `002/site/styles.css` for colors, typography, spacing, and layout. Keep assets inside `002/site/` so the workflow's upload scope remains complete. Do not add secrets, API keys, or private contact information.
