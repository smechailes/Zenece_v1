# Git workflow

`main` is the stable branch. Start every task from an up-to-date `main` branch
using the helper below:

```sh
./scripts/start-task.sh feature investor-dashboard
./scripts/start-task.sh templating refresh-hero
./scripts/start-task.sh fix mobile-overflow
```

Allowed task categories are `feature`, `templating`, `fix`, `docs`, `chore`, and
`refactor`. The helper creates branches such as `feature/investor-dashboard`.

Commits use [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat(scope): add something       # minor release
fix(scope): correct something    # patch release
feat(scope)!: change a contract  # major release
```

Enable the local commit hook once after cloning:

```sh
./scripts/setup-git.sh
```

To create the next release, merge work into `main`, ensure the tree is clean,
and run:

```sh
./scripts/release.sh
```

The script reads `VERSION`, inspects Conventional Commits since the last tag,
updates the SemVer value, creates a release commit, and adds an annotated tag.
Push the commit and tag with `git push origin main --follow-tags`.