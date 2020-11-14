#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

if ! type -p reattach-to-user-namespace > /dev/null; then tmux::internal::reattach-to-user-namespace::install; fi
