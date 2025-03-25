import csv
from grammar import Grammar, Rule
from start import START
import pickle
from typing import Dict, List
import re
import sys

def format_nt(tag: str) -> str:
    pattern = re.compile(r'<([^>]+)>')
    return pattern.sub(r'\1', tag)

def read_grammar_from_csv(file_path):
    grammar_dict: Dict[str, List[str]] = {}
    
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                non_terminal, productions = row[0].split('::=')
                non_terminal = format_nt(non_terminal.strip())
                production_rules = [format_nt(prod.strip().replace('""','')) for prod in productions.split('|')]
                grammar_dict[non_terminal] = production_rules
    
    return grammar_dict

if __name__ == '__main__':

    file_path = '/home/mxa7262xx/Downloads/treevada-gpt/results/grammar_output_for_' + sys.argv[1] + '.txt'     #argv[1] = while-r1
    grammar_dict = read_grammar_from_csv(file_path)
    
    gpt_grammar = Grammar(START)
    for key, value in grammar_dict.items():
        for alts in value:
            rule = Rule(key)
            rule.add_body([alts])
            gpt_grammar.add_rule(rule)

    pickle.dump(gpt_grammar.rules, open("results/gpt_grammar_" + sys.argv[1] + ".gramdict", "wb"))
    for _, value in gpt_grammar.rules.items():
        print(str(value))