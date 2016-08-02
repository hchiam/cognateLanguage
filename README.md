# cognateLanguage
##Purpose:
To create a list of words or vocabulary with maximum "intelligibility" via "(false) cognacy" with words from several languages.  Each word could then serve as a single mnemonic for the words coming from the different source languages, and possibly help with learning those languages by using one "centralized" vocab list.
##Source Languages:
Currently the source languages are:  Mandarin Chinese, Egyptian Arabic, Spanish, Hindi, and Russian.  This was based mainly on personal choice and the fact that these languages are apparently the most commonly understood languages/dialects on the planet.  Notably, English is excluded since it is assumed you already understand it if you are using this code, and your purpose is to learn other languages.  Although including English in the mix to create each word could theoretically aid in mnemonic creation by having the English word "visually embedded", the problem is it could also introduce extra complications in the word or make the word longer.
##Method:
Basically, each word is created by combining words from the source languages, while trying to minimize output word length.  This is done with detecting "overlaps" between words with matching letters.  Matching letters are ideally identical or are at least "allophones" (similar sounds).  To simplify pattern-matching, one basic dictionary of "allophones" is used, as well as "abjad"-like spellings of words (retaining only consonants and initial vowel).  
Each word can be evaluated for optimizing word length against rough measures of "intelligibility" or "(false) cognacy", with languages weighted according to their ranks for estimated number of speakers, and with word length having the highest weighting of them all to encourage conciseness.  
You can test your own "manually-created" words by entering them into ```output.txt```, along with the words from all the source languages, and then you can see the output score to see if it does better than the automatically-generated word.
##File Descriptions:
* The Python file ```cognateLanguage_CreatingList.py``` reads the input word list (```data.txt```) and creates the output word list (```output.txt```).
* The Python file ```cognateLanguage_Evaluators.py``` reads the output word list that was created by ```cognateLanguage_CreatingList.py``` and uses a few different evaluators to "score" each output word against the source language words.
* The Python file ```cognateLanguage.py``` is just the original one-word output test.
* The Python file ```cognateLanguage_LessPrinting.py``` is the same as ```cognateLanguage.py```, except it only prints out the output word.
