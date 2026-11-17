# Create your GitHub portfolio

- **Day:** 030
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Capstone
- **Primary GitHub:** `portfolio`
- **Alternative:** Personal website
- **Slug:** `create-your-github-portfolio`

This capstone turns a curated list of real projects into a profile-ready Markdown portfolio page. The sample highlights work from this challenge repository, links back to each project folder, and can be regenerated from `portfolio.json`. It uses no personal details, credentials, API calls, or extra repositories.

## Build and test

From this folder, run:

```bash
python3 scripts/build_portfolio.py
python3 -m unittest discover -s tests -v
```

The generator validates the portfolio fields, rejects duplicate project paths and missing targets, and writes `030/PORTFOLIO.md`. Review every project description and link before sharing it. To personalize the capstone, edit `portfolio.json` using projects you can verify and describe your role accurately.

## Use the result

`PORTFOLIO.md` is a compact portfolio page inside the existing `365-days` repository. You can link to it from your GitHub profile or personal website. This capstone does not create or modify another repository, profile, or hosted site.

GitHub's [README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) recommends using a README to explain a project's purpose and help people get started. For the separate account-level profile README feature, see [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).
