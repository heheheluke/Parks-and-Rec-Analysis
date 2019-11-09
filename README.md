# Analysis of the characters of the television show "Parks and Recreation"

A personal project to analyze the main characters on Parks and Recreation, based on a variety of metrics: words spoken by each character per season, average number of words per episode, most "important" words for each character based on the TF-IDF weighting. (List subject to change). Transcription was done on Excel, analysis with Python using pandas and visualization using matplotlib.

The idea was inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/cy02do/analysis_of_lead_characters_dialogue_from_the_tv/) for the TV show "Community," which was itself apparently inspired by something similar for The Office.

The scripts are all pulled from [Springfield! Springfield!](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=parks-and-recreation). Unfortunately, as most of them do not have the characters attached to the lines, I went through and assigned every line the character that spoke it as I rewatched the show on Netflix. Some episode scripts from Springfield! are missing lines from extended versions of the episodes, so I have written them in myself. Some also have scenes that appear in different orders, so this final transcription is based on the order the scenes appear on Netflix.

**A few notes on the transcription of the show:**

- While there are formally 125 episodes, the transcription will only show 122 episodes; this is because a few episodes are actually split into part 1 and part 2, and are intended to be viewed as an hour-long episode (and appear on Netflix as one episode). Thus, the episode numbers may be slightly inconsistent with, for example, the Wikipedia list of Parks and Rec episodes. The combined episodes are: _London (S6E1)_, _Moving Up (S6E20)_, and _One Last Ride (S7E12)_. Thus, the "Season" and "Episode" fields for lines may not be consistent with the Wikipedia page for Parks and Rec.

- There are no accents or special characters, e.g. "creme brulee" or "Beyonce" (full disclosure, I didn't actually know Beyonce had an accent on the last e). This shouldn't be a problem, as foreign-borrowed words that utilize accents don't tend to overlap with English words when the special accents are removed.

- There are very few fully non-English lines (besides some ones like "Gracias"). Part of this is because I don't speak those languages, and part of it is because Netflix's subtitles just write "[speaks Spanish]" and not the actual words. This is mostly relevant for April,  who speaks some Spanish in a few episodes (most prominently in the Sister City episode and the short time that Eduardo the boyfriend is a thing).

- The lines may be inconsistently split up as separate entries, e.g. sometimes an entry will have just one sentence (or one word), and sometimes it'll have multiple lines. As an example, "Who's 'we'? What are you-- Oh, God." is one entry, but "What?" "Why?" may be split up into two entries. The character assigned to multiple-lines-as-a-single-entry is still correct (e.g. Ann did say all those lines consecutively in the former example), it just mostly just depended on how lazy I felt to separate the sentences when going though the transcript at the time. Just a warning for those possibly intending to use "number of lines" or "number of entries" as some sort of metric.

- There are some empty lines that may be assigned to the season and episode that follows before them. There are also lines separating episodes, where the "Character" field is empty and the "Line" is something like "Season: 3, Episode 04". These made it easier to transcribe by hand. These are easy to detect; just check that "Season: " and "Episode: " are in the line, as no other lines contain both.

- Sometimes the lesser-known characters (e.g. the random citizens of Pawnee you find at the town halls) are credited as "Extra" or "Extras," and sometimes as their real name. I've tried my best to identify them when they appear, but not all of their lines may be credited to them. I probably could go back and fix it, but it's not really hyper-important for what I'm using the transcription for. The more prominent recurring characters, like Perd Hapley, Joan Callamezzo, and the Saperstein siblings should all be credited correctly.

- The names of the characters are based on the [Parks and Recreation Wiki](https://parksandrecreation.fandom.com/wiki/Parks_and_Recreation), unless a spoken line that mentions the character directly contradicts it. Again, not super relevant, as it won't affect the main characters or even the more prominent recurring characters, it mostly applies to the people that appear for one episode.

- Garry Gergich's name is still "Jerry Gergich" in the transcript. My bad. I'll fix that eventually. Although I do find it appropriate for the character in the context of the show, so maybe I'll leave it. So for now, as an official justification: for a majority of the show, he is referred to as Jerry, so it made it easy to transcribe.

**A few notes on the analysis, visualization as they come to mind (and as a reminder to myself):**
- I defined the main characters, and thus the characters to be analyzed, as the following people: _Leslie Knope, Ann Perkins, Ron Swanson, Tom Haverford, Andy Dwyer, April Ludgate, Ben Wyatt, Chris Traeger, Jerry Gergich (woops), Donna Meagle._ There is a very reasonable case to be made for Mark Brendanawicz and Craig Middlebrooks, but they only appear for a relatively small portion of the show, even though they are acknowledged in the opening credits of the seasons they appear in. Interestingly enough, Brendanawicz is never mentioned again after Season 2, neither in retrospectives about Ann's and Leslie's relationships nor in the series finale showing the future outcomes of all the cast members (even Jean-Ralphio was in the series finale).

- I removed all punctuation, most notably and importantly hyphens. Hyphenated compound words will appear as a single word. This doesn't seem to have really affected the outcome of the analysis, but it may mildly alter certain TF-IDF values and term frequencies.

- I do realize that NLTK and scikit-learn have their own versions of TF-IDF already implemented; I just implemented my own because it seemed fun and relatively simple to do, as TF-IDF is not a particularly complicated heuristic to understand.

- Each "document" is defined as a single episode (so there are 122 possible "documents" in total). I only included a document in the computation of a character's IDF score if the character appeared in that episode (e.g. Andy was missing for the beginning of Season 6, ostensibly temporarily working in London). I don't know if this was totally right to do, so maybe someone more knowledgeable on NLP can correct me if it isn't.

- Stop words are pulled from NLTK's list of stop words, as well as some that I've added on my own (particularly contractions of stop words that are already listed, but their contraction isn't). They're listed at the top of tf_idf.py; a bit too many I feel to list in here.
