#!/bin/bash
	echo "compiling file"
	cc -m32 -w -static $1	
	echo "size of a.out "
	ls -l a.out
	echo "executable sizes " 
	size a.out

