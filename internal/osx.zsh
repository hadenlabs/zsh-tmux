#!/usr/bin/env ksh
# -*- coding: utf-8 -*-

if ! core::exists reattach-to-user-namespace; then core::install reattach-to-user-namespace; fi