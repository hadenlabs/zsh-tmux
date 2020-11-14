#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

function tmux::internal::reattach-to-user-namespace::install {
    if ! type -p brew > /dev/null; then
        message_warning "${TMUX_MESSAGE_BREW}"
        return
    fi
    message_info "Installing reattach-to-user-namespace for ${TMUX_PACKAGE_NAME}"
    brew install reattach-to-user-namespace
    message_success "Installed reattach-to-user-namespace ${TMUX_PACKAGE_NAME}"
}

if ! type -p reattach-to-user-namespace > /dev/null; then tmux::internal::reattach-to-user-namespace::install; fi