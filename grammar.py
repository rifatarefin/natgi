import copy
import re

from lark import Lark
import random

random.seed(0)

def elem_fixup(elem: str, is_antlr4=False) -> str:
    """
    >>> elem_fixup('"-""')
    '"-\""'
    >>> elem_fixup('"="="')
    '"=\"="'
    """
    if len(elem) >= 3 and elem.startswith('"') and elem.endswith('"'):# and '"' not in elem[1:-1]:
        for i in reversed(range(1, len(elem) - 1)):
            term_char = elem[i]
            if term_char == '"' and not is_antlr4:
                elem = elem[:i] + '\\"' + elem[i + 1:]
            elif term_char == "'" and is_antlr4:
                elem = elem[:i] + "\\'" + elem[i + 1:]
            elif term_char == '\\':
                elem = elem[:i] + '\\\\' + elem[i + 1:]
            elif term_char == '\n':
                elem = elem[:i] + '\\n' + elem[i + 1:]
    if elem == ' ':
        return 'ws'
    if is_antlr4 and len(elem) >=3 and elem.startswith('"') and elem.endswith('"'):
        return '\'' + elem[1:-1] + '\''
    return elem

class Grammar():
    """
    Object representing a string-representation of a context-free grammar.
    This class is intended to be used with the Lark module.
    """
    def __init__(self, start):
        """
        Requires that terminals be wrapped in double quotes.
        Rules is a mapping of rule start name to Rule object.
        """
        # Add the first rule pointing a dummy start nonterminal to start
        start_rule = Rule('start')
        start_rule.add_body([start])
        self.start_symbol = start
        self.rules = {'start':start_rule}

        # Define cacheable values and their valid bits
        self.cached_str = ""
        self.cached_parser = None
        self.str_cache_hash = self._rule_hash()
        self.parser_cache_hash = self._rule_hash()

    def copy(self):
        new_grammar = Grammar(self.start_symbol)
        for rule in self.rules.values():
            new_rule = rule.copy()
            new_grammar.add_rule(new_rule)
        return new_grammar

    def _rule_hash(self):
        return hash(tuple([(start, rule._body_hash()) for start, rule in self.rules.items()]))

    def str_cache_valid(self):
        return self.str_cache_hash == self._rule_hash()

    def parser_cache_valid(self):
        return self.parser_cache_hash == self._rule_hash()
    
    def merge(self, other_grammar):
        """
        Merges the rules of another grammar into this one.
        """
        for start, rule in other_grammar.rules.items():
            if start in self.rules:
                saved_rule = self.rules[start]
                for body in rule.bodies:
                    saved_rule.add_body(body)
            else:
                self.rules[start] = rule

    def add_rule(self, rule, depth=None):
        if rule.start in self.rules:
            saved_rule = self.rules[rule.start]
            for rule_body in rule.bodies:
                saved_rule.add_body(rule_body)
        else:
            self.rules[rule.start] = rule

        if depth is not None:
            self.rules[rule.start].depth = max(depth, rule.depth)

        self.cache_hash = self._rule_hash()

    def parser(self):
        if self.parser_cache_valid():
            return self.cached_parser

        self.cached_parser = Lark(str(self).replace('\u03B5', ''))
        self.parser_cache_hash = self._rule_hash()
        return self.cached_parser

    def sample_negatives(self, n, terminals, max_size):
        """
        Samples n random strings that do not belong to the grammar.
        Returns the unique subset of these.
        """
        samples = set()
        attempts = 0
        while len(samples) < n and attempts < 10*n:
            samples.add(self.generate_negative_example(terminals, max_size))
            attempts += 1
        return samples

    def generate_negative_example(self, terminals, max_size):
        # Generate the negative example by choosing randomly from the set of terminals
        negative_example = ""
        n_chars = random.randint(1, max_size)
        for _ in range(n_chars):
            rindex = random.randint(0, len(terminals) - 1)
            term = terminals[rindex]
            assert(term[0]== '"' and term[-1] == '"')
            term = term[1:-1]
            negative_example += term

        # Check if the negative example is in the grammar. Try again if so.
        try:
            self.parser().parse(negative_example)
            return self.generate_negative_example(terminals, max_size)
        except:
            return negative_example

    def sample_positives(self, n, max_depth):
        """
        Samples n random strings that belong to the grammar.
        Returns the unique subset of these.
        """
        samples = set()
        attempts = 0
        while len(samples) < n and attempts < 100*n:
            attempts += 1
            try:
                sample = self.generate_positive_example(max_depth)
                # we blindly consider strings of all lengths
                # if len(sample) > 300:
                #     continue
                samples.add(sample)
            except RecursionError:
                continue
        return samples

    def body_nonterminals(self, grammar, body):
        """Helper function: gets all the nonterminals for a body"""
        nonterminals = []
        for item in body:
            if item in grammar.rules:
                nonterminals.append(item)
        return nonterminals
    
    def generate_positive_example(self, max_depth, start_nonterminal='start', cur_depth=0):
        """
        Samples a random positive example from the grammar, with max_depth as much as possible.
        """
        
        bodies = self.rules[start_nonterminal].bodies
        # If we've reached the max depth, try to choose a non-recursive rule.
        if cur_depth >= max_depth:
            terminal_bodies = [body for body in bodies if len(self.body_nonterminals(self, body)) == 0]
            if len(terminal_bodies) > 0:
                terminal_body = terminal_bodies[random.randint(0, len(terminal_bodies)-1)]
                return "".join([elem.replace('"', '') for elem in terminal_body])
            # Otherwise... guess we'll have to try to stop later.
        body_to_expand = bodies[random.randint(0, len(bodies) -1)]
        nonterminals_to_expand = self.body_nonterminals(self, body_to_expand)
        expanded_body = [self.generate_positive_example(max_depth, elem, cur_depth + 1)
                                if elem in nonterminals_to_expand
                                else elem[1:-1]   # really just wanna non-clean up the terminals
                                for elem in body_to_expand]
        return "".join(expanded_body)

    
    def sample_trees(self, n, max_depth):
        """Generate at least n random parse trees. Also try to
        observe every nonterminal (when possible). 
        """
        attempts = 0
        trees = []
        seen = set()
        all_nonterms = set(self.rules.keys())
        max_attempts = 10*n

        while (len(trees) < n or seen != all_nonterms) and attempts < max_attempts:
            attempts += 1
            try:
                tree = self.generate_positive_trees(max_depth, self.start_symbol, 0, seen)
                tree.update_cache_info()
                trees.append(tree)
            except RecursionError:
                continue

        return trees
    
    
    def generate_positive_trees(self, max_depth, start_nonterminal='start', cur_depth=0, seen=None):
        """
        Samples a dummy parse tree from the grammar.
        Uses the 'seen' set to prefer expanding bodies that introduce unseen nonterminals.
        """
        from parse_tree import ParseNode

        if seen is None:
            seen = set()
        seen.add(start_nonterminal)
        bodies = self.rules[start_nonterminal].bodies
        terminal_bodies = [body for body in bodies if len(self.body_nonterminals(self, body)) == 0]
        # If we've reached the max depth, try to choose a non-recursive rule.
        if cur_depth >= max_depth and len(terminal_bodies) > 0:
            terminal_body = terminal_bodies[random.randint(0, len(terminal_bodies)-1)]
            terminal_token = "".join([elem for elem in terminal_body])
            return ParseNode(start_nonterminal, False, [ParseNode(terminal_token, True, [])])

        # Prefer bodies that contain at least one unseen nonterminal
        def body_has_unseen_nonterm(body):
            for elem in body:
                if elem in self.rules and elem not in seen:
                    return True
            return False

        unseen_bodies = [b for b in bodies if body_has_unseen_nonterm(b)]
        if unseen_bodies and cur_depth < 10:
            body_to_expand = unseen_bodies[random.randint(0, len(unseen_bodies) - 1)]
        else:
            body_to_expand = bodies[random.randint(0, len(bodies) - 1)]

        nonterminals_to_expand = self.body_nonterminals(self, body_to_expand)
        children = [
            self.generate_positive_trees(max_depth, elem, cur_depth + 1, seen) if elem in nonterminals_to_expand
            else ParseNode(elem, True, [])
            for elem in body_to_expand
        ]
        return ParseNode(start_nonterminal, False, children)
    
    def __str__(self):
        if self.str_cache_valid():
            return self.cached_str

        self.cached_str = '\n'.join([str(rule) for rule in self.rules.values()])
        self.cached_str += '\n %import common.WS\n %ignore WS'
        self.str_cache_hash = self._rule_hash()
        return self.cached_str
    
    def remove_indirect_left_recursion(self):
        """
        Removes indirect left recursion from the grammar. We first remove indirect left recursions.
        ANTLR4 accepts direct left recursions but not indirect ones. If any direct left recursion
        causes infinite loop, we remove them as well.
        """
        def is_rule_left_recursive(rule):
            for body in rule.bodies:
                if len(body) > 0 and body[0] == rule.start:
                    return True
            return False

        def remove_left_recursion_from_rule(rule):
            direct_left_recursive_bodies = []
            non_left_recursive_bodies = []
            for body in rule.bodies:
                if len(body) > 0 and body[0] == rule.start:
                    direct_left_recursive_bodies.append(body[1:])
                else:
                    non_left_recursive_bodies.append(body)
            if len(direct_left_recursive_bodies) == 0:
                return rule  # No direct left recursion to remove
            """ A → A α1 | . . . | A αn | β1 | . . . | βm 
            becomes
                A → A_head | A_head A_tails
                A_head → β1 | . . . | βm
                A_tails → A_tail | A_tail A_tails
                A_tail → α1 | . . . | αn
            """
            # beta = Rule(rule.start + "_beta")
            # alpha = Rule(rule.start + "_alpha")
            # alphas = Rule(rule.start + "_alphas")
            # beta.bodies = non_left_recursive_bodies
            # alpha.bodies = direct_left_recursive_bodies
            # alphas.bodies = [[alpha.start], [alpha.start, alphas.start]]
            # rule.bodies = [[beta.start], [beta.start, alphas.start]]
            # return rule, beta, alphas, alpha

            """
            A → A α1 | . . . | A αn | β1 | . . . | βm
            becomes
                A → β1 A' | . . . | βm A'
                A' → α1 A' | . . . | αn A' | ε
            """
            new_start = rule.start + "_"
            new_rule = Rule(new_start)
            for body in direct_left_recursive_bodies:
                new_rule.add_body(body + [new_start])
            new_rule.add_body([''])  # epsilon production

            rule.bodies = []
            for body in non_left_recursive_bodies:
                rule.add_body(body + [new_start])

            return rule, new_rule

        def find_indirect_left_recursion(grammar):
            indirect_left_recursive = set()
            for rule in grammar.rules.values():
                for body in rule.bodies:
                    if len(body) > 0 and body[0] in grammar.rules and body[0] != rule.start:
                        # Check if body[0] can eventually lead back to rule.start
                        to_visit = [body[0]]
                        visited = set()
                        while to_visit:
                            current = to_visit.pop()
                            if current == rule.start:
                                indirect_left_recursive.add((rule.start, body[0]))
                                break
                            if current not in visited:
                                visited.add(current)
                                for b in grammar.rules[current].bodies:
                                    if len(b) > 0 and b[0] in grammar.rules:
                                        to_visit.append(b[0])
            return indirect_left_recursive

        def one_step_pass_indirect(grammar):
            new_grammar = Grammar(grammar.start_symbol)
            old_rules = list(grammar.rules.keys())
            for i in range(len(old_rules)):
                # Work on a copy of the original rule to avoid mutating the input grammar
                ri = grammar.rules[old_rules[i]].copy()
                for j in range(i):
                    rj = new_grammar.rules[old_rules[j]]
                    new_bodies = []
                    for body in ri.bodies:
                        # If the body starts with old_rules[j], replace it with rj's bodies
                        # replace ri: A -> B α with rj: B -> β  => add β α
                        if len(body) > 0 and body[0] == old_rules[j]:
                            for body_j in rj.bodies:
                                new_body = body_j + body[1:]
                                new_bodies.append(new_body)
                            
                        else:
                            new_bodies.append(body)
                    ri.bodies = new_bodies
                if is_rule_left_recursive(ri):
                    new_rule, beta = remove_left_recursion_from_rule(ri)
                    new_grammar.add_rule(new_rule)
                    new_grammar.add_rule(beta)
                else:
                    new_grammar.add_rule(ri)
            return new_grammar
        
        current_grammar = self
        current_grammar = one_step_pass_indirect(current_grammar)
        # indirect_left_recursive = find_indirect_left_recursion(current_grammar)
        # while indirect_left_recursive:
            
        #     current_grammar = one_step_pass_indirect(current_grammar)
        #     # need to remove direct left recursion as well to prevent infinite loops
        #     rule_list = list({item for tpl in indirect_left_recursive for item in tpl})
        #     for rname in rule_list:
        #         if is_rule_left_recursive(current_grammar.rules[rname]):
        #             old_rule = current_grammar.rules[rname]
                    
        #             new_rule, beta, alphas, alpha = remove_left_recursion_from_rule(old_rule)
        #             current_grammar.rules[old_rule.start] = new_rule
        #             current_grammar.add_rule(beta)
        #             current_grammar.add_rule(alphas)
        #             current_grammar.add_rule(alpha)
        #     indirect_left_recursive = find_indirect_left_recursion(current_grammar)

                

        return current_grammar
    
    def to_antlr4(self, log_file_name):
        print("ANTLR4 GRAMMAR:")
        antlr4_rules = self.remove_indirect_left_recursion()
        rules = '\n'.join([rule.antlr4() for rule in antlr4_rules.rules.values()])
        return f"grammar {log_file_name};\n{rules}"
    
        

    def pretty_print(self):

        ret = '\n'.join([rule.pretty_print() for rule in self.rules.values()])

        return ret


    def size(self):
        return sum([rule.size() for rule in self.rules.values()])

class Rule():
    """
    Object representing the string-represenation of a rule of a CFG.
    There is always an associated grammar with every rule.
    This class is intended to be used with the Lark module.
    """
    def __init__(self, start):
        """
        Start must be a nonterminal.
        Each body is a sequence of terminals and nonterminals.
        If there are multiple bodies, they will be connected via the | op.
        The epsilon terminal is represented under the hood as an empty string,
        but is displayed to the user as the epsilon character.
        """
        self.start = start
        self.bodies = []
        self.cached_str = ""
        self.cache_hash = 0
        self.depth = -1

    def copy(self):
        new_rule = Rule(self.start)
        for body in self.bodies:
            new_rule.add_body(body[:])
        new_rule.depth = self.depth
        return new_rule

    def add_body(self, body):
        self.cache_valid = False
        if body not in self.bodies:
            self.bodies.append(body)
        return self

    def _cache_valid(self):
        return self.cache_hash == self._body_hash()

    def _body_hash(self):
        return hash(tuple([tuple(body) for body in self.bodies]))
    
    def antlr4(self):
        rule_str = '%s: %s' % ("ws" if self.start == ' ' else self.start, self._body_str(self.bodies[0], is_antlr4=True))
        for i in range(1, len(self.bodies)):
            rule_str += '\n    | %s' % (self._body_str(self.bodies[i], is_antlr4=True))
        return rule_str + '\n;'

    def __str__(self):
        if self._cache_valid():
            return self.cached_str

        self.cached_str = '%s: %s' % ("ws" if self.start == ' ' else self.start, self._body_str(self.bodies[0]))
        for i in range(1, len(self.bodies)):
            self.cached_str += '\n    | %s' % (self._body_str(self.bodies[i]))

        self.cache_hash = self._body_hash()
        return self.cached_str

    def _body_str(self, body, is_antlr4=False):

        # return ' '.join([elem_fixup(b, is_antlr4) if len(b) > 0 else '\u03B5' for b in body])
        return ' '.join([elem_fixup(b, is_antlr4) for b in body])

    def size(self):
        return 1 + sum([len(body) for body in self.bodies])

    def pretty_print(self):

        ret = '%s: %s' % (self.start, self.pretty_body(self.bodies[0]))
        for i in range(1, len(self.bodies)):
            ret += '\n    | %s' % (self.pretty_body(self.bodies[i]))

        return ret

    def pretty_body(self, body):
        ret = ""
        built_up_terminals = ""
        is_first = True
        for child in body:
            if re.match("t[0-9]+", child):
                if not is_first:
                    ret += " "
                if len(built_up_terminals) > 0:
                    ret += '"' +built_up_terminals + '"'
                    built_up_terminals = ""
                    ret += " "
                ret += child
            elif child == '':
                if not is_first:
                    ret += " "
                ret += '\u03B5'
            else:
                built_up_terminals += child.strip('"')
            is_first = False

        if len(built_up_terminals) > 0:
            if len(ret) > 0:
                ret += " "
            if len(built_up_terminals) > 0:
                ret += '"' + built_up_terminals + '"'

        return ret



# Example grammar with nonterminals n1, n2 and terminals a, b
# grammar = Grammar('n1')
# grammar.add_rule(Rule('n1').add_body(['n2', '"a"']).add_body(['']))
# grammar.add_rule(Rule('n2').add_body(['', 'n1', '']))
# parser = grammar.parser()
# print(parser.parse("aa").pretty())


"""
start: stmt EOF;
stmt : 'L' SPACE '=' SPACE numexpr
  | 'if' SPACE boolexpr SPACE 'then' SPACE stmt SPACE 'else' SPACE stmt
  | stmt SPACE ';' SPACE stmt
  | 'while' SPACE boolexpr SPACE 'do' SPACE stmt
  | 'skip';
boolexpr : 'true' | 'false' | numexpr SPACE '==' SPACE numexpr | boolexpr SPACE '&' SPACE boolexpr | '~' boolexpr;
numexpr : 'L' | 'n' | '(' numexpr '+' numexpr ')';
SPACE: ' ';
"""

def while_grammar():
    grammar = Grammar('stmt')
    grammar.add_rule(Rule('stmt').add_body(['"L"', '"="', '"n"']))
    grammar.add_rule(Rule('stmt').add_body(['"if"', '"true"', '"then"', 'stmt', '"else"', 'stmt']))
    grammar.add_rule(Rule('stmt').add_body(['stmt', 'stmt']))
    grammar.add_rule(Rule('stmt').add_body(['"while"', '"true"', '"do"', 'stmt']))
    grammar.add_rule(Rule('stmt').add_body(['"skip"']))

    grammar.add_rule(Rule('boolexpr').add_body(['"true"']))
    grammar.add_rule(Rule('boolexpr').add_body(['"false"']))
    grammar.add_rule(Rule('boolexpr').add_body(['"n"']))
    grammar.add_rule(Rule('boolexpr').add_body(['"("', 'boolexpr', '"=="', 'boolexpr', '")"']))
    grammar.add_rule(Rule('boolexpr').add_body(['boolexpr', '"&"', 'boolexpr']))
    grammar.add_rule(Rule('boolexpr').add_body(['"~"', 'boolexpr']))

    grammar.add_rule(Rule('numexpr').add_body(['"L"']))
    grammar.add_rule(Rule('numexpr').add_body(['"n"']))
    grammar.add_rule(Rule('numexpr').add_body(['"("', 'numexpr', '"+', 'numexpr', '")"']))

    grammar.add_rule(Rule('SPACE').add_body(['" "']))

    return grammar