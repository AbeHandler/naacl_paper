declare -a arr=("a" "n" "r" "s" "v")
declare -a types=("hyper", "hypo", "syn", "holo", "mero")

rm textfiles/a.txt
rm textfiles/n.txt
rm textfiles/r.txt
rm textfiles/s.txt
rm textfiles/v.txt

## now loop through the above array
for pos in "${arr[@]}"
do
    cat textfiles/results.txt | grep -v 'not_in_wordnet' | grep -v 'same stem' | grep -v 'total' | grep -v 'none' | grep ",""$pos""," | python get_pos_count.py > textfiles/"$pos".txt
done

python pos_chi_squared.py > pos_chi_squared.txt
