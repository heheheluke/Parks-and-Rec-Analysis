#Process the final term frequency data.

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
import pandas as pd
import numpy as np
import random

def rand_colors(n):
    output = []
    for i in range(n):
        color = [random.randint(0, 255)/255, random.randint(0, 255)/255, random.randint(0, 255)/255]
        output.append(color)
    return output

prop = fm.FontProperties(fname=r'C:\Users\heheh\Anaconda3\pkgs\matplotlib-3.1.1-py37hc8f65d3_0\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\OpenSansCondensed-Light.ttf')

#Read in
colnames = ['Character', 'Word', 'TF-IDF']
tfidf_data = pd.read_csv(r"data\tf_idf_full.csv", names=colnames, encoding='latin1')

colnames = ['Character', 'Word', 'Frequency']
freq_data = pd.read_csv(r"data\term_frequencies.csv", names=colnames, encoding='latin1')

#The list of characters to create plots for
characters = [
    "Leslie Knope",
    "Ben Wyatt",
    "Tom Haverford",
    "Ron Swanson",
    "April Ludgate",
    "Andy Dwyer",
    "Chris Traeger",
    "Ann Perkins",
    "Jerry Gergich",
    "Donna Meagle"]

colors = [
    '#F9F871', #Leslie
    '#B0A8B9', #Ben
    '#FF9671', #Tom
    '#936C00', #Ron
    '#4B4453', #April
    '#008B74', #Andy
    '#FF8066', #Chris
    '#3D8AA4', #Ann
    '#BA3CAF', #Jerry
    '#391C77'] #Donna

def plot_tf_idf():
    #Plots for TF-IDF values
    c = 0
    plt.rcParams["figure.figsize"] = [14,2]

    fig, axes = plt.subplots(nrows=2, ncols=5)
    for row in axes:
        for col in row:
            print(characters[c])
            d = tfidf_data[tfidf_data.Character == characters[c]]
            top = d.nlargest(15, 'TF-IDF')
            min = top["TF-IDF"].min()
            max = top["TF-IDF"].max()
            p = top.plot(x='Word', y='TF-IDF', kind='barh', ax = col, width=.7)
            
            #Subplot attributes
            p.set_title(characters[c], fontproperties=prop, fontsize = 12)
            p.get_legend().remove()
            p.tick_params(axis='y', labelsize = '8')
            p.tick_params(axis='x', labelsize='6')
            p.set_ylabel('')
            p.invert_yaxis()
            p.set_xlim([.95*min, 1.04*max])

            c+=1 #Next character

    fig.suptitle("Every character's most important words (using TF-IDF weighting)", fontproperties=prop, fontsize=18)
    plt.tight_layout(pad=0, w_pad=-1)

#Plot total words spoken by each character per episode, by season
def bar_plot_avg_words():
    data = pd.read_csv(r'data/term_frequencies_by_season.csv', encoding='latin1')
    
    #Size of bars
    width = .08
    curr_width = -(10*width - width)/2
    
    #Plot
    episode_count = [6,24,16,22,22,20,12]
    fig, ax = plt.subplots()
    for i, c in enumerate(characters):
        char_row = data.loc[data.Character == c]
        char_row = char_row.values.tolist()[0]
        char_row.pop(0)
        char_row = [x/episode_count[se] for se, x in enumerate(char_row)]

        season = np.arange(1,8)
        ax.bar(x=season+curr_width, height=char_row, width=width, label=c, color=colors[i])
        curr_width += width
    
    #Styling
    ax.legend()
    ax.set_xlim(.5, 7.5)
    ax.set_xticks([1,2,3,4,5,6,7], minor=False)
    ax.set_xticks([1.5,2.5,3.5,4.5,5.5,6.5], minor=True)
    ax.xaxis.grid(True, which='minor')
    ax.set_xlabel('Season', fontproperties=prop, fontsize=12)
    ax.set_ylabel('Word Count', fontproperties=prop, fontsize=12)
    fig.suptitle('Main Character Word Count By Season', fontsize=20)

#Generate charts
plot_tf_idf()
bar_plot_avg_words()

plt.show()

