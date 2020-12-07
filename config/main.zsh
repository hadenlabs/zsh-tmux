#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

function tmux::config::main::factory {
    # shellcheck source=/dev/null
    source "${ZSH_TMUX_PATH}"/config/base.zsh
    case "${OSTYPE}" in
    darwin*)
        # shellcheck source=/dev/null
        source "${ZSH_TMUX_PATH}"/config/osx.zsh
        ;;
    linux*)
        # shellcheck source=/dev/null
        source "${ZSH_TMUX_PATH}"/config/linux.zsh
      ;;
    esac
}

tmux::config::main::factory
