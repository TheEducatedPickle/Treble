from PyLyrics import *
import nltk

def get_features(lyrics: 'string'):
    def normalize_line(line):
        for i in reversed(range(len(line))):
            print(line[i])
            if line[i] in ['(',')']: del line[i]
            else: line[i] = line[i].lower()
        
    lines = [nltk.word_tokenize(line) for line in lyrics.split("\n") if line is not '']
    for line in lines:
        normalize_line(line)
    return lines
    
def classify(artist, track):
    #Lyric retrieval
    lyrics = PyLyrics.getLyrics(artist,track)
    lyrics = get_features(lyrics)
    print(lyrics)
    
if __name__ == '__main__':
    classify('Taylor Swift','Blank Space')