#!/bin/sh

DIR=$1
if [ -z "$DIR" ] || [ ! -e "$DIR" ]; then
    echo "usage: $0 DIR"
    exit 1;
fi

OLDCWD=$(pwd)

JSONSTATS_EXEC="$OLDCWD/$(dirname $0)/jsonstats.py"
if [ -z "$JSONSTATS_EXEC" ] || [ ! -e "$JSONSTATS_EXEC" ]; then
    echo "'$JSONSTATS_EXEC' not found"
    exit 2;
fi

cd "$DIR"
for name in $(ls); do
    filename="$name/complex-Office-Open-XML-Part-1-Fundamentals-wordxml.xml.json"
    if [ -e "$filename" ]; then
        echo "Generating stats for converter '$name'..."
        cat "$filename" | "$JSONSTATS_EXEC"  > "$OLDCWD/stats-$name.txt"
    fi
done

cd "$OLDCWD"
