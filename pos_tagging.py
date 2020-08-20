# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    nns = []
    nn = []
    plurals = []
    
    with open("sentences.txt", "r") as f:
        for line in f:
            for words in line.split():
                if words.split('|')[1] == 'NN' and words.split('|')[0] not in nn:
                    nn += [(words.split('|')[0])]
                elif words.split('|')[1] == 'NNS' and words.split('|')[0] not in nns:
                    nns += [(words.split('|')[0])]

    for word in nns:
        if word in nn:
            plurals += [(word)]
    return plurals
            

unchanging_plurals_list = unchanging_plurals()
#print (unchanging_plurals_list)
def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here
    if s in unchanging_plurals_list:
        return s
    elif re.match('.*men', s):
        s = s[:-3] + "man"
    elif re.match('.*([^aeiousxyz(ch)(sh)])s', s):
        s = s[:-1]
    elif re.match('.*[aeiou]ys', s):
        s = s[:-1]
    elif re.match('..*[^aeiou]ies', s):
        s = s[:-3] + 'y'
    elif re.match('[^aeiou]ies', s):
        s = s[:-1]
    elif re.match('.*(o|x|ch|sh|ss|zz)es', s):
        s = s[:-2]
    elif re.match('.*(([^s]se)|([^z]ze))s', s):
        s = s[:-1]
    elif re.match('.*([^iosxz(^ch)(^sh)])es', s):
        s = s[:-1]
    else:
        s = ""
    return s



def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    pos = []

    pos += [t for t in ['P', 'A'] if wd in lx.getAll(t)]

    if (wd in lx.getAll('N')) or (noun_stem(wd) in lx.getAll('N')):
        if wd in unchanging_plurals_list:
            pos += ["Np", "Ns"]
        elif noun_stem(wd) == '':
            pos += ["Ns"]
        else:
            pos += ["Np"]

    pos += [(t + "p" if verb_stem(wd) == '' else t + "s") for t in ['I', 'T'] if ((wd in lx.getAll(t)) or (verb_stem(wd) in lx.getAll(t)))]
    

    if wd in function_words:

        pos += [t[1] for t in function_words_tags if t[0] == wd]
    
    
    return pos
        

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]
'''
lx = Lexicon()
lx.add("John", "P")
lx.add("Mary", "P")
lx.add("orange", "N")
lx.add("orange", "A")
lx.add("fish", "N")
lx.add("fish", "I")
lx.add("fish", "T")

print(tag_word(lx,"John"))
print(tag_word(lx,"orange"))
print(tag_word(lx,"fish"))
print(tag_word(lx,"a"))
print(tag_word(lx,"zxghqw"))
print(tag_word(lx,"which"))
print(tag_word(lx,"and"))
print(tag_word(lx,"who"))
print(tag_word(lx,"?"))
'''
# End of PART B.
