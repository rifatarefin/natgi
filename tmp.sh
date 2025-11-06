#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "json"; done >  logs_treevada_false_llm_true/json.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "lisp"; done >  logs_treevada_false_llm_true/lisp.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "while"; done >  logs_treevada_false_llm_true/while.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "xml"; done >  logs_treevada_false_llm_true/xml.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "turtle"; done >  logs_treevada_false_llm_true/turtle.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "c-500"; done >  logs_treevada_false_llm_true/c-500.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "curl"; done >  logs_treevada_false_llm_true/curl.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "tinyc"; done >  logs_treevada_false_llm_true/tinyc.log
#for i in {1..5}; do timeout 12h bash command_to_run_treevada.sh "minic"; done >  logs_treevada_false_llm_true/minic.log
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "json" >  logs_org_treevada_false_hdd_true_llm_true_july_12/json_$i.log; done
for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "lisp" >  logs_org_treevada_false_hdd_true_llm_true_july_12/lisp_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "while" >  logs_org_treevada_false_hdd_true_llm_true_july_12/while_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "xml" >  logs_org_treevada_false_hdd_true_llm_true_july_12/xml_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "turtle" >  logs_org_treevada_false_hdd_true_llm_true_july_12/turtle_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "c-500" >  logs_org_treevada_false_hdd_true_llm_true_july_12/c-500_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "curl" >  logs_org_treevada_false_hdd_true_llm_true_july_12/curl_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "tinyc" >  logs_org_treevada_false_hdd_true_llm_true_july_12/tinyc_$i.log; done
for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "minic" >  logs_org_treevada_false_hdd_true_llm_true_july_12/minic_$i.log; done

#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "mysql" > logs_org_treevada_true_hdd_true_llm_true_july_9/shanto_log_mysql_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "c"  > logs_org_treevada_true_hdd_true_llm_true_july_9/shanto_log_c_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "tiny"  > logs_org_treevada_true_hdd_true_llm_true_july_9/shanto_log_tiny_$i.log; done
#for i in {1..10}; do timeout 24h bash command_to_run_org_treevada.sh "lua" > logs_org_treevada_true_hdd_true_llm_true_july_9/shanto_log_luai_$i.log; done

## STANDARD TREEVADA
#timeout 24h bash command_to_run_treevada.sh "json" >  logs_treevada_true_llm_false/json.log
#timeout 24h bash command_to_run_treevada.sh "lisp" >  logs_treevada_true_llm_false/lisp.log
#timeout 24h bash command_to_run_treevada.sh "while" >  logs_treevada_true_llm_false/while.log
#timeout 24h bash command_to_run_treevada.sh "xml" >  logs_treevada_true_llm_false/xml.log
#timeout 24h bash command_to_run_treevada.sh "turtle" >  logs_treevada_true_llm_false/turtle.log
#timeout 24h bash command_to_run_treevada.sh "c-500" >  logs_treevada_true_llm_false/c-500.log
#timeout 24h bash command_to_run_treevada.sh "curl" >  logs_treevada_true_llm_false/curl.log
#timeout 24h bash command_to_run_treevada.sh "tinyc" >  logs_treevada_true_llm_false/tinyc.log
#bash command_to_run_treevada.sh "minic" >  logs_treevada_true_llm_false/minic.log

#timeout 24h bash command_to_run_treevada.sh "mysql" > logs_treevada_true_llm_false/shanto_log_mysql.log
#timeout 24h bash command_to_run_treevada.sh "c"  > logs_treevada_true_llm_false/shanto_log_c.log
#timeout 24h bash command_to_run_treevada.sh "tiny"  > logs_treevada_true_llm_false/shanto_log_tiny.log
#timeout 24h bash command_to_run_treevada.sh "lua" > logs_treevada_true_llm_false/shanto_log_lua.log


## STANDARD TREEVADA without Delta-Debugging
#timeout 24h bash command_to_run_treevada.sh "json" >  logs_treevada_true_llm_false_hdd_false/json.log
#timeout 24h bash command_to_run_treevada.sh "lisp" >  logs_treevada_true_llm_false_hdd_false/lisp.log
#timeout 24h bash command_to_run_treevada.sh "while" >  logs_treevada_true_llm_false_hdd_false/while.log
#timeout 24h bash command_to_run_treevada.sh "xml" >  logs_treevada_true_llm_false_hdd_false/xml.log
#timeout 24h bash command_to_run_treevada.sh "turtle" >  logs_treevada_true_llm_false_hdd_false/turtle.log
#timeout 24h bash command_to_run_treevada.sh "c-500" >  logs_treevada_true_llm_false_hdd_false/c-500.log
#timeout 24h bash command_to_run_treevada.sh "curl" >  logs_treevada_true_llm_false_hdd_false/curl.log
#timeout 24h bash command_to_run_treevada.sh "tinyc" >  logs_treevada_true_llm_false_hdd_false/tinyc.log
##bash command_to_run_treevada.sh "minic" >  logs_treevada_true_llm_false_hdd_false/minic.log
#
#timeout 24h bash command_to_run_treevada.sh "mysql" > logs_treevada_true_llm_false_hdd_false/shanto_log_mysql.log
#timeout 24h bash command_to_run_treevada.sh "c"  > logs_treevada_true_llm_false_hdd_false/shanto_log_c.log
#timeout 24h bash command_to_run_treevada.sh "tiny"  > logs_treevada_true_llm_false_hdd_false/shanto_log_tiny.log
#timeout 24h bash command_to_run_treevada.sh "lua" > logs_treevada_true_llm_false_hdd_false/shanto_log_lua.log

#bash parse_result.sh "logs_treevada_false_llm_true/json.log"
#bash parse_result.sh "logs_treevada_false_llm_true/lisp.log"
#bash parse_result.sh "logs_treevada_false_llm_true/turtle.log"
#bash parse_result.sh "logs_treevada_false_llm_true/while.log"
#bash parse_result.sh "logs_treevada_false_llm_true/xml.log"
#bash parse_result.sh "logs_treevada_false_llm_true/curl.log"
#bash parse_result.sh "logs_treevada_false_llm_true/tinyc.log"
#bash parse_result.sh "logs_treevada_false_llm_true/c-500.log"
#
##For glade
#bash parse_result.sh "logs_treevada_false_llm_true/log_mysql.log"
#bash parse_result.sh "logs_treevada_false_llm_true/shanto_log_c.log"
#bash parse_result.sh "logs_treevada_false_llm_true/shanto_log_tiny.log"
#bash parse_result.sh "logs_treevada_false_llm_true/shanto_log_lua.log"
