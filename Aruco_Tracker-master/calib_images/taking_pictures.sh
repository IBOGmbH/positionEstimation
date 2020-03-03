#!/bin/bash

for i in {1..25}
do 
	echo "Going to take a picture ${i}"
	sleep 1s
	echo Taking a picture
	raspistill -o "Im${i}.jpg" 
	echo Picture taken, waiting for 1s
	sleep 0.5s

done
