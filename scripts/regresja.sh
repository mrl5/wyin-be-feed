#!/bin/bash

#Skrypt sprawdzający wszystkie możliwe (poprawne) godziny

 
hours=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23")
minutes=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23" "24" "25" "26" "27" "28" "29" "30" "31" "32" "33" "34" "35" "36" "37" "38" "39" "40" "41" "42" "43" "44" "45" "46" "47" "48" "49" "50" "51" "52" "53" "54" "55" "56" "57" "58" "59")  

which_endpoint=("event")
time_array=("00:00" "02:02")

if [ "$1" = "-all" ]
        then
          i=0
          for hour in ${hours[*]}
          do
           for minute in ${minutes[*]}
           do  
             time_array[i]="$hour:$minute"
             i=($i+1)
            done
          done  
fi
actual_year=`date +%Y`
if [ "$1" = "-actual" ]
        then
          i=0
          for hour in ${hours[*]}
          do
           for minute in ${minutes[*]}
           do  
             time_array[i]="$hour:$minute"
             i=$((i+1))
             if [ "$hour$minute" = "$actual_year" ]
             then
              break 2
             fi 
            done
          done  
fi

if [ "$1" = "-both" ] 
 then
 which_endpoint[1]="events"
fi 

echo ${which_endpoint[*]}


# running requests for values from time_array
day=`date +%Y-%m-%d_%H:%M:%S` #`date` `+%d-%m-%Y_%H:%M%:%S`
f_name="regres_log_$day.txt"
> ./logs/$f_name
> ./logs/"errors_$f_name"
for chosen_endpoint in ${which_endpoint[*]}
do
 for input_time in ${time_array[*]}
  do
  			echo "http://localhost:8080/history/$chosen_endpoint?t=$input_time"
  			#echo "curl -s -o /dev/null -w %{http_code} http://localhost:8080/history/$chosen_endpoint?t=$input_time"
 	    	wynik=$(curl -s -o /dev/null -w %{http_code} http://localhost:8080/history/$chosen_endpoint?t=$input_time) 
 	    	echo -e "$input_time   $wynik   $chosen_endpoint"  >> ./logs/$f_name 
 	    	  if [ "$wynik" != "200" ]
  				then
  				echo "$input_time   $wynik   $chosen_endpoint" >> ./logs/"errors_$f_name"
  			  fi
     #done
  done
done

 if ! [ -s "./logs/errors_$f_name" ] 
    then
        rm "./logs/errors_$f_name"
 fi
