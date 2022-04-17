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

# Use NLTK's cmudict corpus
entry_list = list(cmudict.entries())


def is_syllable(phoneme: str) -> bool:
    '''Tests whether the phoneme represents a syllable (i.e., contains a digit).'''
    return phoneme.strip(string.ascii_letters)  # e.g., 'R' becomes '' but 'AH0' becomes '0'


def nsyl(phonemes: list[str]) -> int:
    '''Counts the number of syllables represented by the phonemes.'''
    return len(list(filter(is_syllable, phonemes)))


def get_candidates(entry) -> list:
    '''Gets a list of words which are one character longer, but one syllable shorter, than entry. O(n).'''
    characters = entry[1]
    syllables = entry[3]
    return list(filter(
        lambda candidate: (candidate[1] == characters + 1) and (candidate[3] == syllables - 1),
        entry_list
    ))


def single_vowel_difference(a: str, b: str) -> bool:
    '''Tests whether removing 1 vowel from b results in a.'''
    for i in range(0, len(b)):
        if b[i] in VOWELS and a == b[:i] + b[i+1:]:
            return True


def main():
    for i in range(0, len(entry_list)):  # Count syllables for each entry. O(n).
        # Structure of entry is: (word, len(word), phonemes, nsyl(phonemes))
        entry_list[i] = (entry_list[i][0], len(entry_list[i][0]), entry_list[i][1], nsyl(entry_list[i][1]))
    for entry in alive_it(entry_list):  # Test each entry. O(n^2).
        for candidate in get_candidates(entry):
            if single_vowel_difference(entry, candidate):
                print(f'Found a solution: "{entry}" and "{candidate}"')


def profile_main():
    '''Profiles the program to identify performance bottlenecks.
    Will not provide feedback if interrupted, so a manual "breakpoint"
    should be temporarily added to the main process (the line under
    alive_it(entry_list) in main()) to end the run early.'''
    # Adapted from https://docs.python.org/3/library/profile.html#profile.Profile
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())


if __name__ == "__main__":
    main()