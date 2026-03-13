## Functions

zsh tmux includes a small utility `tmux`.

### Public functions and aliases

#### `tmux::dependences`

Checks and installs the dependencies required by the plugin.

#### `tmux::post_install`

Runs the post-install sync flow for tmux and tmuxinator assets.

#### `tmux::sync`

Synchronizes `data/conf/.tmux.conf` into `${HOME}/` and `data/sync/` into `${HOME_CONFIG_PATH}/`.

#### `tmux::install`

Installs tmux using the platform-specific implementation.

#### `edittmux`

Opens `${TMUX_FILE_SETTINGS}` in the configured `${EDITOR}`.

#### `tx::project` `name_project`

Selects a tmuxinator template with `fzf` and starts a tmuxinator project. If no name is passed, it uses the current directory name.

#### `tx`

Alias for `tmuxinator` when the command is available.

#### `ftm`

Creates a new tmux session or switches to an existing one.

#### `ftmk`

Deletes a tmux session.
