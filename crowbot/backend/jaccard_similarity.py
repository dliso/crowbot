from nltk.corpus import wordnet
import nltk
import string

def jaccard_similarity(statement, other_statement, threshold=0.7):
    """
    Calculates the similarity of two statements based on the Jaccard index.

    The Jaccard index is composed of a numerator and denominator.
    In the numerator, we count the number of items that are shared between the sets.
    In the denominator, we count the total number of items across both sets.
    Let's say we define sentences to be equivalent if 50% or more of their tokens are equivalent.
    Here are two sample sentences:

        The young cat is hungry.
        The cat is very hungry.

    When we parse these sentences to remove stopwords, we end up with the following two sets:

        {young, cat, hungry}
        {cat, very, hungry}

    In our example above, our intersection is {cat, hungry}, which has count of two.
    The union of the sets is {young, cat, very, hungry}, which has a count of four.
    Therefore, our `Jaccard similarity index`_ is two divided by four, or 50%.
    Given our threshold above, we would consider this to be a match.

    .. _`Jaccard similarity index`: https://en.wikipedia.org/wiki/Jaccard_index
    """


    a = statement.lower()
    b = other_statement.lower()
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

    ratio = 0
    pos_a = map(get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(a)))
    pos_b = map(get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(b)))
    lemma_a = [lemmatizer.lemmatize(token.strip(string.punctuation), pos) for token, pos in pos_a
               if pos == wordnet.NOUN and token.strip(string.punctuation) not in stopwords]
    lemma_b = [lemmatizer.lemmatize(token.strip(string.punctuation), pos) for token, pos in pos_b
               if pos == wordnet.NOUN and token.strip(string.punctuation) not in stopwords]

    # Calculate Jaccard similarity
    try:
        ratio = len(set(lemma_a).intersection(lemma_b)) / float(len(set(lemma_a).union(lemma_b)))
        print(ratio)
    except Exception as e:
        print('Error', e)
    return ratio >= threshold


print(jaccard_similarity('When is the exam in TDT4140?',
                         'What is the exam date for TDT4140?'))
#Likehet 66,6666%

print(jaccard_similarity('How many exercises is needed in TMA4100?',
                         'How many exercises is mandatory in TMA4100?'))
#Likhet 100%

print(jaccard_similarity('If I completed the exercises last year, are they valid this year?',
                         'Are the exercises I did last year valid this year?'))
#Likhet 100%

print(jaccard_similarity('If I completed the exercises four years ago, are they valid this year?',
                         'Are the exercises I did last year valid this year?'))
#Likhet 66,66666%

print(jaccard_similarity('Are the exercises I did four years ago valid this year?',
                         'Are the exercises I did last year valid this year?'))
#Likhet 50%

print(jaccard_similarity('If I completed the exercises last year, are they valid this year?',
                         'How old can previously completed exercises be, to be valid?'))
#Likhet 50%


