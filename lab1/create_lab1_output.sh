#!/bin/bash

# Script not authored by TA's but by someone in the CS360 discord. 

rm -f output.md

echo "| text | data | bss | dec | hex | filename |" >> output.md
echo "| :--- | :--- | :-- | :-- | :-- | :------- |" >> output.md

for i in {1..6}
do
    gcc -m32 "t$i.c"
    # ./a.out >> output.md
    printf `(size a.out | grep -v "text" | sed -e 's/\s\+/\|/g')` >> output.md
    echo "|" >> output.md
    rm a.out
done
