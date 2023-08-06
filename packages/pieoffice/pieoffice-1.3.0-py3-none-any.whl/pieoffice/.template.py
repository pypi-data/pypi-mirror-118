#! /usr/bin python3

""" <++> script converter

This scripts allows the user to convert between the latinized transliteration
of <++> and the <++> Script itself with (almost) simple rules.

The file can be imported as a module and contains the following functions:
    alpha_to_<++> - returns a converted string in <++> script from
    a romanized string.
    <++>_to_alpha - returns a converted string in romanized linear B from a
    string in <++> Script. (Might return problematic data due to double
    readings for the same grapheme in <++>)

It also contains a dictionary:
    script - contains the equivalences between romanized and <++> scripts.

Usage
-----


"""

from tools import get_key

script = {

        }

def alpha_to_<++>(input):
    """ Converts text in Latin Alphabet to <++> Script

    Each syllable should be separated by a sing dash, each word by a space.

    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in <++> Script

    Usage
    -----
    
    > alpha_to_<++>("<++>")
    + 

    """

    output = []
    input = input.split(" ")
    for word in input:
        word_out = ""
        if word.isnumeric():
            word = [int(i) for i in word]
            tens = [10**n for n in range(len(word)-1,-1,-1)]
            for i in range(len(tens)):
                word_out = word_out + script[str(word[i]*tens[i])]
        elif "-" in word:
            for syllabe in word.split("-"):
                word_out = word_out + script[syllabe]
        else:
            word_out = script[word]

        output.append(word_out)

    return " ".join(output)


def <++>_to_alpha(input):
    """ Converts text in <++> Script to Latin Alphabet

    Some errors might occur if a syllable has multiple values.

    Parameters
    ----------
    input : str
        Text input in <++> Script

    Returns
    -------
    output : str
        Transliterated text in Latin Alphabet

    Usage
    -----
    
    > <++>_to_alpha("<++>")

    """
    output = []
    input = input.split()
    for word in input:
        word_out = ""
        if len(word) > 1:
            syllabes = [sy for sy in word]
            for syllabe in syllabes:
                word_out = word_out + get_key(syllabe, script) + "-"
            word_out = str(word_out)
            if len(word_out) > 1 and word_out[-1] == "-":
                word_out = word_out[:-1]
        else:
            word_out = get_key(word, script)
        output.append(word_out)
        for i in range(len(output)):
            if output[i].split("-")[0].isnumeric():
                output[i] = str(sum([int(i) for i in output[i].split("-")]))

    return " ".join(output)

if __name__ == "__main__":
        
