#for i in {1..50}; do bash runAll_for_gpt.sh  tinyc-r1-$i; done |& tee log
if [[ $1 == "" ]]; then
 echo "give the saved file name (e.g., tinyc-r1)"
 exit
fi

if [[ $1 == tinyc-r1-* ]]; then
    python3 gpt.py Seed_Programs/tinyc/tinyc-train-r1/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/tinyc/parse_tinyc
    python3 eval.py external Seed_Programs/tinyc/parse_tinyc Seed_Programs/tinyc/tinyc-test results/gpt_grammar_${1}

elif [[ $1 == curl-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  curl-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/curl/curl-train-r1/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/curl/parse_curl
    python3 eval.py external Seed_Programs/curl/parse_curl Seed_Programs/curl/curl-test results/gpt_grammar_${1}

elif [[ $1 == microbench-json-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  microbench-json-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/micro-benchmarks/json/guides-r1/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/micro-benchmarks/json/parse_json
    python3 eval.py external Seed_Programs/micro-benchmarks/json/parse_json Seed_Programs/micro-benchmarks/json/test_set results/gpt_grammar_${1}

elif [[ $1 == microbench-lisp-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  microbench-lisp-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/micro-benchmarks/lisp/guides-r1/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/micro-benchmarks/lisp/parse_lisp
    python3 eval.py external Seed_Programs/micro-benchmarks/lisp/parse_lisp Seed_Programs/micro-benchmarks/lisp/test_set results/gpt_grammar_${1}


elif [[ $1 == microbench-turtle-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  microbench-turtle-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/micro-benchmarks/turtle/guides-r1/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/micro-benchmarks/turtle/parse_turtle
    python3 eval.py external Seed_Programs/micro-benchmarks/turtle/parse_turtle Seed_Programs/micro-benchmarks/turtle/test_set results/gpt_grammar_${1}

elif [[ $1 == microbench-while-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  microbench-while-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/micro-benchmarks/while/guides-r1/ $1
    python3 grammar_from_csv.py $1 "Seed_Programs/micro-benchmarks/while/parse_while"
    python3 eval.py external "Seed_Programs/micro-benchmarks/while/parse_while" Seed_Programs/micro-benchmarks/while/test_set results/gpt_grammar_${1}

elif [[ $1 == microbench-xml-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  microbench-xml-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/micro-benchmarks/xml/guides-r1/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/micro-benchmarks/xml/parse_xml
    python3 eval.py external Seed_Programs/micro-benchmarks/xml/parse_xml Seed_Programs/micro-benchmarks/xml/test_set results/gpt_grammar_${1}

elif [[ $1 == microbench-c-500-r1-* ]]; then # will run later #for i in {1..50}; do bash runAll_for_gpt.sh  microbench-c-500-r1-$i; done |& tee log
    python3 gpt.py Seed_Programs/tinyc/tinyc-train-r5/ $1
    python3 grammar_from_csv.py $1 Seed_Programs/tinyc/parse_tinyc
    python3 eval.py external Seed_Programs/tinyc/parse_tinyc Seed_Programs/tinyc/tinyc-test results/gpt_grammar_${1}
fi
