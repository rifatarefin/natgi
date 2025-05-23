
#log_file=$1
#ans=$(grep -r "Recall: " $log_file)
#echo $ans
##grep -o "Recall: [0-9.]*, Precision: [0-9.]*, F-1: [0-9.]*" "$log_file" | \
##awk '
##{
##    split($2, r, ":"); recall_sum += r[2];
##    split($4, p, ":"); precision_sum += p[2];
##    split($6, f, ":"); f1_sum += f[2];
##    count++;
##}
##END {
##    if (count > 0) {
##        printf "Average Recall: %.3f\n", recall_sum / count;
##        printf "Average Precision: %.3f\n", precision_sum / count;
##        printf "Average F1: %.3f\n", f1_sum / count;
##    } else {
##        print "No matching lines found.";
##    }
##}'
## Get the line with all metrics
#line=$(grep -o "Recall: [0-9.]*, Precision: [0-9.]*, F-1: [0-9.]*" "$log_file")
#
## Convert it to one item per line and feed to awk
#echo "$line" | tr ' ' '\n' | awk '
#BEGIN { recall_sum=0; precision_sum=0; f1_sum=0; count=0 }
#/^Recall:/ {
#    split($0, a, ":");
#    recall_sum += a[2];
#    count++;
#}
#/^Precision:/ {
#    split($0, a, ":");
#    precision_sum += a[2];
#}
#/^F-1:/ {
#    split($0, a, ":");
#    f1_sum += a[2];
#}
#END {
#    if (count > 0) {
#        printf "Average Recall: %.3f\n", recall_sum / count;
#        printf "Average Precision: %.3f\n", precision_sum / count;
#        printf "Average F1: %.3f\n", f1_sum / count;
#    } else {
#        print "No scores found.";
#    }
#}'
#!/bin/bash

log_file=$1

recall_sum=0
precision_sum=0
f1_sum=0
count=0

while IFS= read -r line; do
    recall=$(echo "$line" | grep -oP "Recall: \K[0-9.]+" )
    precision=$(echo "$line" | grep -oP "Precision: \K[0-9.]+" )
    f1=$(echo "$line" | grep -oP "F-1: \K[0-9.]+" )

    recall_sum=$(echo "$recall_sum + $recall" | bc -l)
    precision_sum=$(echo "$precision_sum + $precision" | bc -l)
    f1_sum=$(echo "$f1_sum + $f1" | bc -l)
    count=$((count + 1))
done < <(grep "^Recall:" "$log_file")

if [ "$count" -gt 0 ]; then
    avg_recall=$(echo "$recall_sum / $count" | bc -l)
    avg_precision=$(echo "$precision_sum / $count" | bc -l)
    avg_f1=$(echo "$f1_sum / $count" | bc -l)

    printf "Average Recall: %.3f\n" "$avg_recall"
    printf "Average Precision: %.3f\n" "$avg_precision"
    printf "Average F1: %.3f\n" "$avg_f1"
else
    echo "No valid lines found."
fi

