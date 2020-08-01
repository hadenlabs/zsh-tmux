#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

#
# Defines install tmux for osx or linux.
#
# Authors:
#   Luis Mayta <slovacus@gmail.com>
#

ZSH_TMUX_PATH=$(dirname "${0}")

# shellcheck source=/dev/null
source "${ZSH_TMUX_PATH}"/config/main.zsh

# shellcheck source=/dev/null
source "${ZSH_TMUX_PATH}"/internal/main.zsh

# shellcheck source=/dev/null
source "${ZSH_TMUX_PATH}"/pkg/main.zsh
