#Methods for computing term frequencies, inverse document frequencies (idf) in order to create tf-idf matrix for
#the words spoken by characters on the tv show Parks and Recreation.

import csv
import sys
import re
import math
import string

#-----------------------------------------------------------------------------------------

#Stop words list pulled from NLTK (largely contractions, due to removing all punctuation, e.g. "im", "ive") 
stop_words = ["i", "ive", "im", "id" ,"me", "my", "myself", "we", "our", "ours", "ourselves",
"you", "your", "yours", "youre", "yourself", "yourselves", "he", "him", "his", "himself",
"she", "her", "hers", "herself", "ill", "it", "its", "itself", "they", "them", "their",
"theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those",
"am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
"having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", 
"because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", 
"between", "into", "through", "during", "before", "after", "above", "below", "to", "from", 
"up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", 
"here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
"most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
"too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "oh"]

#Import the transcriptions and returns a csv reader object. Avoids redundant code.
def import_trans():
    transcription = r"C:\Users\heheh\Desktop\work\P-and-R-analysis\data\p_r_scripts.csv"
    f = open(transcription, 'r', encoding='Latin 1')
    t_out = csv.reader(f)
    return t_out

#Returns the characters present in the transcript.
def get_characters():
    output = []
    temp = import_trans()
    for row in temp:

        #Ignore lines that haven't been attributed to a character.
        if row[0] == '':
            continue
        if row[0] not in output:
            output.append(row[0])
    return output

#Removes punctuation, white space (leading, trailing, and extra within), lowercase, returns the line as a list of words
def clean_strip_line(line):
    out = line.lower()
    for p in string.punctuation:
        out = out.replace(p, '')
    return out.strip()

#-------------------TF FUNCTIONS--------------------------------------------------------------

#Generate the term frequencies, as a Python dictionary, in the corresponding transcription of lines in the show. Accepts a boolean for whether or not to include stop words in the final
#TF output (by default False).

#Example (just for my own memory of the format):
#term_frequency() = {... "Leslie Knope": {'word': X, 'word2': Y, ...} ...}
def term_frequency(stop_w = True):

    t_reader = import_trans()

    #Final output as nested dictionary; character name as key, dictionary of words-to-frequency as value.
    final_char = {}

    for l in t_reader:
        speaker = l[0]
        line = clean_strip_line(l[1])

        if speaker == '': #Ignore lines not assigned to characters (unfinished transcription)
            continue
        if speaker in final_char: #Speaker has appeared before
            for word in line.lower().split():

                #If the associated word frequency dictionary for a character has the word already
                if word in final_char[speaker]:
                    final_char[speaker][word] = final_char[speaker][word] + 1
                else:
                    final_char[speaker].update({word : 1})

        #If the speaker hasn't yet appeared, create a new entry with an empty word-frequency dictionary.
        else:
            final_char.update({speaker : {} })

    #Eliminate stop word entries if necessary
    if (stop_w == True):
        for k in final_char:
            for w in stop_words:
                if w in final_char[k].keys():
                    del (final_char[k])[w]
                else:
                    continue
    return final_char

#Returns a list of tuples sorted from highest to lowest of a character's spoken words. Second optional argument for whether or not to include stop words. (for debugging)
def get_sorted_tf(character, stop_w = True):
    term_freq = term_frequency(stop_w)
    return sorted(term_freq[character].items(), key = lambda x: x[1], reverse = True)

#Generate the number of episodes each character appears in.
#e.g. {"Leslie Knope": 122, ...}
def episode_appearance():
    
    t_reader = import_trans()
    total = {}
    season = 1
    episode = 1
    appearances = [] #Characters that appear in current episode
    for l in t_reader:
        speaker = l[0]
        line = l[1]

        #New episode
        if "Season: " in line and "Episode: " in line:
            for c in appearances:
                if c in total:
                    total[c]+=1
                else:
                    total[c]=1
            season = int(line[len("Season: "): len("Season: ")+1])
            episode = int(line[len("Season: x Episode: "):])
            appearances = []
        else:
            if speaker in appearances:
                continue
            else:
                appearances.append(speaker)
    
    #Add the last episode
    for c in appearances:
        if c in total:
            total[c] += 1
        else:
            total[c]=1

    return total


#Generate the average number of words spoken per episode
def average_word_by_episode(stop_w = False):
    tf = term_frequency(stop_w)
    eps = episode_appearance()

    #Get total words for each character
    total_words = {}
    for character in tf.keys():
        total_words[character] = 0
        for word in tf[character]:
            total_words[character] += tf[character][word]
    
    output = {}
    for c in total_words:
        print(c)
        print(total_words[c])
        print(eps[c])
        output[c] = total_words[c]/eps[c]
    
    return output

#Write average words to CSV file.
def write_avg_word_to_file():
    fieldnames = ["Character", "Average"]
    target = r'C:\Users\heheh\Desktop\work\P-and-R-analysis\data\average_words_by_episode.csv'
    target = open(target, 'w', newline='', encoding="utf-8")
    writer = csv.DictWriter(target, fieldnames=fieldnames)

    avgs = average_word_by_episode()
    for c in avgs:
        writer.writerow({"Character": c, "Average": avgs[c]})

#Write the term frequencies for every character to a CSV file.
def write_to_file_tf(stop_w = False):
    fieldnames = ["Character", "Word", "Frequency"]
    target = r'C:\Users\heheh\Desktop\work\P-and-R-analysis\data\term_frequencies.csv'
    target = open(target, 'w', newline='', encoding="utf-8")
    writer = csv.DictWriter(target, fieldnames=fieldnames)
    
    #For each character, get their TF-IDF dictionaries and write to the file.
    c = get_characters()
    print(c)
    for character in c:
        if character == "Character":
            continue
        print("Writing frequencies for character: " + character)
        term_freq = term_frequency(stop_w)[character]
        for word in term_freq:
            writer.writerow({"Character": character, "Word": word, "Frequency": term_freq[word]})

#-----------------------------IDF FUNCTIONS-----------------------------------
#Generate the inverse document frequency (IDF), as a Python dictionary, for a set of transcriptions. Specifically, for each character, this function will output
#each word's IDF value corresponding to each character. Each "document" is defined as an episode (previously, per line, un-ideal).

#Notes: currently uses base-10 logarithmic weighting.

#Example: idf() = {...'Leslie Knope' : {...'word1' : 0.5, 'word2' : .1, ...} ... }
def idf(stop_w = True):

    #Convert lines to dictionary for easier parsing, as a list of tuples. Skips any unlabeled lines.
    t_reader = import_trans()
    transcription = []        
    for l in t_reader:
        
        speaker = l[0]
        temp_line = l[1]
        if (speaker == '' or speaker == 'Character') and ("Season: " not in temp_line and "Episode: " not in temp_line): #Ignore unattributed lines, except for those that delineate a new episode.
            continue
        else:
            temp_line = temp_line.lower()                             #Lowercase, remove whitespace, remove punctuation
            for p in string.punctuation:
                temp_line = temp_line.replace(p, '')
            temp_line.strip() 
        
        to_add = (speaker, temp_line)
        transcription.append(to_add)

    output = {}
    episode_words = {} #Maintain a list of words spoken for each character for a single episode.
    characters = [i[0] for i in transcription]
    characters = list(set(characters))

    #Create dictionary entries for each character, where key = character and value = words spoken
    for c in characters:
        output[c] = {}
        episode_words[c] = [] #Only need to maintain which words have been said

    transcript_line_number = 0 #Track the line of the transcript the loop is currently processing.
    episode_number = 0 #Track the episode number.
    
    for line in transcription:
        transcript_line_number = transcript_line_number + 1
        #For each episode, maintain a list of words that the character has spoken. After each episode, update the overall tracker; at the end, should be aggregate count.


        #print(str(transcript_line_number) + ": " + line[1])
        #Detect whether we've reached a new episode. If so, update the overall output with a total count of document appearances per word, per character, then reset episode_words.
        if ("season " in line[1] and "episode " in line[1]) or line[1] == 'line':
            for person in episode_words.keys():
                words_appeared = episode_words[person]                
                
                #Go through each word that was spoken in the episode by the character. Increment the count for all words that appear.
                for word in words_appeared:
                    if word in output[person]:
                        output[person][word] = output[person][word] + 1
                    else:
                        output[person][word] = 1

                episode_words[person] = {} #Reset the words that have appeared in the episode in question for this character.
            episode_number = episode_number+1 #Update the episode number.

        else:
            for word in line[1].split():
                if (word in stop_words) and (stop_w == True): #Check for stop words
                    continue
                if len(episode_words[line[0]]) == 0: #If the list of spoken words for the character is empty, create a list.
                    episode_words[line[0]] = [word]
                elif word not in episode_words[line[0]]: #Add the word to list of spoken words for the character attributed to the line
                    episode_words[line[0]].append(word)
                else:
                    continue
        
        #DETECT THE LAST LINE, because there will be no "new episode" indicator, using the line number tracker; do what you would do as if a new episode was beginning.
        if transcript_line_number == len(transcription):
            for person in episode_words.keys():
                words_appeared = episode_words[person]                
                
                #Go through each word that was spoken in the episode by the character. Increment the count for all words that appear.
                for word in words_appeared:
                    if word in output[person]:
                        output[person][word] = output[person][word] + 1
                    else:
                        output[person][word] = 1

    #Compute the actual IDF scores for each word.
    for c in characters:
        for word in output[c]:
            output[c][word] = math.log(episode_number/(output[c][word]), 10) #IDF = log(N / n), where N = total number of episodes, n = episodes the word appears in.
    return output

#Return a given character's list of words by TF * IDF weighting, sorted from highest to lowest. Optional parameter to round the numbers for readability (default 10).
def tf_idf_char(character, stop_w = True, r_pts = 10):
    char_tf = term_frequency(stop_w)[character]
    char_idf = idf(stop_w)[character]
    
    #Compute the tf_idf for each word
    output = {word : round(char_tf[word] * char_idf[word], r_pts) for word in char_tf.keys()}
    return output

#Returns the tf_idf of each word for a character, sorted (for printing, mostly)
def sorted_tf_idf_char(character, stop_w = True, r_pts = 10):
    temp = tf_idf_char(character, stop_w, r_pts)
    return sorted(temp.items(), key = lambda x: x[1], reverse = True)


#Write the total tf_idf scores for every character and word to file. 
def write_to_file_tfidf(stop_w = True, r_pts = 10):
    fieldnames = ["Character", "Word", "TF-IDF"]
    target = r'C:\Users\heheh\Desktop\work\P-and-R-analysis\data\tf_idf_full.csv'
    target = open(target, 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(target, fieldnames=fieldnames)
    
    #For each character, get their TF-IDF dictionaries and write to the file.
    c = get_characters()
    print(c)
    for character in c:
        if character == "Character":
            continue
        print("Writing words for character: " + character)
        tf_idf = tf_idf_char(character, stop_w, r_pts)
        for word in tf_idf:
            writer.writerow({"Character": character, "Word": word, "TF-IDF": tf_idf[word]})

#Create complete CSV file; comment out if you don't want it to.
#write_to_file_tfidf()
#write_to_file_tf()