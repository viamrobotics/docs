# Plan 03: Fix Alias reminder

**Status:** NOT STARTED
**Fixes:** `alias-reminder.yml` (the _Alias reminder_ job).
**Depends on:** nothing.

## Problem

On pull requests that rename or move `.md` files, this workflow should post a
sticky comment reminding the author to add redirect aliases. It currently never
posts, so authors get no reminder and broken redirects slip through.

## Root cause

The detection step emits its result with the deprecated `::set-output` workflow
command (`Write-Host "::set-output name=...::"`). GitHub has disabled
`::set-output`, so `steps.check_files_moved.outputs.*` is never populated. The
gate on the comment step (`== 'True'`) therefore never evaluates true, and the
comment step is dead.

## Plan

1. **Migrate to `$GITHUB_OUTPUT`.** Replace the `::set-output` writes in the
   PowerShell detection step with appends to the `GITHUB_OUTPUT` file. In `pwsh`:

   ```powershell
   "files_moved=$filesMoved" | Out-File -FilePath $env:GITHUB_OUTPUT -Append
   "moved_list=$movedList"   | Out-File -FilePath $env:GITHUB_OUTPUT -Append
   ```

   Keep the existing output names so the downstream `if:` does not need changing
   beyond confirming the comparison value (`'True'` vs `'true'`: normalize the
   value the step writes and the condition it is compared against).
2. **Handle multi-line output safely.** If `moved_list` can contain multiple
   filenames or newlines, use the heredoc form for `GITHUB_OUTPUT` so the value
   is not truncated:

   ```powershell
   "moved_list<<EOF"  | Out-File $env:GITHUB_OUTPUT -Append
   $movedList         | Out-File $env:GITHUB_OUTPUT -Append
   "EOF"              | Out-File $env:GITHUB_OUTPUT -Append
   ```

3. **Confirm the gate** on the sticky-comment step references the corrected
   output and boolean value.

## Verification

1. Open a test PR that renames a `.md` file under `docs/`.
2. Confirm the workflow runs (note: it triggers on `labeled` and `synchronize`,
   not `opened`, so push a change or apply a label after opening).
3. Confirm the sticky comment appears and lists the moved file.
4. Open a PR with no moved files and confirm no comment is posted.

## Rollback

Single-workflow change with no side effects beyond a PR comment; revert the
commit to restore the previous (non-posting) behavior.

## Risks and open questions

- The workflow uses `pull_request_target` and checks out the PR head SHA; keep
  the step limited to `git diff` and grep (no execution of PR code) to avoid the
  known elevated-token risk of that trigger.
- Consider adding `opened` to the trigger types so the reminder also fires when
  a PR is first opened with moved files, not only after a label or new push.
