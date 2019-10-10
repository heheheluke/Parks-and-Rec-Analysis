#TO DO: 
#1) Stop words for TF
#2) IDF

#Methods for computing term frequencies, inverse document frequencies (idf) in order to create tf-idf matrix for
#the words spoken by characters on the tv show Parks and Recreation.

import csv
import sys
import re
import math

#-----------------------------------------------------------------------------------------

#Stop words list pulled from NLTK, with some added myself (largely contractions, due to removing all punctuation) 
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
"too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

#Import the transcriptions, iterate through each line.
def import_trans():
    transcription = r"C:\Users\heheh\Desktop\work\P-and-R-analysis\data\p_r_scripts_final_two.csv"
    f = open(transcription, 'r')
    t_out = csv.reader(f)
    return t_out

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
        line = l[1].lower().strip()     #Lowercase, remove whitespace, remove punctuation
        line = re.sub(r'[^\w\s]','', line) 

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



#Returns a list of tuples sorted from highest to lowest of a character's spoken words. Second optional argument for whether or not to include stop words.
def get_sorted_tf(character, stop_w = True):
    term_freq = term_frequency(stop_w)
    return sorted(term_freq[character].items(), key = lambda x: x[1], reverse = True)


#----------------------------------IDF FUNCTIONS---------------------------------

#Generate the inverse document frequency (IDF), as a Python dictionary, for a set of transcriptions. Specifically, for each character, this function will output
#each word's IDF value corresponding to each character.

#Notes: currently uses natural logarithmic weighting.

#Example: idf() = {...'Leslie Knope' : {...'word1' : 0.5, 'word2' : .1, ...} ... }
def idf(stop_w = True):

    output = {}

    t_reader = import_trans()

    #Convert lines to dictionary for easier parsing
    transcription = []        
    for l in t_reader:
        speaker = l[0]
        line = l[1].lower().strip()                             #Lowercase, remove whitespace, remove punctuation
        line = re.sub(r'[^\w\s]','', line) 
        if (speaker == '' or speaker == 'Character'):
            continue
        
        to_add = (speaker, line)
        transcription.append(to_add)

    #Grab list of characters
    characters = [i[0] for i in transcription]
    characters = list(set(characters)) 

    for c in characters:
        c_only_trans = [l[1] for l in transcription if c == l[0]] #Isolate the lines for which c is the speaker 

        #Go through each line; for each word, increment the document appearance count.
        word_freqs = {}
        for line in c_only_trans:
            already_appeared = [] #Maintain a list of words that have already appeared in the line, that will reset per line

            for word in line.split():

                if ((word in stop_words) and (stop_w == True)):     #Check for stop words
                    continue

                if word in already_appeared: #Skip words that have already appeared
                    continue
                
                if word in word_freqs: 
                    word_freqs[word] = word_freqs[word] + 1
                else:
                    word_freqs.update({word : 1})
                
                already_appeared.append(word)

        #Divide the document appearance frequency by the total number of lines spoken by the character (i.e. total number of documents),
        #then take the log of the inverse.
        word_freqs.update((k, math.log(len(c_only_trans)/v) ) for k,v in word_freqs.items())
        #Add the character's idf to the final output
        output[c] = word_freqs

    return output


#Return a given character's list of words by TF * IDF weighting, sorted from highest to lowest. Optional parameter to round the numbers for readability.
def tf_idf(character, stop_w = True, r_pts = 10):
    char_tf = term_frequency(stop_w)[character]
    char_idf = idf(stop_w)[character]
    
    output = {word : round(char_tf[word] * char_idf[word], r_pts) for word in char_tf.keys()}
    return sorted(output.items(), key = lambda x: x[1], reverse = True)