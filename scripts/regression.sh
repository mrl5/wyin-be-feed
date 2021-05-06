#!/bin/bash

# Checks all or chosen time values for get/event and get events

hours=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23")
minutes=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23" "24" "25" "26" "27" "28" "29" "30" "31" "32" "33" "34" "35" "36" "37" "38" "39" "40" "41" "42" "43" "44" "45" "46" "47" "48" "49" "50" "51" "52" "53" "54" "55" "56" "57" "58" "59")

which_endpoint=("event")
time_array=("00:01" "02:02" "17:45") # here are set default values to check

port_value="8080"

if [ "$1" = "-port"  ]
 then
 port_value="$2"
 shift 2;
fi

if [ "$1" = "-both"  ]
 then
 which_endpoint[1]="events"
 shift 1;
elif [ "$1" = "-events" ]
 then
 which_endpoint[0]="events"
 shift 1;
fi

if [ "$1" = "-all_hours" ]
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

elif [ "$1" = "-real_hours" ]
	then
		i=0
        actual_year=`date +%Y`
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

elif [ "$1" = "-type_hours" ]; then
time_array=("")
shift 1;
i=1;
for input_param in "$@"
do
    time_array[$i]=$input_param
    i=$((i + 1));
done
fi


echo ${which_endpoint[*]}


# running requests for values from time_array
day=`date +%Y-%m-%d_%H:%M:%S`
f_name="reg_log_$day.txt"
> ./logs/$f_name
> ./logs/"errors_$day.txt"
for chosen_endpoint in ${which_endpoint[*]}
do
 for input_time in ${time_array[*]}
  do
        echo "http://localhost:$port_value/history/$chosen_endpoint?t=$input_time"
        wynik=$(curl -s -o /dev/null -w %{http_code} http://localhost:$port_value/history/$chosen_endpoint?t=$input_time)
 	    	echo -e "$input_time   $wynik   $chosen_endpoint"  >> ./logs/$f_name
 	    	  if [ "$wynik" != "200" ]
  				then
  				echo "$input_time   $wynik   $chosen_endpoint" >> ./logs/"errors_$f_name"
  			  fi

  done
done

 if ! [ -s "./logs/errors_$day.txt" ]
    then
        rm "./logs/errors_$day.txt"
 fi
