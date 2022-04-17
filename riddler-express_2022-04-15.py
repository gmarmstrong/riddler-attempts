import string

from nltk.downloader import Downloader
from nltk.corpus import cmudict

from alive_progress import alive_it

# Riddler Express for April 15, 2022. Article by Zach Wissner-Gross.
# 
# As you may recall, around this time last year, I ran two puzzles by high
# school students who were winners of the Regeneron Science Talent Search. This
# year, I am delighted to have puzzles from two of this year’s winners as well.
# 
# Luke Robitaille is from Euless, Texas. As part of his research project, he
# proved that most simple braids — topological structures composed on
# intertwining strands — are orderly for low numbers of strands. But as the
# number of strands increases, nearly all simple braids become chaotic. Luke
# also represented the United States three times in the International Math
# Olympiad, taking home three gold medals.
# 
# Now, I can’t recall ever running a straight-up word puzzle in my days as the
# editor of The Riddler. But Luke’s puzzle was too good to pass up, so here
# goes:
# 
# Find a word in the English language to which you can add a vowel, resulting in
# another word that has fewer syllables.
# 
# By “add a vowel,” I mean insert one additional letter — a vowel — somewhere in
# the word (or at the beginning or end), while keeping the ordering of all the
# other letters the same. For example, you could add a vowel to the word “TASTY”
# to get the word “TOASTY.” However, both words are two syllables, meaning this
# is not the solution.
#
# SOURCE: https://fivethirtyeight.com/features/can-you-add-a-vowel-to-lose-a-syllable/

VOWELS      = ['a', 'e', 'i', 'o', 'u']
VOWELS_Y    = ['a', 'e', 'i', 'o', 'u', 'y']
VOWELS_YW   = ['a', 'e', 'i', 'o', 'u', 'y', 'w']

# Install NLTK's cmudict corpus
downloader = Downloader()
if downloader.status('cmudict', downloader._get_download_dir()) != downloader.INSTALLED:
    downloader.download('cmudict')

# Use NLTK's cmudict corpus, sorted by word length.
entry_list = list(cmudict.entries())
entry_list.sort(key=lambda entry: len(entry[0]), reverse=True)


def is_syllable(phoneme: str) -> bool:
    '''Tests whether the phoneme represents a syllable (i.e., contains a digit).'''
    return phoneme.strip(string.ascii_letters)  # e.g., 'R' becomes '' but 'AH0' becomes '0'


def nsyl(phonemes: list[str]) -> int:
    '''Counts the number of syllables represented by the phonemes.'''
    return len(list(filter(is_syllable, phonemes)))


def print_syllable_counts(entries) -> None:
    '''Prints each entry and its syllable count.'''
    for entry in entries:
        print(f'{entry[0]} has {nsyl(entry[1])} syllables(s).')


def get_candidates(entry) -> list:
    '''Gets a list of words which are one character longer, but one syllable shorter, than entry.'''
    characters = len(entry[0])
    syllables = nsyl(entry[1])
    return list(filter(
        lambda candidate: (len(candidate[0]) == characters + 1) and (nsyl(candidate[1]) == syllables - 1),
        entry_list
    ))


def single_vowel_difference(a: str, b: str) -> bool:
    '''Tests whether inserting a vowel into a results in b.'''
    for i in range(0, len(b)):
        character: str = b[i]
        if character in VOWELS:
            if a == b[:i] + b[i+1:]:
                return True


if __name__ == "__main__":
    for entry in alive_it(entry_list):
        for candidate in get_candidates(entry):
            if single_vowel_difference(entry, candidate):
                print(entry)
                print(candidate)