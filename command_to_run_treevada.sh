#bash command_to_run_treevada.sh "json"
if [[ $1 == "" ]]; then
echo "Give the language name (e.g., json/lisp/turtle/while/xml/curl/tinyc/minic/c-500)"
fi
#$1="curl"

seed="r1"

#for bench in curl tinyc; do
if [[ $1 == "json" || $1 == "lisp" || $1 == "while"  || $1 == "xml" || $1 == "turtle"  ]]; then
    bench="micro-benchmarks/$1"

    echo "**** Running search.py ****"
    echo "python3 search.py external Seed_Programs/$bench/parse_$1 Seed_Programs/$bench/guides-r1 Seed_Programs/$1-$seed-tv.log"
    python3 search.py external Seed_Programs/$bench/parse_$1 Seed_Programs/$bench/guides-r1 Seed_Programs/$1-$seed-tv.log

    echo "**** Running eval.py ****"
    python3 eval.py external Seed_Programs/$bench/parse_$1 Seed_Programs/$bench/test_set Seed_Programs/$1-$seed-tv.log #json, lisp, while, xml, turtle

elif  [[ $1 == "c-500" ]]; then
    bench="tinyc"
    seed="r5"
    #$1="tinyc"
    echo "**** Running search.py ****"
    python3 search.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/tinyc-train-r5 Seed_Programs/$1-$seed-tv.log
    echo "**** Running eval.py ****"
    python3 eval.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/tinyc-test Seed_Programs/$1-$seed-tv.log

elif [[ $1 == "minic" ]]; then
    bench="$1"
    echo "python3 search.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/$bench-train-r0 Seed_Programs/$1-$seed-tv.log"
    python3 search.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/$bench-train-r0 Seed_Programs/$1-$seed-tv.log
    echo "**** Running eval.py ****"
    python3 eval.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/$bench-test Seed_Programs/$1-$seed-tv.log

elif [[ $1 == "curl" || $1 == "tinyc" ]]; then
    bench="$1"
    echo "python3 search.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/$bench-train-r1 Seed_Programs/$1-$seed-tv.log"
    python3 search.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/$bench-train-r1 Seed_Programs/$1-$seed-tv.log
    echo "**** Running eval.py ****"
    python3 eval.py external Seed_Programs/$bench/parse_$bench Seed_Programs/$bench/$bench-test Seed_Programs/$1-$seed-tv.log

elif [[ $1 == "lua" || $1 == "mysql" || $1 == "c" || $1 == "tiny" ]]; then 
    bench="$1"
    echo "python3 search.py external glade-2/$bench/parse_$bench glade-2/$bench/$bench-train glade-2/$1-$seed-tv.log"
    python3 search.py external glade-2/$bench/parse_$bench glade-2/$bench/$bench-train glade-2/$1-$seed-tv.log
    echo "**** Running eval.py ****"
    python3 eval.py external glade-2/$bench/parse_$bench glade-2/$bench/$bench-test glade-2/$1-$seed-tv.log
fi
echo "**** Running search.py ****"
