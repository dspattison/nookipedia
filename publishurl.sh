#!/bin/sh

set -x #debug
set -e #error

base=/Volumes/nook/my\ downloads
target_dir=$base/sync

ls "$base"
mkdir -p "$target_dir"

tmp=.
#tmp=`mktemp -d -t dave`
#mkdir -p $tmp_dir

curl $1 > $tmp/$1.html

ebook-convert $tmp/$1.html $tmp/$1.epub

cp $tmp/$1.epub "$target_dir"
