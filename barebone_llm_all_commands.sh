#for i in {1..50}; do bash runAll_for_gpt.sh  tinyc-r1-$i; done |& tee log-tinyc
#for i in {1..50}; do bash runAll_for_gpt.sh  curl-r1-$i; done |& tee log-curl
#for i in {1..50}; do bash runAll_for_gpt.sh  microbench-json-r1-$i; done |& tee log-json
#for i in {1..50}; do bash runAll_for_gpt.sh  microbench-lisp-r1-$i; done |& tee log-lisp
#for i in {1..50}; do bash runAll_for_gpt.sh  microbench-turtle-r1-$i; done |& tee log-turtle
#for i in {1..50}; do bash runAll_for_gpt.sh  microbench-while-r1-$i; done |& tee log-while
#for i in {1..50}; do bash runAll_for_gpt.sh  microbench-xml-r1-$i; done |& tee log-xml
#for i in {1..50}; do bash runAll_for_gpt.sh  microbench-c-500-r1-$i; done |& tee log-microbench-c-500
#for i in {1..50}; do bash runAll_for_gpt.sh  minic-r1-$i; done |& tee log-minc
#
#
#for i in {1..50}; do bash runAll_for_gpt.sh  glade2-lua-$i; done |& tee log-glade2-lua
for i in {1..50}; do bash runAll_for_gpt.sh  glade2-mysql-$i; done |& tee log-glade2-mysql
for i in {1..50}; do bash runAll_for_gpt.sh  glade2-c-$i; done |& tee log-glade2-c
for i in {1..50}; do bash runAll_for_gpt.sh  glade2-tiny-$i; done |& tee log-glade2-tiny
