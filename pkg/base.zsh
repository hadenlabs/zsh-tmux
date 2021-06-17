#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

function tmux::dependences {
    message_info "Installing dependences for ${TMUX_PACKAGE_NAME}"
    message_success "Installed dependences for ${TMUX_PACKAGE_NAME}"
}

function tmux::install {
    tmux::internal::tmux::install
}

function tmux::post_install {
    message_info "Post Install ${TMUX_PACKAGE_NAME}"
    tmux::sync
    message_success "Success Install ${TMUX_PACKAGE_NAME}"
}

function tmux::sync {
    rsync -avzh --progress "${ZSH_TMUX_PATH}/conf/" "${HOME}/"
    rsync -avzh --progress "${ZSH_TMUX_PATH}/conf/sync/tmuxinator/" "${TMUXINATOR_CONFIG_PATH}/"
}
