#Methods for computing term frequencies, inverse document frequencies (idf) in order to create tf-idf matrix for
#the words spoken by characters on the tv show Parks and Recreation.

import csv
import sys
import re

#-----------------------------------------------------------------------------------------


#Generate the term frequencies, as a Python dictionary, in the corresponding transcription of lines in the show.
def term_frequency():

    #Import the transcriptions, iterate through each line.
    transcription = r"C:\Users\heheh\Desktop\work\P-and-R-analysis\data\p_r_scripts_final_two.csv"
    f = open(transcription, 'r')
    t_reader = csv.reader(f)

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
    
    return final_char

#Returns a list of tuples sorted from highest to lowest of a character's spoken words.
def get_sorted(character, term_freq):
    return sorted(term_freq[character].items(), key = lambda x: x[1], reverse = True)


#Generate the inverse document frequency (IDF) for a set of transcriptions.
def idf():
    pass