# cognateLanguage

> "[Entuni yawizkertcahot djidjansabrefzna yuyazlenbhaclog tonkogartmiy?](https://drive.google.com/open?id=0B239lCkYOdXfdDJRVlpsb3BFTE0)" 

(Click to hear this pronounced by Google Translate!)

_______
# Table of Contents:
1) [Purpose](#purpose)

2) [Source Languages](#source-languages)

3) [How was the Vocabulary Generated?](#how-was-the-vocabulary-generated)

4) [How Do I Pronounce the Words?](#how-do-i-pronounce-the-words)

5) [What Do the Files Do?](#5-what-do-the-files-do)

6) [How Can I Use the Files?](#how-can-i-use-the-files)
_______

1) ##Purpose

To create a list of words or vocabulary with maximum "intelligibility" via "(false) cognacy" with words from several of the most-commonly-spoken languages.  Each word could then serve as a single mnemonic for the words coming from the different source languages, and possibly help with learning those languages simultaneously by using one "centralized" vocab list.  In other words, it serves as a fun attempt at maximizing ROI for receptive lexicon (a multilingual one).  This project takes inspiration from zonal conlangs (applied more "globally"), auxlangs, Lojban, and Proto-Indo-European reconstruction, but applied to mnemonics for multiple modern languages by creating words in a way sort of like portmanteaus or like folk etymology, in order to increase the effects of partial intelligibility or cognacy.  Basically, I created this project as a tool for my personal language learning interests.  Plus I thought it'd be fun to make a program that automatically creates for me a vocabulary for a made up language!

2) ##Source Languages

Currently the source languages are:  Mandarin Chinese, Spanish, Hindi, Egyptian Arabic, and Russian.  This was based mainly on personal choice and the fact that these languages are apparently the most commonly understood languages/dialects on the planet.  Notably, English is excluded since it is assumed you already understand it if you are using this code, and your purpose is to learn other languages.  Although including English in the mix to create each word could theoretically aid in mnemonic creation by having the English word "visually embedded", the problem is it could also introduce extra complications in the word or make the word longer.
I'll start with using words from the Swadesh lists for the sources languages.  I know there are more "updated" versions of the Swadesh list (such as the Leipzig–Jakarta list), but the Swadesh list seems to be easier to find for each language.

3) ##How was the Vocabulary Generated?

Basically, each word is created by combining words from the source languages, while trying to minimize output word length.  This is done with detecting "overlaps" between words with matching letters.  Matching letters are ideally identical or are at least "allophones" (similar sounds).  To simplify pattern-matching, one basic dictionary of "allophones" is used, as well as "abjad-like" spellings of words (retaining only consonants and initial vowel).  I currently use the initial syllables of words to help limit word length.
Each word can be evaluated for optimizing word length against rough measures of "intelligibility" or "(false) cognacy", with languages weighted according to their ranks for estimated number of speakers, and with word length also having a say in order to encourage conciseness.  
Sometimes I see repeating patterns and can think of shorter ways to combine the source words.  You can test your own "manually-created" words by entering them into `output.txt`, along with the words from all the source languages, and then you can see the output score to see if it does better than the automatically-generated word using the same source words.  Follow the format of ordering the languages when you enter the words:  "**yournewword**,English,Chinese,Spanish,Hindi,Arabic,Russian,".

4) ##How Do I Pronounce the Words?

The spellings of the words (for all the languages) in the data/output files use approximate phonetic spellings, with all letters retaining their IPA values, except for these letters:
* **c** : (pronounced as /[ʃ](https://upload.wikimedia.org/wikipedia/commons/c/cc/Voiceless_palato-alveolar_sibilant.ogg)/ like the "sh" in "[shoe](https://upload.wikimedia.org/wikipedia/commons/4/44/En-us-shoe.ogg)"),
* **j** : (pronounced as /[ʒ](https://upload.wikimedia.org/wikipedia/commons/3/30/Voiced_palato-alveolar_sibilant.ogg)/ like the "s" in "[measure](https://upload.wikimedia.org/wikipedia/commons/3/35/En-us-measure.ogg)", or the "j" in the French word "[je](https://upload.wikimedia.org/wikipedia/commons/c/c4/Fr-je.ogg)"),
* **y** : (pronounced as /[j](https://upload.wikimedia.org/wikipedia/commons/e/e8/Palatal_approximant.ogg)/ like the "y" in the English word "[yes](https://upload.wikimedia.org/wikipedia/commons/b/b1/En-us-yes.ogg)"), and 
* **h** : (pronounced as /[h](https://upload.wikimedia.org/wikipedia/commons/d/da/Voiceless_glottal_fricative.ogg)/ or /[x](https://upload.wikimedia.org/wikipedia/commons/0/0f/Voiceless_velar_fricative.ogg)/, but so far /[x](https://upload.wikimedia.org/wikipedia/commons/0/0f/Voiceless_velar_fricative.ogg)/ seems easier to clearly pronounce when it's next to other consonants).

See https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants for the consonants (the vowels are in the following section) and click on the letters for links to other Wikipedia pages that have their sound files you can play to listen to (look for the triangle buttons), instead of reading their full technical descriptions.

##5) What Do the Files Do?

* The Python file `cognateLanguage_CreatingList.py` reads the input word list (`data.txt`) and creates the output word list (`output.txt`).
* The Python file `cognateLanguage_Evaluators.py` reads the output word list that was created by `cognateLanguage_CreatingList.py` and uses a few different evaluators to "score" each output word against the source language words.
* The Python file `cognateLanguage.py` is just the original one-word output test.
* The Python file `cognateLanguage_LessPrinting.py` is the same as `cognateLanguage.py`, except it only prints out the output word.
* The Python file `cognateLanguage_Translate.py` lets you use the command-line/terminal to translate English text.
* The Python file `levenshteinDistance.py` is a copy of code from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python from which I plan to import the function in other Python files.
* The Python file `levenshteinDistance.pyc` is the compiled that might be used to make the code compile faster.  (This file isn't really required to run the other files as it's automatically generated anyways.)
* The Python file `levenshteinDistance_Test.py` lets you do quick tests:  import the Levenshtein distance function, and test calculation inputs.

6) ##How Can I Use the Files?

I personally use Terminal (a.k.a. command-line) to run the .py files.  For example, to run the "cognateLanguage_Translate.py" file, I enter "pyt" and press tab for autocomplete, then I type the first letter "c" and tab for autocomplete (which gives me "cognateLanguage_") and then "T" and tab again (to get "cognateLanguage_Translate.py").  What this looks like in the commandline after I've done these keyboard presses is:  `python cognateLanguage_Translate.py`.

1. Add/Edit data in `data.txt`.

2. Run `cognateLanguage_CreatingList.py` (make sure `data.txt` is in the same folder).

3. You can edit `output.txt` to add in your "manual" attempts at word creation, so you can compare it with the automatically-generated words. 

4. Run `cognateLanguage_Evaluators.py` to check out the scoring of the words in `output.txt`.

5. Make mnemonics for the words (think of typical techniques used for words in Memrise courses, or Google different techniques used by language learners), but also practice using the words in fun contexts to make it easier to encode in memory.  Currently the generated words may have up to 5 syllables (since there are 5 source languages) if overlapping allophones are lacking in a word set.

> "[Yunsastempot dawkolena cweprentaltsik!](https://drive.google.com/open?id=0B239lCkYOdXfaVRydEl5NzZhVkk)"

(Click to hear this pronounced by Google Translate!)