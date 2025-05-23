#bash command_to_run_treevada.sh "json"
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
#bash parse_result.sh "shanto_log_tiny.log"
