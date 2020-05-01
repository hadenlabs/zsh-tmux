#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

#
# Defines install tmux for osx or linux.
#
# Authors:
#   Luis Mayta <slovacus@gmail.com>
#

ZSH_TMUX_ROOT=$(dirname "${0}")
TMUX_MESSAGE_BREW="Please install brew or use antibody bundle luismayta/zsh-brew branch:develop"
tmux_package_name=tmux


function tmux::install {
    message_info "Installing ${tmux_package_name}"
    if ! type -p brew > /dev/null; then
        message_warning "${TMUX_MESSAGE_BREW}"
        return
    fi
    brew install tmux
    message_success "Installed ${tmux_package_name}"
    tmux::post_install
}

function tpm::install {
    message_info "Installing tpm for ${tmux_package_name}"
    git clone https://github.com/tmux-plugins/tpm "${HOME}"/.tmux/plugins/tpm
    message_success "Installed tpm for ${tmux_package_name}"
}

function rsync::install {
    if ! type -p brew > /dev/null; then
        message_warning "${TMUX_MESSAGE_BREW}"
        return
    fi
    message_info "Installing rsync for ${tmux_package_name}"
    brew install rsync
    message_success "Installed rsync ${tmux_package_name}"
}

function tmux::dependences {
    message_info "Installing dependences for ${tmux_package_name}"
    message_success "Installed dependences for ${tmux_package_name}"
}

function tmux::post_install {
    message_info "Post Install ${tmux_package_name}"
    tmux::sync
    message_success "Success Install ${tmux_package_name}"
}

function tmux::sync {
    rsync -avzh --progress "${ZSH_TMUX_ROOT}/conf/" "${HOME}/"
}

if ! type -p tmux > /dev/null; then tmux::install; fi
if ! type -p rsync > /dev/null; then rync::install; fi
if [ ! -e "${HOME}/.tmux/plugins/tpm" ]; then tpm::install; fi
