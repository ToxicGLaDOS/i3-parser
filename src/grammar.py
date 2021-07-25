import parsimonious.grammar

def build_grammar():
    with open('grammar/grammar.pars', 'r') as i3_grammar:
        grammar = parsimonious.grammar.Grammar(i3_grammar.read())
        return grammar


if __name__ == "__main__":
    build_grammar()