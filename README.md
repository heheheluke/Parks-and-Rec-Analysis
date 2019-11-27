# Analysis of the characters of the television show "Parks and Recreation"

A personal project to analyze the main characters on Parks and Recreation, based on a variety of metrics: words spoken by each character per season, average number of words per episode, most "important" words for each character based on the TF-IDF weighting. (List subject to change). Transcription was done on Excel, analysis with Python using pandas and visualization using matplotlib.

The idea was inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/cy02do/analysis_of_lead_characters_dialogue_from_the_tv/) for the TV show "Community," which was itself apparently inspired by something similar for The Office.

The scripts are all pulled from [Springfield! Springfield!](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=parks-and-recreation). Unfortunately, as most of them do not have the characters attached to the lines, I went through and assigned every line the character that spoke it as I rewatched the show on Netflix. Some episode scripts from Springfield! are missing lines from extended versions of the episodes, so I have written them in myself. Some also have scenes that appear in different orders, so this final transcription is based on the order the scenes appear on Netflix.

**A few notes on the analysis, visualization as they come to mind (and as a reminder to myself):**
- The main characters, and thus the characters to be analyzed, are defined as the following people: _Leslie Knope, Ann Perkins, Ron Swanson, Tom Haverford, Andy Dwyer, April Ludgate, Ben Wyatt, Chris Traeger, Jerry Gergich (woops), Donna Meagle._ There is a very reasonable case to be made for Mark Brendanawicz and Craig Middlebrooks, but they only appear for a relatively small portion of the show, even though they are acknowledged in the opening credits of the seasons they appear in. Interestingly enough, Brendanawicz is never mentioned again after Season 2, neither in retrospectives about Ann's and Leslie's relationships nor in the series finale showing the future outcomes of all the cast members (even Jean-Ralphio was in the series finale).

- All punctuation is removed, most notably and importantly hyphens. Hyphenated compound words will appear as a single word. This doesn't seem to have really affected the outcome of the analysis, but it may mildly alter certain TF-IDF values and term frequencies (the ones that immediately come to mind are "we'll" and "i'll").

- I do realize that NLTK and scikit-learn have their own versions of TF-IDF already implemented; I just implemented my own because it seemed fun and relatively simple to do, as TF-IDF is not a particularly complicated heuristic to understand.

- Each "document" is defined as a single episode (so there are 122 possible "documents" in total). I only included a document in the computation of a character's IDF score if the character appeared in that episode (e.g. Andy was missing for the beginning of Season 6, ostensibly temporarily working in London). I don't know if this was totally right to do, so maybe someone more knowledgeable on NLP can correct me if it isn't.

- Stop words are pulled from NLTK's list of stop words, as well as some that I've added on my own (particularly contractions of stop words that are already listed, but their contraction isn't). They're listed at the top of tf_idf.py; a bit too many to list in here.
