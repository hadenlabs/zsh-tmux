#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

export TMUX_FILE_SETTINGS="${HOME}"/.tmux.conf
export TMUX_MESSAGE_BREW="Please install brew or use antibody bundle luismayta/zsh-brew branch:develop"
export TMUX_PACKAGE_NAME=tmux
export TMUX_TPM_PATH="${HOME}"/.tmux/plugins/tpm

[ -z "${EDITOR}" ] && export EDITOR="vim"