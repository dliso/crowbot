from nltk.corpus import wordnet
import nltk
import string

def lemmalize(statement):

    a = statement.lower()
    # Get default English stopwords and extend with punctuation
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(string.punctuation)
    stopwords.append('')
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    def get_wordnet_pos(pos_tag):
        if pos_tag[1].startswith('J'):
            return (pos_tag[0], wordnet.ADJ)
        elif pos_tag[1].startswith('V'):
            return (pos_tag[0], wordnet.VERB)
        elif pos_tag[1].startswith('N'):
            return (pos_tag[0], wordnet.NOUN)
        elif pos_tag[1].startswith('R'):
            return (pos_tag[0], wordnet.ADV)
        else:
            return (pos_tag[0], wordnet.NOUN)

    pos_a = map(get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(a)))
    lemma_a = [lemmatizer.lemmatize(token.strip(string.punctuation), pos) for token, pos in pos_a
               if pos == wordnet.NOUN and token.strip(string.punctuation) not in stopwords]
    return lemma_a

