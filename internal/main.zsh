#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

function tmux::internal::main::factory {
    # shellcheck source=/dev/null
    source "${ZSH_TMUX_PATH}"/internal/base.zsh
    case "${OSTYPE}" in
    darwin*)
        # shellcheck source=/dev/null
        source "${ZSH_TMUX_PATH}"/internal/osx.zsh
        ;;
    linux*)
        # shellcheck source=/dev/null
        source "${ZSH_TMUX_PATH}"/internal/linux.zsh
      ;;
    esac
}

tmux::internal::main::factory

if ! type -p rsync > /dev/null; then tmux::internal::rync::install; fi
if ! type -p tmux > /dev/null; then tmux::internal::tmux::install; fi
if ! type -p tmuxinator > /dev/null; then tmux::internal::tmuxinator::install; fi
[ -e "${TMUX_TPM_PATH}" ] || tmux::internal::tpm::install
