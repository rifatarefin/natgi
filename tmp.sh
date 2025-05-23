for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "json"; done >  logs_treevada_false_llm_true/json.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "lisp"; done >  logs_treevada_false_llm_true/lisp.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "while"; done >  logs_treevada_false_llm_true/while.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "xml"; done >  logs_treevada_false_llm_true/xml.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "turtle"; done >  logs_treevada_false_llm_true/turtle.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "c-500"; done >  logs_treevada_false_llm_true/c-500.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "curl"; done >  logs_treevada_false_llm_true/curl.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "tinyc"; done >  logs_treevada_false_llm_true/tinyc.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "minic"; done >  logs_treevada_false_llm_true/minic.log
#bash command_to_run_treevada.sh "lisp"
#bash command_to_run_treevada.sh "while"
#bash command_to_run_treevada.sh "xml"
#bash command_to_run_treevada.sh "turtle"
#bash command_to_run_treevada.sh "c-500"
#bash command_to_run_treevada.sh "curl"
#bash command_to_run_treevada.sh "tinyc"
#bash command_to_run_treevada.sh "minic"


#timeout 12h bash command_to_run_treevada.sh "mysql" > log_mysql.log
for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "c"; done > shanto_log_c.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "tiny"; done > shanto_log_tiny.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "lua"; done > shanto_log_lua.log

#bash parse_result.sh "logs_treevada_false_llm_true/shanto_log_tiny.log"
