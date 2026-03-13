<!-- Space: Projects -->
<!-- Parent: ZshTmux -->
<!-- Title: Contributing ZshTmux -->
<!-- Label: ZshTmux -->
<!-- Label: Contributing -->
<!-- Include: disclaimer.md -->
<!-- Include: ac:toc -->

# How To Contribute

Contributions to zsh-tmux are welcome.

Feel free to use all of the contribution options:

- Contribute to zsh-tmux repositories on [GitHub](https://github.com/hadenlabs/zsh-tmux). See [Git flow](./contribute/github-flow.md).

## Getting Started

### Development

In general, MRs are welcome. We follow the typical "fork-and-pull" [Github flow](./contribute/github-flow.md).

1. **Fork** the repo on Github
2. **Clone** the project to your own machine
3. **Commit** changes to your own branch using [Github Flow](./contribute/github-flow.md)
4. **Push** your work back up to your fork

5. Submit a **Pull Request** so that we can review your changes

**NOTE:** Be sure to rebase the latest changes from "upstream" before making a pull request!

## Styleguides

### Git Commit Messages

Your commit messages should serve these 3 important purposes:

- To speed up the reviewing process.
- To provide the least amount of necessary documentation
- To help the future maintainers.

Follow the repository commit format enforced by commitlint: `<type> <emoji> (<scope>): <subject>`. The repository currently accepts scopes `core`, `accounts`, and `ci`, with a maximum subject length of 100 characters.

**chore**: something just needs to happen, e.g. versioning

**docs**: documentation pages in `docs/` or docstrings

**feat**: new code in `./`

**fix**: code improvement in `./`

**refactor**: code movement in `./`

**style**: aesthetic changes

**test**: test case modifications in `test/`

Examples commit messages:

- chore 🧹 (core): refresh release metadata
- docs 📚 (core): update configuration paths
- feat ✨ (core): add tmux workflow helpers
- fix 🐛 (core): correct sync destination
- refactor 🎨 (core): simplify tmux helper flow
- style 💄 (core): normalize shell formatting
- test 🧪 (core): cover sync commands

**Keep it short and simple!**

### Branches

See [Github Flow](./contribute/github-flow.md).

### Documentation

Documentation is part of the zsh-tmux code base. You can find the documentation files in the `docs/` directory of the [main repository](https://github.com/hadenlabs/zsh-tmux). `README.md` is generated from `provision/generators/README.yaml`, `provision/templates/README.tpl.md`, and the included files under `docs/`.

### Testing

See [Testing](./testing.md).

### Code Submission

1. See if a [Pull Request](https://github.com/hadenlabs/zsh-tmux/pulls) exists
   - Add some comments or review the code to help it along
   - Don\'t be afraid to comment when logic needs clarification
2. Create a Fork and open a [Pull Request](https://github.com/hadenlabs/zsh-tmux/pulls) if needed

### Code Review

- Anyone can review code
- Any [Pull Request](https://github.com/hadenlabs/zsh-tmux/pulls) should be closed or merged within a week

### Code Acceptance

Try to keep history as linear as possible using a [rebase] merge strategy.
