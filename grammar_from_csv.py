import csv
from grammar import Grammar, Rule
from parse_tree import ParseNode
from token_expansion import expand_tokens
from oracle import ExternalOracle
from start import START
import pickle
from typing import Dict, List
import re
import sys

def format_nt(tag: str) -> str:
    """ remove surrounding <> tags"""
    pattern = re.compile(r'<([^<>]+)>')
    return pattern.sub(r'\1', tag)

def remove_empty_quotes(s: str) -> str:
    """ remove empty double quotes except when escaped 
    ignore if preceding backslash or quote
    ignore if followed by quote
    e.g. don't remove \"" but remove ""
    """
    pattern = re.compile(r'(?<!\\)(?<!")""(?!")')
    return pattern.sub('', s)

def read_grammar_from_csv(file_path):
    grammar_dict: Dict[str, List[str]] = {}
    
    with open(file_path, mode='r') as file:
        
        for row in file:
            row = row.strip()
            if row:
                if "::=" in row:    
                    non_terminal, productions = row.split('::=')
                    non_terminal = format_nt(non_terminal.strip())
                    production_rules = [format_nt(remove_empty_quotes(prod.strip())) for prod in productions.split('|')]
                    grammar_dict[non_terminal] = production_rules
                else:
                    productions = ''.join([i for i in row.split('|')[1:]])
                    alt_rule = [format_nt(remove_empty_quotes(prod.strip())) for prod in productions.split('|')]
                    production_rules.extend(alt_rule)
                    grammar_dict[non_terminal] = production_rules
    return grammar_dict

def split_whitespace(s: str) -> List[str]:
    """
    split string by whitespace 
    ignore whitespace inside double quotes
    e.g. "a b" c d => ["a b", "c", "d"]
    Ignore escaped double quotes, triple quotes
    """
    pattern = re.findall(r'"(?:[^"\\]|\\.)*"+|\S+', s)
    return pattern

if __name__ == '__main__':

    file_path = '/home/mxa7262xx/Downloads/treevada-gpt/results/gpt_grammar_' + sys.argv[1] + '.txt'     #argv[1] = while-r1
    csv_dict = read_grammar_from_csv(file_path)
    oracle = ExternalOracle(sys.argv[2])    #argv[2] = lang/parse_lang
    gpt_grammar = Grammar(START)
    for key, value in csv_dict.items():
        rule = Rule(key)
        for alt in value:
            rule.add_body(split_whitespace(alt))
        gpt_grammar.add_rule(rule)

    # create few dummy trees for token expansion
    trees: List[ParseNode] = gpt_grammar.sample_trees(10, 5)
    gpt_grammar = expand_tokens(oracle, gpt_grammar, trees)

    pickle.dump(gpt_grammar.rules, open("results/gpt_grammar_" + sys.argv[1] + ".gramdict", "wb"))
    for _, value in gpt_grammar.rules.items():
        print(value)