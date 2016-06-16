#!/bin/sh

PROJ=`find . -name '*.xib' -o -name '*.[mh]' -o -name '*.storyboard' -o -name '*.mm' `

#echo "Looking for in files: $PROJ"

find . -iname '*.png' -print0 | while read -d $'\0' png
do
name=`basename -s .png "$png"`
name=`basename -s @2x $name`
name=`basename -s @3x $name`

if grep -qhs "$name" $PROJ; then
#echo "(used - $png)"
echo "----------"
else
echo "!!!UNUSED - $png"
fi
done