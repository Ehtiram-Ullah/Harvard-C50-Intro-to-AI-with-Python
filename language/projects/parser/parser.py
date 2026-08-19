import nltk
import sys
import re
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP

NP -> N | Det N | AP N | Det AP N | NP PP
VP -> V | V NP | VP PP | V PP | VP Adv | Adv VP | V NP PP | VP Conj VP

AP -> Adj | Adj AP
PP -> P NP | P N
"""
# S -> N V Det N

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        with open('sentences/4.txt') as f:
                s = f.read()
        # s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
 
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # print(sentence)
    tokens = nltk.word_tokenize(sentence)
    clean_tokens = [word.lower() for word in tokens if re.search("[a-zA-Z]", word)]
    return clean_tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            nested_np = any(
                child.label() == "NP"
                for child in subtree.subtrees()
                if child != subtree
            )
            if not nested_np:
                chunks.append(subtree)
    return chunks


if __name__ == "__main__":
    main()
