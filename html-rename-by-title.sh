#!/bin/bash

# a=1
for f in $(find . -type f | grep \.htm); do
   title=$(awk 'BEGIN{IGNORECASE=1;FS="<title>|</title>";RS=EOF} {print $2}' "$f")
   # mv -i "$f" "${a}-${title//[ ]/-}".html
   # ((a = a + 1))
   mv -i "$f" "${title//[ ]/-}".html
done

prename "s/\n//g" ./*
prename "y/A-Z/a-z/" ./*
