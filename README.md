# ["Cognate Language" Project](https://hchiam.github.io/cognateLanguage/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

A language with special mnemonic properties.

This project inspired these repos: [cognateLanguage2](https://github.com/hchiam/cognateLanguage2) and [cogLang-geneticAlgo](https://github.com/hchiam/cogLang-geneticAlgo) and [coglang-translator](https://github.com/hchiam/coglang-translator) and [text-similarity-test which uses TensorFlow.js Machine Learning](https://github.com/hchiam/text-similarity-test).

**Plain English Description**: The goal of this project's code is to generate a list of words that allow you to learn words from 5 languages at the same, by learning words from just 1 list instead of 5 separate lists. If you just want to get the gist of a sentence in any of those 5 languages, you could get there more efficiently with simple _recognition_ (of root words), not _production_ (of grammatically-correct words/sentences). Proper memory techniques should apply the same way as if you were learning any other language, and can compensate for any longer words (but there are also short forms for each word in this "cognate language").

**Technical Description**: Expand your [receptive vocabulary](https://en.wikipedia.org/wiki/Vocabulary#Productive_and_receptive) in multiple languages at the same time by using a vocab list generated to maximize multi-lingual "cognacy" while compressing/chunking memory usage; for example, use 1 mind palace journey instead of 5. This "cognate language" is like a functional conlang that just has vocabulary. Got questions? Go [here](#questions).

**Just want to test out some translations?** Go to [this website](https://codepen.io/hchiam/full/pojNLOj) to run the code in your browser: [https://codepen.io/hchiam/full/pojNLOj](https://codepen.io/hchiam/full/pojNLOj)

**Translation puzzle**: Yikwah harwe ardvos castah kidwoc? http://hchiam.blogspot.ca/2017/11/geeky-translation-puzzle.html

**Learning Prereq**: Effective mnemonics, i.e. memory aids (see the ones on Memrise for the kinds described under [http://www.memrise.com/science/](https://web.archive.org/web/20190104212307/https://www.memrise.com/science/)). I'm not talking about things like acrostics and first-letter memory aids. To get an idea of what visual/emotional/well-connected mnemonics are like, it might help to google ["Benny Lewis imagination"](https://www.fluentin3months.com/imagination-your-key-to-memorizing-hundreds-of-words-quickly/) and ["Ron White mind palace"](https://www.youtube.com/watch?v=3vlpQHJ09do). These are the kinds of memory techniques also described in Barbara Oakley's "A Mind for Numbers" and Cal Newport's "Deep Work". The [ROI](https://en.wiktionary.org/wiki/ROI) for the time spent on deeply rooting memories is worth the investment of long-term, effective storage (i.e. you don't have to forget and re-review things as much).

## Example 1:

"you" = _["entuni"](https://drive.google.com/open?id=0B239lCkYOdXfbHpwZjZfamNoelk)_, which is a single word that embeds these words:

- "ni" (Chinese),
- "tu" (Spanish),
- "tum" (Hindi - more conversationally),
- "enta" (Arabic), and
- "ti" (Russian - with simplified sounds).

**Memory compression**: 6 syllables total -> 3 syllables. 5 words -> 1 word.

**Mnemonic**: "You are _Anthony_". _"Entuni"_ sounds like "Anthony", but more like ["en-too-knee"](https://drive.google.com/open?id=0B239lCkYOdXfbHpwZjZfamNoelk). The mnemonic still helps because "Anthony" is a near homophone---it sounds similar enough to "entuni"---but also because you can connect this memory link to something you know very well already, in this case the first time you met someone named Anthony.

## Example 2: with longer source words

"queue" = _["paykatcirsafil"](https://drive.google.com/open?id=0B239lCkYOdXfaWVnTFdfek1iaVE)_ (sounds like "_pie catchers of Phil_", as if people are in line to watch some strange food circus), which corresponds to "paydwe", "fila", "katar", "saf", and "otcirit", in their respective languages, with the simplified [pronunciation](#4-how-do-i-pronounce-the-words) used by this project.

**Memory compression:** 10 syllables total -> 5 syllables. 5 words -> 1 word. (The vocab list generator only incorporates the first syllables from each source word because they're usually the most easily recognizable---think abbreviations. Different languages have different priorities/weights in terms of which overlapping letters are chosen, for highest ROI.)

## Example 3:

"heal" = "yidcankuritcaf" (sounds like "itchin', cure it chef!").

...

With the right preparation, the memorization process is faster to do than to explain. The visual imagination bit described in the various sources linked above also makes it more enjoyable to learn the words, all while also knowing you're packing multiple words into single words.

> ["Entuni yawizkertcahot djidjansabrefzna yuyazlenbhaclog tonkogartmiy?"](https://drive.google.com/open?id=0B239lCkYOdXfdDJRVlpsb3BFTE0)

^^^ (Click to hear this pronounced by Google Translate!) ^^^

---

# Questions?:

[1) Why?](#1-why)

[2) What are the Source Languages and Vocab?](#2-what-are-the-source-languages-and-vocab)

[3) How is the Vocabulary Generated?](#3-how-is-the-vocabulary-generated)

[4) How Do I Pronounce the Words?](#4-how-do-i-pronounce-the-words)

[5) What Do the Files Do?](#5-what-do-the-files-do)

[6) How Do I Remember Such Long Words?](#6-how-do-i-remember-such-long-words)

[7) How Can I Use the Files?](#7-how-can-i-use-the-files)

[8) Can I Contribute?](#8-can-i-contribute)

---

# 1) Why?

To create a list of words or vocabulary with maximum "intelligibility" via "(false) cognacy" with words from several of the most-commonly-spoken languages. Each word could then serve as a single mnemonic for the words coming from the different source languages, and possibly help with learning those languages simultaneously by using one "centralized" vocab list. In other words, it serves as a fun attempt at maximizing ROI for [receptive vocabulary](https://en.wikipedia.org/wiki/Vocabulary#Productive_and_receptive) (a multilingual one).

This personal project takes inspiration from zonal conlangs (applied more "globally"), auxlangs, Lojban, and Proto-Indo-European reconstruction, but applied to mnemonics for multiple modern languages by creating words in a way similar to portmanteaus or folk etymologies, in order to increase the effects of partial intelligibility or cognacy. In a way this makes it more of a worldlang than a zonal conlang, but with the original purpose of learning other languages, not as a "language" itself.

But basically, I created this project as a tool for my personal language learning interests. Plus I thought it'd be fun to make a program that automatically creates vocabulary for a made-up language!

    Djyenkonbanstroi!

# 2) What are the Source Languages and Vocab?

Currently the source languages are: Mandarin Chinese, Spanish, Hindi, Egyptian Arabic, and Russian. This was based mainly on personal choice and the fact that these languages are apparently the most commonly understood languages/dialects on the planet. Notably, English is excluded since it is assumed you already understand it if you are using this code, and your purpose is to learn other languages. Although including English in the mix to create each word could theoretically aid in mnemonic creation by having the English word "visually embedded", the problem is it could also introduce extra complications in the word or make each word longer.

I started building the vocab by first using words from the Swadesh lists for each of the sources languages. I know there are more "updated" versions of the Swadesh list (such as the Leipzig–Jakarta list), but words in the corresponding Swadesh lists seem to be easier to find for each source language. After that, I expanded the list to include words I found useful for making simple sentences from basic words (like "want", "use", "able", "must", "or", "hi", ...), based on imaginary conversations with would-be speakers of such a language, or based on notes I would want to translate for fun. Other words could be used to paraphrase ideas to make the most of the limited vocabulary (like "person", "thing", "time", "place"). Some words I added were oddly missing in the Swadesh list. For example, "who", "what", "where", etc. were already there, but "why" was missing. I don't know why.

    Nanot djenkon tsapal!
    Nanodjyenkotsapal!

# 3) How is the Vocabulary Generated?

To help support the decisions made, here are some test results as of September 30th, 2018:

| Score:  | Using Certain Optimizations/Trade-offs:                                                                               |
| ------- | --------------------------------------------------------------------------------------------------------------------- |
| -381.5  | Whole words appended together (no optimizations used). Like learning 5 vocab lists the normal way.                    |
| 8466.3  | Appending initial syllables but ignoring obvious overlaps (so you get things like "mammadmammam").                    |
| 13805.7 | Using all of the automated optimizations/trade-offs discussed in this README.md (e.g.: "mamad" and "bwentchawtayhor") |
| 14845.9 | "Curating" the automatically-generated output with manually-improved words (e.g.: "bwentchawrtay").                   |

(Scores were calculated by first generating different outputs in output.txt and then evaluating the score each time with `py cognateLanguage_OverallEvaluator.py output.txt`. The scoring algorithm isn't perfect, but it does seem that I'm onto something.)

Basically, each word is created by combining words from the source languages, while trying to minimize output word length. This is done by detecting "overlaps" between words with matching letters or consonant patterns. The matching letters/consonants are ideally identical or are at least "allophones" (treated as similar sounds for our purposes). To simplify pattern-matching, one basic dictionary of "allophones" is used, as well as the use of "abjad-like" spellings of words (retaining only consonants and initial vowel). I focus on consonants because, from my own anecdotal observations, consonants seem to be preserved better than vowels during language evolution despite language changes/differences. I currently use the initial syllables of source words to help limit word length. The first syllable of a (root) word is also typically the minimum easily-recognizable part of words. For example, think of common short forms like co., freq., com., ca., approx., cert., etc. Abbreviations seem to tend to use the first syllable or so of their respective words.

The initial consonants of words also seem most stable across related languages. Example: "milk" in French, Italian, Spanish, and Portuguese are lait, latte, leche, and leite, respectively, and all start with "l" and then a vowel, and then followed by "t" literally or phonetically.

Each word can be evaluated for optimizing word length against rough measures of "intelligibility" or "(false) cognacy", with languages weighted according to their ranks for estimated number of speakers, and with word length also having a say in order to encourage shorter words.

Sometimes I see repeating patterns and can think of shorter ways to combine the source words than the program outputs. You can test your own "manually-created" words by entering them into `output_shortlist.txt`, along with the words from all the source languages, and then you can see the output score to see if it does better than the automatically-generated word using the same source words. Use the following format of ordering the languages when you enter the words: "**yournewword**,English,Chinese,Spanish,Hindi,Arabic,Russian,".

For example: (Don't forget that last comma!)

    bwentchawrtay,good,haw,bweno,atcha,tayeb,horoci,

You can try to ensure that the right words from each language are used by "manually" checking for higher-frequency words, meaning matches, using most common registers, and using only roots of words. However, an automated search can be done with my [multiWebScraper.py](https://github.com/hchiam/webScraper/blob/master/multiWebScraper.py) to save on time, but at the cost of not double-checking for appropriate translations of intended meaning(s).

# 4) How Do I Pronounce the Words?

The spellings of the words (for all the languages) in the data/output files use approximate phonetic spellings, with all letters retaining their [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) values, except for these letters:

- **c** : (pronounced as /[ʃ](https://upload.wikimedia.org/wikipedia/commons/c/cc/Voiceless_palato-alveolar_sibilant.ogg)/ like the "sh" in ["shoe"](https://upload.wikimedia.org/wikipedia/commons/4/44/En-us-shoe.ogg)),
- **j** : (pronounced as /[ʒ](https://upload.wikimedia.org/wikipedia/commons/3/30/Voiced_palato-alveolar_sibilant.ogg)/ like the "s" in ["measure"](https://upload.wikimedia.org/wikipedia/commons/3/35/En-us-measure.ogg), or the "j" in the French word ["je"](https://upload.wikimedia.org/wikipedia/commons/c/c4/Fr-je.ogg)),
- **y** : (pronounced as /[j](https://upload.wikimedia.org/wikipedia/commons/e/e8/Palatal_approximant.ogg)/ like the "y" in the English word ["yes"](https://upload.wikimedia.org/wikipedia/commons/b/b1/En-us-yes.ogg)), and
- **h** : (pronounced as /[h](https://upload.wikimedia.org/wikipedia/commons/d/da/Voiceless_glottal_fricative.ogg)/ or /[x](https://upload.wikimedia.org/wikipedia/commons/0/0f/Voiceless_velar_fricative.ogg)/, but so far /[x](https://upload.wikimedia.org/wikipedia/commons/0/0f/Voiceless_velar_fricative.ogg)/ seems easier for me to clearly pronounce when it's next to most other consonants).

This all means that the _rest_ of the letters in the English alphabet are represented by the same symbol as they appear in the IPA: "b" is /b/, "d" is /d/, "e" is /e/, etc. Even "q" is /q/! (But you can pronounce it as /k/ if you find it hard to do.) And depending on how your computer's font shows on your screen, "a" is /a/.

See [https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants) for the consonants (the vowels are in the section after it) and click on the letters for links to other Wikipedia pages that have their sound files you can play to listen to (look for the triangle buttons), instead of reading their full technical descriptions.

# 5) What Do the Files Do?

- `cognateLanguage_CreatingList.py` reads the input word list (`data.txt`) and creates the output word list (`output.txt`). I like to copy and paste a cleaner version of the output into `output_shortlist.txt`.
- `cognateLanguage_Evaluators.py` reads the output word list that is created by `cognateLanguage_CreatingList.py` and uses a few different evaluators to "score" each output word against the source language words.
- `cognateLanguage.py` is just the original one-word output test.
- `cognateLanguage_LessPrinting.py` is the same as `cognateLanguage.py`, except it only prints out the output word.
- `cognateLanguage_Translate.py` lets you use the command-line/terminal to translate English text. Updated version includes "short-form" translation.
- `levenshteinDistance.py` is a copy of code from [https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python](https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python) from which I plan to import the function in other Python files.
- `levenshteinDistance.pyc` is the compiled that might be used to make the code compile faster. (This file isn't really required to run the other files as it's automatically generated anyways.)
- `levenshteinDistance_Test.py` lets you do quick tests: import the Levenshtein distance function, and test calculation inputs.
- `cognateLanguage_AutoSentence.py` automatically creates sentences based on very simple word "types":
  - `a` = Action/verb,
  - `d` = Descriptor/adjective/adverb,
  - `t` = Thing/noun/pronoun,
  - `c` = Connector/preposition.
- `repeatTranslation.py` is the code behind [the trinket.io interface](https://trinket.io/python3/80ac3c35c6?outputOnly=true&runOption=run). It also lets you run translations just like `cognateLanguage_Translate.py` in Terminal/CommandLine. This .py file also accounts for different Python versions (e.g. 3.0 versus 2.7).
- `geneticAlgo.py` uses a genetic algorithm to generate words. See it [here](https://github.com/hchiam/cogLang-geneticAlgo).

# 6) How Do I Remember Such Long Words?

Make mnemonics that connect to things you already know well. The ones [here](http://www.memrise.com/course/1195771/coglang/) typically use (semi-)homophones of English words to create visual scenes, and some make use of the method of loci. See the next section for more ideas on making automatic sentence translations.

Despite the optimizations the code can make so far (plus manual optimizations), most words are still long---at least, longer than traditional rote memory techniques can handle. It might help to google ["Benny Lewis imagination"](https://www.fluentin3months.com/imagination-your-key-to-memorizing-hundreds-of-words-quickly/) and ["Ron White mind palace"](https://www.youtube.com/watch?v=3vlpQHJ09do).

Once you're familiar with the rationale and how the language works in theory, try out the Memrise course here: [https://www.memrise.com/course/1195771/coglang/](https://www.memrise.com/course/1195771/coglang/)

If you're already familiar with the full words, you can use the "short translations" output from `cognateLanguage_Translate.py` to build sentences with shorter versions of the words.

# 7) How Can I Use the Files?

I personally use Terminal (a.k.a. command-line) to run the .py files. For example, to run the "cognateLanguage*Translate.py" file, I enter "pyt" and press tab for autocomplete, then I type the first letter "c" and tab for autocomplete (which gives me "cognateLanguage*") and then "T" and tab again (to get "cognateLanguage_Translate.py"). What this looks like in the commandline after I've done these keyboard presses is: `python cognateLanguage_Translate.py`.

1. Add/Edit data in `data.txt`.

2. Run `cognateLanguage_CreatingList.py` (make sure `data.txt` is in the same folder).

3. You can edit `output_shortlist.txt` to add in your "manual" attempts at word creation, so you can compare it with the automatically-generated words. (Note: I've added a letter at the end of each entry to identify word types for `cognateLanguage_AutoSentence.py`.)

4. Run `cognateLanguage_Evaluators.py` to check out the scoring of the words in `output_shortlist.txt`.

5. Make mnemonics for the words or use [this course](http://www.memrise.com/course/1195771/coglang/) (think of typical techniques used for words in Memrise courses, or Google different techniques used by language learners), but also practice using the words in fun contexts to make it easier to encode in memory, like translating sentences with `cognateLanguage_Translate.py`, or like with auto-generated sentences with `cognateLanguage_AutoSentence.py` (please note the words are randomly chosen based on word class, so some sentences may sound quite weird--use with caution). Currently the generated words may have up to 5 syllables (since there are 5 source languages) if overlapping allophones are lacking in a word set. There may be an extra syllable at the beginning of the word to ease pronunciation if the relevant source word has an initial vowel.

# 8) Can I Contribute?

Yes!

Feel free to message me on the [conlang reddit](https://www.reddit.com/r/conlangs/comments/5uaihi/pet_project_cognate_language_to_help_with/).

Some ideas:

- (Done) ~~Create browser-runnable version of the `cognateLanguage_Translate.py` file, so no download is needed for demonstration or for other people to try out low-commitment. Then I can link to it in this README file.~~
- (Kinda done [here](https://github.com/hchiam/cogLang-geneticAlgo)) ~~Use ML: take source letter per language group + extra neurons for "logic" layers + knowledge of which letters to prioritize + knowledge of the letters (a-z minus x) in the network.~~
- Some way to automate the raw data compilation of source words but while still ensuring the right translations are being used. Also need to extract the IPA of each source word and map to the simplified pronunciation used in this project. Preferably also taking only the roots of source words. Maybe some kind of smart web scraper.

---

> ["Yunsastempot dawkolena cweprentaltsik!"](https://drive.google.com/open?id=0B239lCkYOdXfaVRydEl5NzZhVkk)

^^^ (Click to hear this pronounced by Google Translate!) ^^^
