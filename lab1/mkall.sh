
#!/bin/bash/

for I in 1 2 3 4 5 6
do
	echo ./mk.sh t$I.c
	./mk.sh t$I.c
done

