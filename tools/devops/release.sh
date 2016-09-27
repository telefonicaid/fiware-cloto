#!/bin/sh
#
# Copyright 2016 Telefónica I+D
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

#
# Prepare a new release or hotfix for this component, automatically including
# release spec in dockerfiles (changes are committed into a new "release/X.Y.Z"
# branch or in the already existing "hotfix/???").
#
# Usage:
#   $0 [RELEASE_NUMBER]
#   $0 --help
#
# Options:
#   -h, --help		show this help message and exit
#

OPTS='h(help)'
PROG=$(basename $0)

# Command line options
RELEASE_NUMBER=

# Command line processing
OPTERR=
OPTSTR=$(echo :-:$OPTS | sed 's/([a-zA-Z0-9]*)//g')
OPTHLP=$(sed -n '20,/^$/ { s/$0/'$PROG'/; s/^#[ ]\?//p }' $0)
while getopts $OPTSTR OPT; do while [ -z "$OPTERR" ]; do
case $OPT in
'h')	OPTERR="$OPTHLP";;
'?')	OPTERR="Unknown option -$OPTARG";;
':')	OPTERR="Missing value for option -$OPTARG";;
'-')	OPTLONG="${OPTARG%=*}";
	OPT=$(expr $OPTS : ".*\(.\)($OPTLONG):.*" '|' '?');
	if [ "$OPT" = '?' ]; then
		OPT=$(expr $OPTS : ".*\(.\)($OPTLONG).*" '|' '?')
		OPTARG=-$OPTLONG
	else
		OPTARG=$(echo =$OPTARG | cut -d= -f3)
		[ -z "$OPTARG" ] && { OPTARG=-$OPTLONG; OPT=':'; }
	fi;
	continue;;
esac; break; done; done
shift $(expr $OPTIND - 1)
[ -n "${RELEASE_NUMBER:=$1}" ] && shift
[ -z "$OPTERR" -a -n "$*" ] && OPTERR="Too many arguments"
[ -n "$OPTERR" ] && {
	PREAMBLE=$(printf "$OPTHLP" | sed -n '0,/^Usage:/ p' | head -n -1)
	USAGE="Usage:\n"$(printf "$OPTHLP" | sed '0,/^Usage:/ d')"\n\n"
	TAB=4; LEN=$(echo "$USAGE" | awk -F'\t' '/ .+\t/ {print $1}' | wc -L)
	TABSTOPS=$TAB,$(((LEN/TAB+2)*TAB)); WIDTH=${COLUMNS:-$(tput cols)}
	[ "$OPTERR" != "$OPTHLP" ] && PREAMBLE="ERROR: $OPTERR"
	printf "$PREAMBLE\n\n" | fmt -$WIDTH 1>&2
	printf "$USAGE" | tr -s '\t' | expand -t$TABSTOPS | fmt -$WIDTH -s 1>&2
	exit 1
}

# Common properties
PROGDIR=$(readlink -f $(dirname $0))
BASEDIR=$(readlink -f $PROGDIR/../..)
CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Component properties
DOCKERFILE=$BASEDIR/docker/Dockerfile

# Function to check current branch
check_current_branch() {
	if [ -n "$(expr $CUR_BRANCH : '^\(release/.*\)$')" ]; then
		RELEASE_NUMBER=${CUR_BRANCH#release/}
		return 0
	elif [ -z "$(expr $CUR_BRANCH : '^\(develop\|hotfix/.*\)$')" ]; then
		printf "Must change to develop or hotfix branch first\n" 1>&2
		return 1
	elif [ "$CUR_BRANCH" = "develop" -a -z "$RELEASE_NUMBER" ]; then
		printf "Missing release number (type \`$PROG --help')\n" 1>&2
		return 1
	fi
}

# Function to create a new "release/X.Y.Z" branch if needed
get_changelog_branch() {
	if [ "$CUR_BRANCH" = "develop" ]; then
		git checkout -b release/$RELEASE_NUMBER
	fi
}

# Function to change release when needed
bump_new_release() {
	[ -n "$RELEASE_NUMBER" ] || return 0
	cd $PROGDIR
	bumpversion \
		--commit --no-tag --allow-dirty \
		--new-version=$RELEASE_NUMBER \
		--message='New release {new_version}' \
		--search='GIT_REV develop' \
		--replace='GIT_REV {new_version}' \
		patch $DOCKERFILE
}

# Main
check_current_branch \
&& get_changelog_branch \
&& bump_new_release
