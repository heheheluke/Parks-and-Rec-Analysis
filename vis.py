#Process the final term frequency data.

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
import pandas as pd
import numpy as np

prop = fm.FontProperties(fname=r'C:\Users\heheh\Anaconda3\pkgs\matplotlib-3.1.1-py37hc8f65d3_0\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\OpenSansCondensed-Light.ttf')

#Read in
colnames = ['Character', 'Word', 'TF-IDF']
tfidf_data = pd.read_csv(r"data\tf_idf_full.csv", names=colnames, encoding='latin1')

colnames = ['Character', 'Word', 'Frequency']
freq_data = pd.read_csv(r"data\term_frequencies.csv", names=colnames, encoding='latin1')

#The list of characters to create plots for
characters = ["Leslie Knope", "Ben Wyatt", "Tom Haverford", "Ron Swanson", "April Ludgate", "Andy Dwyer", "Chris Traeger", "Ann Perkins", "Jerry Gergich", "Donna Meagle"]

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

# #Plot for total words spoken
# totals = []
# for c in characters:
#     d = freq_data[freq_data.Character == c]
#     totals.append(d.Frequency.sum())
# t = pd.DataFrame({'Characters': characters, 'Totals': totals})
# t = t.plot(kind='barh', x="Characters")
# for i,v in enumerate(totals):
#     t.text(v, i, str(v), ha = 'left', va = 'center', color='blue')

plt.show()

