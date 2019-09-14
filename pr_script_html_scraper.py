from lxml import html
import requests
import csv

all_lines = []  #Final list of all lines, separated by season and episode

#---------------------------------Processing------------------------------------------

#Given a string and a punctuation to look for, return a list of strings, separated by those punctuations
def separate(str, punct_arr):
    str_start = 0
    output = []
    for i in range(0, len(str)-1):
        if str[i] in punct_arr:
            output.append(str[str_start:i+1])
            str_start = i+1
    
    output.append(str[str_start:])
    return output


#Loop through each season, each episode
season_lengths = [6,24,16,22,22,21,12]

for season in range(1, 8):
    for episode in range(1, season_lengths[season-1]+1):

        #Convert episode number to string; add 0 if episode # is single digit (format of website URL)
        if (episode < 10):
            episode = '0' + str(episode)
        else:
            episode = str(episode)

        all_lines.append("Season: " + str(season) + " Episode: " + episode) #Add season/episode delineation for data readability
        print("Reading - " + "Season: " + str(season) + " Episode: " + episode)

        #Grab HTML, parse for " <div class="scrolling-script-container"> ", save as string list of lines
        target_url = 'https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=parks-and-recreation&episode=s0' + str(season) + 'e' + episode
        page = requests.get(target_url)
        tree = html.fromstring(page.content)
        lines = tree.xpath('//div[@class="scrolling-script-container"]/text()')


        #Iterate thru lines to clean up, separate by punctuation
        remove_these = ['\n', '\r', '\t', '-', 'â', '\x80', '\x99']
        for idx in range(0, len(lines)):
            
            #Clean up lines, get rid of \n, \r, \t, hyphens, whitespace, empty lines
            for i in remove_these:
                lines[idx] = (lines[idx]).replace(i, '')
            lines[idx] = (lines[idx]).strip()

            #Break up lines by ending punctation to avoid two different speakers in same line; [?, !, .]
            punct = ["?", "!", "."]
            if any([x in lines[idx] for x in punct]):
                sep_str = separate(lines[idx], punct)
                lines.pop(idx)                       #Remove the existing line
                lines[idx:idx] = sep_str             #Replace with the separated lines at the right index


        lines[:] = (s for s in lines if s != '') #Remove any lines that are empty

        #Break up the lines by ending punctuation, e.g. ?, !, ., 
        

        all_lines.extend(lines)

#---------------------------------------------------------------------------------------------

#Write final list of lines to excel file
target = r'C:\Users\heheh\Desktop\data\p_r_scripts_final.csv'

target = open(target, 'w', newline='')
writer = csv.writer(target)
for val in all_lines:
    writer.writerows([[val]])

print("Writing finished")