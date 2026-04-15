# Copilot Repository Instructions

## Reporting Rules (Required)

For every code or content change, always include a short report in the final response that explains:
1. What was changed.
2. Why the change was made.

This report must be present in the final response for each task, even for small edits.

## Work Done Note Update (Required)

For every code or content change, always update `WORK_DONE_NOTE.md` in the repository root.

Each new entry must include:
1. Date.
2. What changed.
3. Why the change was made.
4. Files touched.

Do not skip this update, even for small edits.

## Commit Rule (Required)

For every code or content change, always create a git commit after verification/tests succeed.

Commit requirements:
1. Stage only files related to the task.
2. Use a clear commit message describing the change.
3. Do not leave task-related changes uncommitted.

## GitFlow Branch Rule (Required)

For every new task, always create and work on a dedicated git branch before making changes.

GitFlow requirements:
1. Never work directly on `main`.
2. Never work directly on `develop`.
3. Create a branch that matches GitFlow intent (for example: `feature/...`, `hotfix/...`, `release/...`).
4. Keep commits scoped to the branch purpose.
5. Merge back through a pull request following the normal GitFlow path.

## "Finish Feature" Rule (Required)

When the user says "finish feature", always do all steps below in order:
1. Verify tests/checks relevant to the task.
2. Commit all task-related changes.
3. Push the branch.
4. Open a pull request to `main`.
5. Merge the pull request when mergeable.

Do not stop at a partial state when this command is used.
