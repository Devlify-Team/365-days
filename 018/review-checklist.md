# Code review checklist

Use the checklist as a thinking aid, not a demand that every change be perfect. Follow the repository's own standards and scope.

## Understand the change

- Read the description and linked issue; restate the intended behavior in your own words.
- Check the base/head branches and inspect the full diff, one file at a time; open surrounding code when the diff alone is unclear.
- Confirm the change is focused and belongs in this component; note any parts outside your expertise.

## Look for meaningful risk

- **Design and function:** Does the change solve the intended problem for users and fit the system?
- **Boundaries and failures:** Consider empty, invalid, unusually large, or concurrent inputs where relevant. Are failures handled safely?
- **Security and privacy:** Check trust boundaries, permissions, sensitive data, and secret handling where the change touches them.
- **Tests:** Do tests cover changed behavior and important edge cases? Would they fail if the behavior broke? Are the tests understandable?
- **Complexity and maintenance:** Are names clear? Is the solution simpler than speculative generality? Are comments and documentation useful and accurate?
- **Scope:** Are generated files, unrelated changes, risky operations, or user-visible effects understood?

## Write useful feedback

A strong comment points to an observable behavior, explains the impact, and offers a question or concrete next step. For example: “Could this handle an empty list? The first item is accessed unconditionally, so an empty request currently raises an error. A guard or explicit validation would make the boundary clear.”

Separate a blocking correctness or safety issue from a suggestion. Mark purely optional polish as a nit when the team's conventions support that; do not block a sound change for personal style preferences. Include positive observations too. If you do not understand the intent, ask before treating an assumption as a defect.

## Decide and record scope

- Approve, comment, or request changes according to the actual repository's review rules.
- State what you reviewed, what checks you ran or did not run, and any area you could not verify.
- Re-review changed lines and relevant surrounding behavior after updates; do not treat a resolved thread as proof of correctness.

Project review policies differ. A checklist, green CI, or local linter cannot replace human review or repository-specific merge requirements.
