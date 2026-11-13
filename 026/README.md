# Participate in discussions

- **Day:** 026
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Community
- **Primary GitHub:** `discussions`
- **Alternatives:** Discord, Slack
- **Slug:** `participate-in-discussions`

A small kit for asking useful questions, sharing ideas, and replying constructively in a project community. It includes a channel-selection guide, discussion templates, a sample question, and a local checker that catches missing context in a question draft. It never posts or contacts anyone.

## Try the question workflow

Read `PARTICIPATION_GUIDE.md`, then adapt `templates/question.md` and compare it with `samples/question-draft.md`. To check whether a draft has the basic sections and has replaced its placeholders, run:

```bash
python3 scripts/check_question.py samples/question-draft.md
python3 -m unittest discover -s tests -v
```

The checker is a writing aid, not a quality score: a complete template cannot guarantee that a question is answerable or that it belongs in the selected community. Follow the project’s own contribution rules, never include credentials or private user data, and keep the conversation respectful.

## References

GitHub describes Discussions as a place to ask and answer questions, share information, and gather ideas in [About Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions). Its [community conversation guidance](https://docs.github.com/en/discussions/guides/best-practices-for-community-conversations-on-github) recommends focused questions and follow-ups, then turning agreed work into an issue when appropriate. See also GitHub’s documentation on [discussion categories](https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-categories-for-discussions) and [participating in a discussion](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/participating-in-a-discussion).
