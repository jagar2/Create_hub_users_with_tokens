for i in 1 2 3 4 5 6 7 8 9 10 11
do
 echo Lecture_$1
 python create_user_script.py Lecture_${i} Lecture_${i} 200 $1 $2
done

for i in 1 2 3 4 5 6 7 8 9 10 11
do
 echo Lab_$1
 python create_user_script.py Lab_${i} Lab_${i} 200 $1 $2
done
