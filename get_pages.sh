#!/bin/bash

for i in {1..500}
do 
	touch ./scraped/${i}.html
	curl "https://www.lehighsports.com/schedule.aspx?schedule=${i}" >> ./scraped/${i}.html
done
