<!-- Space: Projects -->
<!-- Parent: ZshTmux -->
<!-- Title: EnvVars ZshTmux -->
<!-- Label: ZshTmux -->
<!-- Label: Project -->
<!-- Label: EnvVars -->
<!-- Include: disclaimer.md -->
<!-- Include: ac:toc -->

---

## Env Vars

### Application

- `HOME_CONFIG_PATH`: base config directory used for synced assets, default `${HOME}/.config`
- `TMUX_FILE_SETTINGS`: target tmux config file, default `${HOME}/.tmux.conf`
- `TMUX_PACKAGE_NAME`: package identifier used in plugin messages
- `TMUX_CONFIG_DIR`: target tmux config directory, default `${HOME_CONFIG_PATH}/tmux`
- `TMUX_TPM_PATH`: target path for the tmux plugin manager installation
- `TMUXINATOR_TEMPLATE_DIR`: directory scanned by `tx::project` for tmuxinator templates
- `TMUXINATOR_DEFAULT_TEMPLATE`: fallback tmuxinator template name when no selection is made
- `EDITOR`: editor used by `edittmux`; defaults to `vim` when unset
