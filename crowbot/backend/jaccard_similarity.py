from nltk.corpus import wordnet
import nltk
import string

def jaccard_similarity(lemmas1, lemmas2, threshold=0.7):
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
    # Calculate Jaccard similarity
    try:
        ratio = len(set(lemmas1).intersection(lemmas2)) / float(len(set(lemmas1).union(lemmas2)))
    except Exception as e:
        print('Error', e)
    return [ratio >= threshold, ratio]

"""
print(jaccard_similarity('When is the exam in TDT4140?',
                         'What is the exam date for TDT4140?'))
#Likehet 66,6666%

print(jaccard_similarity('How many exercises is needed in TMA4100?',
                         'How many exercises is mandatory in TMA4100?')[0])
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

"""
