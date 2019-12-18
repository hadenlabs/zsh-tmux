#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

#
# Defines install tmux for osx or linux.
#
# Authors:
#   Luis Mayta <slovacus@gmail.com>
#
tmux_package_name=tmux


function tmux::install {
    message_info "Installing ${tmux_package_name}"
    if ! type -p brew > /dev/null; then
        message_error "it's neccesary brew, add: luismayta/zsh-brew"
    fi
    brew install tmux
    message_success "Installed ${tmux_package_name}"
}

function tpm::install {
    message_info "Installing tpm for ${tmux_package_name}"
    git clone https://github.com/tmux-plugins/tpm "${HOME}"/.tmux/plugins/tpm
    message_success "Installed tpm for ${tmux_package_name}"
}

function rsync::install {
    if ! type -p brew > /dev/null; then
        message_error "it's neccesary brew, add: luismayta/zsh-brew"
    fi
    message_info "Installing rsync for ${tmux_package_name}"
    brew install rsync
    message_success "Installed rsync ${tmux_package_name}"
}

if ! type -p tmux > /dev/null; then tmux::install; fi
if ! type -p rsync > /dev/null; then rync::install; fi
if [ ! -e "${HOME}/.tmux/plugins/tpm" ]; then tpm::install; fi

function tmux::dependences {
    message_info "Installing dependences for ${tmux_package_name}"
    message_success "Installed dependences for ${tmux_package_name}"
}

function tmux::post_install {
    message_info "Post Install ${tmux_package_name}"
    message_success "Success Install ${tmux_package_name}"
}

function tmux::sync {
    rsync -avzh --progress "${ZSH_TMUX_ROOT}/conf/" "${HOME}/"
}

tmux::sync
