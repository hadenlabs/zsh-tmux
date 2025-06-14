#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

# edittmux edit settings for tmux
function edittmux {
    if [ -z "${EDITOR}" ]; then
        message_warning "it's necessary the var EDITOR"
        return
    fi
    "${EDITOR}" "${TMUX_FILE_SETTINGS}"
}

# tx::project [name project].
# Description: Select a tmuxinator template interactively with fzf and start a new project session.
function tx::project {
  local selected_template project_name

  if ! core::exists tmuxinator; then
    message_error "tmuxinator is not installed."
    return 1
  fi

  # List all yml templates
  local templates=()
  while IFS= read -r template; do
    templates+=("$template")
  done < <(find "${TMUXINATOR_TEMPLATE_DIR}" -maxdepth 1 -name '*.yml' -exec basename -s .yml {} \;)

  if (( ${#templates[@]} == 0 )); then
    message_warning "No templates found in ${TMUXINATOR_TEMPLATE_DIR}"
    return 1
  fi

  selected_template=$(printf '%s\n' "${templates[@]}" | fzf --prompt="Select tmuxinator template: ") || selected_template="${TMUXINATOR_DEFAULT_TEMPLATE}"
  project_name=${1:-$(basename "$PWD")}

  message_info "Launching tmuxinator project '${project_name}' with template '${selected_template}'..."
  tmuxinator start "${selected_template}" "${project_name}"
}

# ftm [SESSION_NAME | FUZZY PATTERN] - create new tmux session, or switch to existing one.
# Running `tm` will let you fuzzy-find a session mame
# Passing an argument to `ftm` will switch to that session if it exists or create it otherwise
function ftm {
    [[ -n "${TMUX}" ]] && change="switch-client" || change="attach-session"
    if [ -n "${1}" ]; then
        tmux "${change}" -t "${1}" 2>/dev/null \
            || (tmux new-session -d -s "${1}" && tmux "${change}" -t "${1}"); return
    fi

    session=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | fzf --exit-0) && tmux "${change}" -t "${session}" || echo "No sessions found."
}

# ftmk [SESSION_NAME | FUZZY PATTERN] - delete tmux session
# Running `tm` will let you fuzzy-find a session mame to delete
# Passing an argument to `ftm` will delete that session if it exists
function ftmk {
    if [ -n "${1}" ]; then
        tmux kill-session -t "${1}"; return
    fi
    session=$(tmux list-sessions -F "#{session_name}" 2>/dev/null \
        | fzf --exit-0) && tmux kill-session -t "${session}" || echo "No session found to delete."
}