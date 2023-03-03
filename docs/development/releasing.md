# Release workflow

1. Fill the `CHANGELOG.md`
1. Change the version number in `__about__.py`
1. Commit changes with a message like `Bump version to X.x.x`
1. Apply a git tag with the relevant version: `git tag -a 0.3.0 {git commit hash} -m "New awesome feature"`
1. Push commit and tag to main branch: `git push --tags`
