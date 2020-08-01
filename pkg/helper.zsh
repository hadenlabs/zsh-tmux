#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

# edittmux edit settings for tmux
function edittmux {
    if [ -z "${EDITOR}" ]; then
        message_warning "it's neccesary the var EDITOR"
        return
    fi
    "${EDITOR}" "${TMUX_FILE_SETTINGS}"
}
