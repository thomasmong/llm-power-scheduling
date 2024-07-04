cpt=0
for f in *.txt
do
	echo "$f"
	s=$(cat "$f" | grep '^"' | wc -l)
	cpt=$(($cpt+$s))
done
echo $cpt
