log_file=$1
log_file_to_get_time=$2
program_name=$3
result_file="Result.csv"
recall_sum=0
precision_sum=0
f1_sum=0
count=0
echo "$log_file"
if [ ! -f "$result_file" ]; then
    echo "program_name,recall,precision,f1,build_time,queries(oracle calls),llm_calls" > $result_file  
fi
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

    #printf "Average Recall: %.3f\n" "$avg_recall"
    #printf "Average Precision: %.3f\n" "$avg_precision"
    #printf "Average F1: %.3f\n" "$avg_f1"
    #printf "Average Recall: %.3f\nAverage Precision: %.3f\nAverage F1: %.3f\n" "$avg_recall" "$avg_precision" "$avg_f1"
    printf "%.3f,%.3f,%.3f\n" "$avg_recall" "$avg_precision" "$avg_f1"
else
    echo "No valid lines found."
fi

#Time spent building grammar: 939.0642974376678s
#Parse calls: 31396, 11717 
#LLM calls for bubble finding: 10
# === Time spent building grammar ===
# === Time spent building grammar ===
grammar_sum=0
grammar_count=0
while read -r line; do
    value=$(echo "$line" | grep -oP "Time spent building grammar: \K[0-9.]+" )
    grammar_sum=$(echo "$grammar_sum + $value" | bc -l)
    grammar_count=$((grammar_count + 1))
done < <(grep "Time spent building grammar:" "$log_file_to_get_time")

# === LLM calls for bubble finding ===
llm_sum=0
llm_count=0
while read -r line; do
    value=$(echo "$line" | grep -oP "LLM calls for bubble finding: \K[0-9]+")
    llm_sum=$(echo "$llm_sum + $value" | bc)
    llm_count=$((llm_count + 1))
done < <(grep "LLM calls for bubble finding:" "$log_file_to_get_time")

# === Parse calls (only first number) ===
parse_sum=0
parse_count=0
while read -r line; do
    value=$(echo "$line" | grep -oP "Parse calls: \K[0-9]+")
    parse_sum=$(echo "$parse_sum + $value" | bc)
    parse_count=$((parse_count + 1))
done < <(grep "Parse calls:" "$log_file_to_get_time")

# === Compute Averages ===
avg_grammar=$(echo "$grammar_count > 0" | bc -l) && [ "$avg_grammar" -eq 1 ] && avg_grammar=$(echo "$grammar_sum / $grammar_count" | bc -l) || avg_grammar=0
avg_llm=$(echo "$llm_count > 0" | bc -l) && [ "$avg_llm" -eq 1 ] && avg_llm=$(echo "$llm_sum / $llm_count" | bc -l) || avg_llm=0
avg_parse=$(echo "$parse_count > 0" | bc -l) && [ "$avg_parse" -eq 1 ] && avg_parse=$(echo "$parse_sum / $parse_count" | bc -l) || avg_parse=0

#grammar_sum=0
#grammar_count=0
#while read -r line; do
#    value=$(echo "$line" | cut -d':' -f2 | sed 's/s//g' | xargs)
#    grammar_sum=$(echo "$grammar_sum + $value" | bc -l)
#    grammar_count=$((grammar_count + 1))
#done < <(grep "Time spent building grammar:" "$log_file")
#
## === LLM calls for bubble finding ===
#llm_sum=0
#llm_count=0
#while read -r line; do
#    value=$(echo "$line" | cut -d':' -f2 | xargs)
#    llm_sum=$(echo "$llm_sum + $value" | bc)
#    llm_count=$((llm_count + 1))
#done < <(grep "LLM calls for bubble finding:" "$log_file")
#
## === Parse calls (only first number) ===
#parse_sum=0
#parse_count=0
#while read -r line; do
#    value=$(echo "$line" | cut -d':' -f2 | cut -d',' -f1 | xargs)
#    parse_sum=$(echo "$parse_sum + $value" | bc)
#    parse_count=$((parse_count + 1))
#done < <(grep "Parse calls:" "$log_file")
#
## === Print averages ===
#if [ "$grammar_count" -gt 0 ]; then
#    avg_grammar=$(echo "$grammar_sum / $grammar_count" | bc -l)
#else
#    avg_grammar=0
#fi
#
#if [ "$llm_count" -gt 0 ]; then
#    avg_llm=$(echo "$llm_sum / $llm_count" | bc -l)
#else
#    avg_llm=0
#fi
#
#if [ "$parse_count" -gt 0 ]; then
#    avg_parse=$(echo "$parse_sum / $parse_count" | bc -l)
#else
#    avg_parse=0
#fi

# Output in one line
printf "Avg Grammar Time:,Avg Parse Calls:,Avg LLM Calls:   %.3f,%.2f,%.2f\n" "$avg_grammar" "$avg_parse" "$avg_llm" 

echo "$program_name,$avg_recall,$avg_precision,$avg_f1,$avg_grammar,$avg_parse,$avg_llm" >> $result_file  
#echo -n ",$avg_grammar,$avg_parse,$avg_llm >> $result_file
