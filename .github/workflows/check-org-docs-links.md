# `ORG_REPO_READ_TOKEN` setup for the org docs-link check

The nightly [`check-org-docs-links.yml`](./check-org-docs-links.yml) job clones
each target repo and scans it for `docs.viam.com` links. Public repos (`rdk`,
`api`, `viam-python-sdk`, `viam-typescript-sdk`, `viam-flutter-sdk`) clone
tokenless. The **private `app` repo** needs a read token; without it the job
scans the other repos and logs a warning (it does **not** fail).

Provide the token as the repository secret **`ORG_REPO_READ_TOKEN`**. Two ways to
create one — a fine-grained PAT is simplest.

## Option A — fine-grained personal access token (recommended)

1. GitHub → **Settings → Developer settings → Fine-grained personal access
   tokens → Generate new token**.
2. **Resource owner:** `viamrobotics`.
3. **Repository access:** *Only select repositories* → `viamrobotics/app` (add
   any other private repos you later add to the scan).
4. **Permissions:** Repository permissions → **Contents: Read-only**. Nothing
   else is needed (the job only clones).
5. **Expiration:** pick a policy your org allows (e.g. 90 days) and set a
   calendar reminder to rotate — an expired token silently drops `app` from the
   scan (the job warns, doesn't fail).
6. Generate. If the org requires approval for fine-grained tokens, an org owner
   approves the request before it works.

Ideally create the token from a **service/bot account** with read access to
`app`, not a personal account, so the scan does not depend on one person's
membership.

## Option B — GitHub App installation token

If the org prefers Apps over PATs: install (or reuse) a GitHub App with
**Contents: Read** on `app`, mint an installation token in the workflow (e.g.
`actions/create-github-app-token`), and pass it in place of the PAT. This adds a
step to the workflow but avoids PAT expiry/rotation.

## Add the secret

Repo → **Settings → Secrets and variables → Actions → New repository secret**:

- **Name:** `ORG_REPO_READ_TOKEN`
- **Value:** the token from Option A or B

The workflow uses it only for the private clone:

```bash
git clone --filter=blob:none --depth 1 \
  "https://x-access-token:${ORG_REPO_READ_TOKEN}@github.com/viamrobotics/app.git" \
  repos/app
```

## Verify

Run the workflow manually (**Actions → Org docs-link check → Run workflow**) and
confirm the log shows `Cloning private app ...` rather than the
`ORG_REPO_READ_TOKEN not set; skipping private 'app' repo.` warning.
