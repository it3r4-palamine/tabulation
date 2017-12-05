# Imports
import difflib
import nltk
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string
from ..views.common import *

from nltk.corpus import wordnet as wn
from nltk.tokenize import WordPunctTokenizer

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

def get_wordnet_pos(pos_tag):
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wn.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wn.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wn.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wn.ADV)
    else:
        return (pos_tag[0], wn.NOUN)

# Create tokenizer and stemmer
tokenizer = WordPunctTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

def is_ci_partial_set_token_stopword_lemma_match(a, b):
    """Check if a and b are matches."""
    pos_a = map(get_wordnet_pos, nltk.pos_tag(tokenizer.tokenize(a)))
    pos_b = map(get_wordnet_pos, nltk.pos_tag(tokenizer.tokenize(b)))
    lemmae_a = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
                    if token.lower().strip(string.punctuation) not in stopwords]
    lemmae_b = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_b \
                    if token.lower().strip(string.punctuation) not in stopwords]
    # Calculate Jaccard similarity
    ratio = len(set(lemmae_a).intersection(lemmae_b)) / float(len(set(lemmae_a).union(lemmae_b)))
    return (ratio > 0.66)


def sentence_matching(target_sentence,model,pk,model_pk=None):
	filters = {"question" : pk,"is_active" : True}
	model = str_to_model(model)

	if model_pk:
		sentences = model.objects.filter(**filters).exclude(id=model_pk).values_list('value',flat=True)
	else:
		sentences = model.objects.filter(**filters).values_list('value',flat=True)

	similar_sentences = None
	sentences = [x.lower() for x in sentences]
	if target_sentence.lower() in sentences:
		similar_sentences = target_sentence
	else:
		for sentence in sentences:
			result = is_ci_partial_set_token_stopword_lemma_match(target_sentence, sentence)
			if result:
				similar_sentences = sentence
	

	return similar_sentences

