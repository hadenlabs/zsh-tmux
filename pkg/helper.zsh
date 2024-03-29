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

# tx::project [name project] - create new tmux session with project template.
function tx::project {
    local name_project
    name_project="${1}"
    if [ -z "${name_project}" ]; then
        name_project=$(basename "$(pwd)")
    fi
    tmuxinator start project "${name_project}"
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

    session=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | fzf --exit-0) && tmux ${change} -t "${session}" || echo "No sessions found."
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
