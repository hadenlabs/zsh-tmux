#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

function internal::main::factory {
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

internal::main::factory

if ! type -p rsync > /dev/null; then rync::install; fi
if ! type -p tmux > /dev/null; then tmux::install; fi
[ -e "${TMUX_TPM_PATH}" ] || tpm::install