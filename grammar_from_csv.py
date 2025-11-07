import csv
from grammar import Grammar, Rule
from parse_tree import ParseNode
from token_expansion import expand_tokens
from oracle import ExternalOracle
from start import START, handle_special_nonterminals
import pickle
from typing import Dict, List
import re
import sys
import string
from next_tid import allocate_tid
import os

def format_nt(tag: str) -> str:
    """ remove surrounding <> tags
    ignore if within quotes
    e.g. <a> => a
    """
    pattern = re.compile(r'(?<!")<([^<>]+)>(?!")')
    def repl(m):
        # add spaces around the captured content
        return ' ' + m.group(1) + ' '

    out = pattern.sub(repl, tag)
    # collapse runs of whitespace to a single space and trim
    out = re.sub(r'\s+', ' ', out).strip()
    return out

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
                    # ignore '|' without double quotes
                    production_rules = [format_nt(remove_empty_quotes(prod.strip())) for prod in re.split(r'(?<!")\|(?!")', productions)]
                    grammar_dict[non_terminal] = production_rules
                else:
                    productions = row.split('|', 1)[1] if '|' in row else ''
                    alt_rule = [format_nt(remove_empty_quotes(prod.strip())) for prod in re.split(r'\|(?![^"]*")', productions)]
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
    # replace single quotes with double quotes
    result = [item.replace("'", '"') if item.startswith("'") and item.endswith("'") else item for item in pattern]
    return result

if __name__ == '__main__':

    current_dir = os.getcwd()
    #file_path = '/home/sr53282/grammar-inference/treevada-gpt/results/gpt_grammar_' + sys.argv[1] + '.txt'     #argv[1] = while-r1

    file_path = current_dir+'/results/gpt_grammar_' + sys.argv[1] + '.txt'     #argv[1] = while-r1
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

    # check for special characters in the nonterminal names, underscores are allowed
    for rule in list(gpt_grammar.rules.values()):
        if any(c in rule.start for c in string.punctuation.replace('_','')) or (rule.start and rule.start[0].isdigit()):
            handle_special_nonterminals(gpt_grammar, rule.start, allocate_tid())
        if any(c.isupper() for c in rule.start):
            handle_special_nonterminals(gpt_grammar, rule.start, rule.start.lower())

    pickle.dump(gpt_grammar.rules, open("results/gpt_grammar_" + sys.argv[1] + ".gramdict", "wb"))
    for _, value in gpt_grammar.rules.items():
        print(value)
    try:
        gpt_grammar.parser()
        print(f"Parse calls: {oracle.parse_calls}")
    
    except Exception as e:
        print('\n\nLoaded grammar does not compile! %s' % str(e))
  
