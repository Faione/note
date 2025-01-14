## MdBook

[tutorial](https://rust-lang.github.io/mdBook/)

## Continuouse Integration

mdbook可以通过GitHub Actions或者GitLab CI/CD来进行CICD

[^2] [cicd](https://rust-lang.github.io/mdBook/continuous-integration.html)

```yaml
```yaml
name: Deploy
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # To push a branch 
      pull-requests: write  # To create a PR from that branch
    steps:
    - uses: actions/checkout@v3 # using checkout actions to retrive code
      with:
        fetch-depth: 0
    - name: Install mdbook
      run: |
        mkdir mdbook
        curl -sSL https://github.com/rust-lang/mdBook/releases/download/v0.4.27/mdbook-v0.4.27-x86_64-unknown-linux-gnu.tar.gz | tar -xz --directory=./mdbook
        echo `pwd`/mdbook >> $GITHUB_PATH
    - name: Deploy GitHub Pages
      run: |
        # This assumes your book is in the root of your repository.
        # Just add a `cd` here if you need to change to another directory.
        mdbook build
        git worktree add gh-pages
        git config user.name "Deploy from CI"
        git config user.email ""
        cd gh-pages
        # Delete the ref to avoid keeping history.
        git update-ref -d refs/heads/gh-pages
        rm -rf *
        mv ../book/* .
        git add .
        git commit -m "Deploy $GITHUB_SHA to gh-pages"
        git push --force --set-upstream origin gh-pages
```
```