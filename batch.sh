for i in 1 2 3 4 5 6 7 8 9 10 11
do
 echo lecture_$1
 python create_user_script.py lecture_${i} lecture_${i} 200 $1 $2
done

for j in 1 2 3 4 5 6 7 8 9 10 11
do
 echo lab_$1
 python create_user_script.py lab_${j} lab_${j} 200 $1 $2
done
