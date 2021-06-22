day=`date +%Y-%m-%d_%H:%M:%S`
f_name="log_dates_$day.txt"
> ./logs/$f_name


for i in {1501..2023};
do
  rok="$i";
  echo $rok "    " >> ./logs/$f_name;
  wynik=$(curl -sb -H 'GET'   "https://wyin-be-feed-2wmi3dgqxq-ez.a.run.app/history/event/$rok?lang=pl" 'accept: application/json');
  echo ${wynik}  >> ./logs/$f_name;
  echo "" >> ./logs/$f_name;
  echo $i;
done
