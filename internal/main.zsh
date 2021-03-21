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

if ! core::exists rsync; then core::install rsync; fi
if ! core::exists tmux; then tmux::internal::tmux::install; fi
[ -e "${TMUX_TPM_PATH}" ] || tmux::internal::tpm::install
