# cognateLanguage

**Short description**:  Possibly a "language" to help you learn multiple languages at the same time (but only [receptive vocab](https://en.wikipedia.org/wiki/Vocabulary#Productive_and_receptive)). 

**Prereq**:  Effective mnemonics, i.e. memory aids (see the ones on Memrise for the kinds described under http://www.memrise.com/science/ ).  I'm not talking about things like acrostics and first-letter memory aids.  It might help to google "[Benny Lewis imagination](https://www.fluentin3months.com/imagination-your-key-to-memorizing-hundreds-of-words-quickly/)" and "[Ron White mind palace](https://www.youtube.com/watch?v=3vlpQHJ09do)".  These are the kinds of memory techniques also described in Barbara Oakley's "A Mind for Numbers" and Cal Newport's "Deep Work".

**Example 1**:  "you" = *"[entuni](https://drive.google.com/open?id=0B239lCkYOdXfbHpwZjZfamNoelk)"*, which is a single word that embeds these words: 
 * "ni" (Chinese), 
 * "tu" (Spanish), 
 * "tum" (Hindi - more conversationally), 
 * "enta" (Arabic), and 
 * "ti" (Russian - with simplified sounds).

**Mnemonic**:  "You are *Anthony*".  *"Entuni"* sounds like "Anthony", but more like "[en-too-knee](https://drive.google.com/open?id=0B239lCkYOdXfbHpwZjZfamNoelk)".  The mnemonic still helps because "Anthony" is a near homophone---it sounds similar enough to "entuni"---but also because you can connect this memory link to something you know very well already, in this case the first time you met someone named Anthony.

**Example 2, with longer source words**: "east" = *"[purcarvasdon](https://drive.google.com/open?id=0B239lCkYOdXfdjZETnpVVDVKazQ)"*, which compresses these 5 words and serves to aid recognition of words by their beginning sounds: 
 * "don" (Chinese - with simplified sounds), 
 * "este" (Spanish), 
 * "purva" (Hindi), 
 * "carq" (Arabic - using the phonetic spelling of this project), and 
 * "vastok" (Russian - phonetically spelled).

(Only the first few letters of a source word are used because they're usually the most easily recognizable.  Different languages have different priorities/weights in terms of which letters are chosen, for highest ROI.)

**Mnemonic, shortened**:  Sounds like "[Porsche rivers down](https://drive.google.com/open?id=0B239lCkYOdXfdjZETnpVVDVKazQ)".  (This one's a near homophone too.)

**...Or more concretely**:  Imagine Eurus the robber driving a *Porsche* (east-ward), crashing through a few *rivers* before finally sinking *down*---I guess it was a bad decision to drive *east* that day.  *"Porsche rivers down"*.

With the right preparation, the memorization process is faster to do than to explain.  The visual imagination bit described in the various sources above also makes it more enjoyable to learn the words, all while also knowing you're packaging multiple words into single words.

> "[Entuni yawizkertcahot djidjansabrefzna yuyazlenbhaclog tonkogartmiy?](https://drive.google.com/open?id=0B239lCkYOdXfdDJRVlpsb3BFTE0)"

^^^ (Click to hear this pronounced by Google Translate!) ^^^

_______
# Questions?:

[1) Why?](#1-why)

[2) What are the Source Languages and Vocab?](#2-what-are-the-source-languages-and-vocab)

[3) How is the Vocabulary Generated?](#3-how-is-the-vocabulary-generated)

[4) How Do I Pronounce the Words?](#4-how-do-i-pronounce-the-words)

[5) What Do the Files Do?](#5-what-do-the-files-do)

[6) How Do I Remember Such Long Words?](#6-how-do-i-remember-such-long-words)

[7) How Can I Use the Files?](#7-how-can-i-use-the-files)

[8) Can I Contribute?](#8-can-i-contribute)
_______

##1) Why?

To create a list of words or vocabulary with maximum "intelligibility" via "(false) cognacy" with words from several of the most-commonly-spoken languages.  Each word could then serve as a single mnemonic for the words coming from the different source languages, and possibly help with learning those languages simultaneously by using one "centralized" vocab list.  In other words, it serves as a fun attempt at maximizing ROI for [receptive vocabulary](https://en.wikipedia.org/wiki/Vocabulary#Productive_and_receptive) (a multilingual one).  

This personal project takes inspiration from zonal conlangs (applied more "globally"), auxlangs, Lojban, and Proto-Indo-European reconstruction, but applied to mnemonics for multiple modern languages by creating words in a way similar to portmanteaus or folk etymologies, in order to increase the effects of partial intelligibility or cognacy.  In a way this makes it more of a worldlang than a zonal conlang, but with the original purpose of learning other languages, not as a "language" itself.

Basically, I created this project as a tool for my personal language learning interests.  Plus I thought it'd be fun to make a program that automatically creates vocabulary for a made-up language!

    Djyenkonbanstroi!

##2) What are the Source Languages and Vocab?

Currently the source languages are:  Mandarin Chinese, Spanish, Hindi, Egyptian Arabic, and Russian.  This was based mainly on personal choice and the fact that these languages are apparently the most commonly understood languages/dialects on the planet.  Notably, English is excluded since it is assumed you already understand it if you are using this code, and your purpose is to learn other languages.  Although including English in the mix to create each word could theoretically aid in mnemonic creation by having the English word "visually embedded", the problem is it could also introduce extra complications in the word or make each word longer.

I started building the vocab by first using words from the Swadesh lists for each of the sources languages.  I know there are more "updated" versions of the Swadesh list (such as the Leipzig–Jakarta list), but words in the corresponding Swadesh lists seem to be easier to find for each source language.  After that, I expanded the list to include words I found useful for making simple sentences for basic sentences (like "want", "use", "able", "must", "or", "hi", ...), based on imaginary conversations with would-be speakers of such a language, or based on notes I would want to translate for fun.  Other words could be used to paraphrase ideas to make the most of the limited vocabulary (like "person", "thing", "time", "place").  Some words I added were oddly missing in the Swadesh list.  For example, "who", "what", "where", etc. were already there, but "why" was missing.  I don't know why.

    Nanodjyenkotsapal!

##3) How is the Vocabulary Generated?

Basically, each word is created by combining words from the source languages, while trying to minimize output word length.  This is done by detecting "overlaps" between words with matching letters or consonant patterns.  The matching letters/consonants are ideally identical or are at least "allophones" (treated as similar sounds for our purposes).  To simplify pattern-matching, one basic dictionary of "allophones" is used, as well as the use of "abjad-like" spellings of words (retaining only consonants and initial vowel).  I focus on consonants because, from my own observations, consonants seem to be preserved better than vowels despite language changes/differences.  I currently use the initial syllables of source words to help limit word length.  The first syllable of a (root) word is also typically the minimum easily-recognizable part of words.  For example, think of common short forms like co., freq., com., ca., approx., cert., etc.  Abbreviations seem to tend to use the first syllable or so of their respective words.

Each word can be evaluated for optimizing word length against rough measures of "intelligibility" or "(false) cognacy", with languages weighted according to their ranks for estimated number of speakers, and with word length also having a say in order to encourage shorter words.  

Sometimes I see repeating patterns and can think of shorter ways to combine the source words than the program outputs.  You can test your own "manually-created" words by entering them into `output_shortlist.txt`, along with the words from all the source languages, and then you can see the output score to see if it does better than the automatically-generated word using the same source words.  Use the following format of ordering the languages when you enter the words:  "**yournewword**,English,Chinese,Spanish,Hindi,Arabic,Russian,".

For example:  (Don't forget that last comma!)
    
    bwentchawrtay,good,haw,bweno,atcha,tayeb,horoci,

You can try to ensure that the right words from each language are used by "manually" checking for higher-frequency words, meaning matches, using most common registers, and using only roots of words.  However, an automated search can be done with https://github.com/hchiam/webScraper/blob/master/multiWebScraper.py to save on time, but at the cost of not double-checking for appropriate translations of intended meaning(s).

##4) How Do I Pronounce the Words?

The spellings of the words (for all the languages) in the data/output files use approximate phonetic spellings, with all letters retaining their [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) values, except for these letters:
* **c** : (pronounced as /[ʃ](https://upload.wikimedia.org/wikipedia/commons/c/cc/Voiceless_palato-alveolar_sibilant.ogg)/ like the "sh" in "[shoe](https://upload.wikimedia.org/wikipedia/commons/4/44/En-us-shoe.ogg)"),
* **j** : (pronounced as /[ʒ](https://upload.wikimedia.org/wikipedia/commons/3/30/Voiced_palato-alveolar_sibilant.ogg)/ like the "s" in "[measure](https://upload.wikimedia.org/wikipedia/commons/3/35/En-us-measure.ogg)", or the "j" in the French word "[je](https://upload.wikimedia.org/wikipedia/commons/c/c4/Fr-je.ogg)"),
* **y** : (pronounced as /[j](https://upload.wikimedia.org/wikipedia/commons/e/e8/Palatal_approximant.ogg)/ like the "y" in the English word "[yes](https://upload.wikimedia.org/wikipedia/commons/b/b1/En-us-yes.ogg)"), and 
* **h** : (pronounced as /[h](https://upload.wikimedia.org/wikipedia/commons/d/da/Voiceless_glottal_fricative.ogg)/ or /[x](https://upload.wikimedia.org/wikipedia/commons/0/0f/Voiceless_velar_fricative.ogg)/, but so far /[x](https://upload.wikimedia.org/wikipedia/commons/0/0f/Voiceless_velar_fricative.ogg)/ seems easier for me to clearly pronounce when it's next to most other consonants).

This all means that the *rest* of the letters in the English alphabet are represented by the same symbol as they appear in the IPA: "b" is /b/, "d" is /d/, "e" is /e/, etc.  Even "q" is /q/!  (But you can pronounce it as /k/ if you find it hard to do.)  And depending on how your computer's font shows on your screen, "a" is /a/.

See https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants for the consonants (the vowels are in the section after it) and click on the letters for links to other Wikipedia pages that have their sound files you can play to listen to (look for the triangle buttons), instead of reading their full technical descriptions.

##5) What Do the Files Do?

* `cognateLanguage_CreatingList.py` reads the input word list (`data.txt`) and creates the output word list (`output.txt`).  I like to copy and paste a cleaner version of the output into `output_shortlist.txt`.
* `cognateLanguage_Evaluators.py` reads the output word list that is created by `cognateLanguage_CreatingList.py` and uses a few different evaluators to "score" each output word against the source language words.
* `cognateLanguage.py` is just the original one-word output test.
* `cognateLanguage_LessPrinting.py` is the same as `cognateLanguage.py`, except it only prints out the output word.
* `cognateLanguage_Translate.py` lets you use the command-line/terminal to translate English text. Updated version includes "short-form" translation.
* `levenshteinDistance.py` is a copy of code from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python from which I plan to import the function in other Python files.
* `levenshteinDistance.pyc` is the compiled that might be used to make the code compile faster.  (This file isn't really required to run the other files as it's automatically generated anyways.)
* `levenshteinDistance_Test.py` lets you do quick tests:  import the Levenshtein distance function, and test calculation inputs.
* `cognateLanguage_AutoSentence.py` automatically creates sentences based on very simple word "types": 
 * `a` = Action/verb,
 * `d` = Descriptor/adjective/adverb,
 * `t` = Thing/noun/pronoun,
 * `c` = Connector/preposition.

##6) How Do I Remember Such Long Words?

Make mnemonics that connect to things you already know well.  The ones [here](http://www.memrise.com/course/1195771/coglang/) typically use (semi-)homophones of English words to create visual scenes, and some make use of the method of loci.  See the next section for more ideas on making automatic sentence translations.

Despite the optimizations the code can make so far (plus manual optimizations), most words are still long---at least, longer than traditional rote memory techniques can handle.  It might help to google "[Benny Lewis imagination](https://www.fluentin3months.com/imagination-your-key-to-memorizing-hundreds-of-words-quickly/)" and "[Ron White mind palace](https://www.youtube.com/watch?v=3vlpQHJ09do)".

If you're already familiar with the full words, you can use the "short translations" output from `cognateLanguage_Translate.py` to build sentences with shorter versions of the words.

##7) How Can I Use the Files?

I personally use Terminal (a.k.a. command-line) to run the .py files.  For example, to run the "cognateLanguage_Translate.py" file, I enter "pyt" and press tab for autocomplete, then I type the first letter "c" and tab for autocomplete (which gives me "cognateLanguage_") and then "T" and tab again (to get "cognateLanguage_Translate.py").  What this looks like in the commandline after I've done these keyboard presses is:  `python cognateLanguage_Translate.py`.

1. Add/Edit data in `data.txt`.

2. Run `cognateLanguage_CreatingList.py` (make sure `data.txt` is in the same folder).

3. You can edit `output_shortlist.txt` to add in your "manual" attempts at word creation, so you can compare it with the automatically-generated words. (Note:  I've added a letter at the end of each entry to identify word types for `cognateLanguage_AutoSentence.py`.) 

4. Run `cognateLanguage_Evaluators.py` to check out the scoring of the words in `output_shortlist.txt`.

5. Make mnemonics for the words or use [this course](http://www.memrise.com/course/1195771/coglang/) (think of typical techniques used for words in Memrise courses, or Google different techniques used by language learners), but also practice using the words in fun contexts to make it easier to encode in memory, like translating sentences with `cognateLanguage_Translate.py`, or like with auto-generated sentences with `cognateLanguage_AutoSentence.py` (please note the words are randomly chosen based on word class, so some sentences may sound quite weird--use with caution).  Currently the generated words may have up to 5 syllables (since there are 5 source languages) if overlapping allophones are lacking in a word set.  There may be an extra syllable at the beginning of the word to ease pronunciation if the relevant source word has an initial vowel.

##8) Can I Contribute?

Yes!

Feel free to message me.  https://www.reddit.com/r/conlangs/comments/5uaihi/pet_project_cognate_language_to_help_with/

-------

> "[Yunsastempot dawkolena cweprentaltsik!](https://drive.google.com/open?id=0B239lCkYOdXfaVRydEl5NzZhVkk)"

^^^ (Click to hear this pronounced by Google Translate!) ^^^