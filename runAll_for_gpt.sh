if [[ $1 == "" ]]; then
 echo "give the saved file name (e.g., tinyc-r1)"
 exit
fi
python3 gpt.py Seed_Programs/tinyc/tinyc-train-r1/ $1
python3 grammar_from_csv.py $1 Seed_Programs/tinyc/parse_tinyc
python3 eval.py external Seed_Programs/tinyc/parse_tinyc Seed_Programs/tinyc/tinyc-test results/gpt_grammar_${1}
