import argparse
import random, sys, os, time, string
from typing import Dict, List

from tqdm import tqdm

from parse_tree import ParseTree, ParseNode
from grammar import Grammar, Rule
from start import get_times, START
from lark import Lark
from oracle import CachingOracle, ExternalOracle
from token_expansion import expand_tokens
"""
High-level command line to launch Arvada evaluation.
 
See __main__ dispatch at the bottom for usage. 
"""
PRECISION_SIZE=1000
ANTLR4_OUTPUT=True

def main_internal(external_folder, log_file, random_guides=False):
    """
    `external_folder`: the base folder for the benchmark, which contains:
      - random-guides: dir of random guide examples
      - guides: dir of minimal guide examples
      - test_set: dir of held-out test examples
      - parse_bench_name: the parser command (oracle). assume bench_name is the
        base (i.e. without parent directories) name of external_folder
    `log_file`: where to write results
    `fast`: use internal caching oracle created with the Lark grammar, instead
            of the external command
    `random_guides`: learn from the guide examples in random-guides instead of guides
    """
    import os
    bench_name = os.path.basename(external_folder)
    test_folder = os.path.join(external_folder, "test_set")
    parser_command = os.path.join(external_folder, f"parse_{bench_name}")
    
    main(parser_command, log_file, test_folder)

def main(oracle_cmd, log_file_name, test_examples_folder ):
    oracle = ExternalOracle(oracle_cmd)


    real_recall_set = []
    for filename in os.listdir(test_examples_folder):
        full_filename = os.path.join(test_examples_folder, filename)
        test_raw = open(full_filename).read()
        if test_raw:
            real_recall_set.append(test_raw)
        # TODO: make an option to try


    # Create the log file and write positive and negative examples to it
    # Also write the initial starting grammar to the file
    with open(log_file_name + ".eval", 'w+') as f:
        start_time = time.time()
        import pickle
        learned_grammar = Grammar(START)
        grammar_dict : Dict[str, Rule] = pickle.load(open(log_file_name + ".gramdict", "rb"))
        for key, rule in grammar_dict.items():
            print(rule)
            learned_grammar.add_rule(rule)

        try:
            print("Loading grammar")
            learned_grammar.parser()
            print('\n\nInitial grammar loaded:\n%s' % str(learned_grammar), file=f)
            if ANTLR4_OUTPUT:
                dir_name = os.path.dirname(log_file_name)
                bench_name = os.path.basename(log_file_name)
                bench_name = ''.join(c for c in bench_name if c not in string.punctuation)
                antlr_file = os.path.join(dir_name, bench_name + ".g4")
                with open(antlr_file, 'w') as antlr_f:
                    antlr_f.write(learned_grammar.to_antlr4(bench_name)) # todo: remove indirect left recursion
                    antlr_f.close()
        except Exception as e:
            print('\n\nLoaded grammar does not compile! %s' % str(e), file=f)
            print(learned_grammar, file=f)
            print(e)
            exit()
        
        parser: Lark = learned_grammar.parser()
        precision_set = learned_grammar.sample_positives(PRECISION_SIZE, 5)

        num_precision_parsed = 0

        print(f"Precision set (size {len(precision_set)}):", file=f)
        print(f"Precision set (size {len(precision_set)}):")
        print("Eval of precision:")
        for example in tqdm(precision_set):
            try:
                oracle.parse(example, timeout=10)
                print("Passed\n", example, file=f)
                num_precision_parsed += 1
            except Exception as e:
                print("Failed", example, " <----- FAILURE", file=f)
                continue

        example_gen_time = time.time()
        num_recall_parsed = 0

        if real_recall_set is not None:
            print(f"Recall set (size {len(real_recall_set)}):", file=f)
            print(f"Recall set (size {len(real_recall_set)}):")
            print("Recall eval:")
            for example in tqdm(real_recall_set):
                try:
                    parser.parse(example)
                    print("   ", example, file=f)
                    num_recall_parsed += 1
                except Exception as e:
                    print("   ", example, " <----- FAILURE", file=f)
                    continue
            recall = num_recall_parsed / len(real_recall_set)
            precision = num_precision_parsed / len(precision_set)
            f1 = 2 * (recall * precision) / (recall + precision) if (recall + precision) > 0 else 0
            print(f'Recall: {recall}, Precision: {precision}, F-1: {f1}', file=f)
            print(f'Recall: {recall}, Precision: {precision}, F-1: {f1}')
        else:
            print(
                f'Recall: [no test set provided], Precision: {num_precision_parsed / len(precision_set)}',
                file=f)
            print(
                f'Recall: [no test set provided], Precision: {num_precision_parsed / len(precision_set)}')

        print(f'Example gen time: {example_gen_time - start_time}', file=f)
        print(f'Scoring time: {time.time() - example_gen_time}', file=f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('oracle_cmd', help='the oracle command; should be invocable on a filename via `oracle_cmd filename`, and return a non-zero exit code on invalid inputs', type=str)
    parser.add_argument('examples_dir', help='folder containing the test (recall) examples', type=str)
    parser.add_argument('log_file', help='log file output from search.py', type=str)
    parser.add_argument('--no-antlr4', help='also output an ANTLR4 grammar file', action='store_true', dest='no_antlr4')
    parser.add_argument('-n', '--precision_set_size', help='size of precision set to sample from learned grammar (default 1000)', type=int, default=1000)

    args = parser.parse_args()
    
    if args.precision_set_size is not None:
        PRECISION_SIZE = args.precision_set_size
    if args.no_antlr4:
        ANTLR4_OUTPUT = False
    main(args.oracle_cmd, args.log_file, args.examples_dir)
