# How to use this project

## What the plugin does

The plugin loads tmux helpers, installs missing runtime dependencies, and synchronizes the repository assets into the expected tmux paths in your home directory.

## Post-install behavior

When the plugin is loaded, it ensures the required tools are available and then keeps these paths aligned with the repository data:

- `data/conf/.tmux.conf` -> `${HOME}/.tmux.conf`
- `data/sync/tmux/` -> `${HOME_CONFIG_PATH}/tmux/`
- `data/sync/tmuxinator/templates/` -> `${HOME_CONFIG_PATH}/tmuxinator/templates/`

## Common workflow

1. Install the plugin with your preferred zsh plugin manager.
2. Run `task setup` if you are developing in this repository.
3. Reload your shell.
4. Use `tmux::post_install` or `tmux::sync` if you need to resync the local tmux assets manually.

## Interactive helpers

- `edittmux` opens the generated tmux config file in `${EDITOR}`
- `tx::project` lets you select a tmuxinator template with `fzf`
- `ftm` switches to or creates tmux sessions
- `ftmk` deletes tmux sessions
