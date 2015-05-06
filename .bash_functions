#!/usr/bin/bash

function fname() { find . -name "$@"; }

function psgrep() { ps aux | grep -v grep | grep "$@" -i --color=auto; }

function svnlist {
    svn list $REPO/$@ | lolcat
}

function svnlog {
    echo svn log -l10 --stop-on-copy $REPO/"$@"
    svn log -l10 --stop-on-copy $REPO/"$@" | lolcat
}

function findlibs() {
    # Finds all the header files and/or libs installed by the specified packages
    rpm -ql $@ | egrep '/(include|lib)' | sort
}

function jp() {
    javap $@ | colout ".*" java
}

function jpv() {
    javap -v -c -private $@ | colout ".*" java
}

function cless() {
    pygmentize -g $@ | less -R
}
