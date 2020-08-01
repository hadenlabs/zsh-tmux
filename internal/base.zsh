#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

function tmux::install {
    message_info "Installing ${TMUX_PACKAGE_NAME}"
    if ! type -p brew > /dev/null; then
        message_warning "${TMUX_MESSAGE_BREW}"
        return
    fi
    brew install tmux
    message_success "Installed ${TMUX_PACKAGE_NAME}"
    tmux::post_install
}

function tmuxinator::install {
    message_info "Installing tmuxinator for ${TMUX_PACKAGE_NAME}"
    if ! type -p gem > /dev/null; then
        message_warning "${TMUX_MESSAGE_RVM}"
        return
    fi
    gem install tmuxinator
    message_success "Installed tmuxinator for ${TMUX_PACKAGE_NAME}"
}

function tpm::install {
    message_info "Installing tpm for ${TMUX_PACKAGE_NAME}"
    git clone https://github.com/tmux-plugins/tpm "${TMUX_TPM_PATH}"
    message_success "Installed tpm for ${TMUX_PACKAGE_NAME}"
}

function rsync::install {
    if ! type -p brew > /dev/null; then
        message_warning "${TMUX_MESSAGE_BREW}"
        return
    fi
    message_info "Installing rsync for ${TMUX_PACKAGE_NAME}"
    brew install rsync
    message_success "Installed rsync ${TMUX_PACKAGE_NAME}"
}

function tmux::dependences {
    message_info "Installing dependences for ${TMUX_PACKAGE_NAME}"
    message_success "Installed dependences for ${TMUX_PACKAGE_NAME}"
}

function tmux::post_install {
    message_info "Post Install ${TMUX_PACKAGE_NAME}"
    tmux::sync
    message_success "Success Install ${TMUX_PACKAGE_NAME}"
}

function tmux::sync {
    rsync -avzh --progress "${ZSH_TMUX_PATH}/conf/" "${HOME}/"
}

