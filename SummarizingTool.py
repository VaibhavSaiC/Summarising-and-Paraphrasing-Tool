import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from language_tool_python import LanguageTool

def paraphrase_sentence(sentence):
    words = word_tokenize(sentence)
    paraphrased_words = []

    exceptions = ["and", "or", "but", "nor", "for", "yet", "so",  # Conjunctions
                  "i", "you", "he", "she", "it", "we", "they", "me", "him", "her","us", "them",    # Pronouns
                  "this", "that", "these", "those",                # Determiners
                  "a", "an", "the"]                                           # Articles

    # Customize the stopwords list to exclude exceptions
    stop_words = set(stopwords.words("english")) - set(exceptions)

    for word in words:
        # Exception for specific words to keep them unchanged
        if word.lower() in exceptions:
            paraphrased_words.append(word)
            continue

        # Skip stop words
        if word.lower() in stop_words:
            paraphrased_words.append(word)
            continue

        synonyms = wordnet.synsets(word)
        if synonyms:
            paraphrased_word = synonyms[0].lemmas()[0].name()
            paraphrased_word = paraphrased_word.replace("_", " ")  # Remove underscores
            paraphrased_words.append(paraphrased_word)
        else:
            paraphrased_words.append(word)

    paraphrased_sentence = ' '.join(paraphrased_words)
    return paraphrased_sentence



def improve_paraphrasing(paraphrased_text, original_text):
    original_sentences = sent_tokenize(original_text)
    paraphrased_sentences = sent_tokenize(paraphrased_text)

    improved_sentences = []
    for paraphrased_sentence, original_sentence in zip(paraphrased_sentences, original_sentences):
        improved_sentence = paraphrased_sentence

        # Replace paraphrased words with original words if they are in the original sentence
        paraphrased_words = word_tokenize(paraphrased_sentence)
        original_words = word_tokenize(original_sentence)
        for i, paraphrased_word in enumerate(paraphrased_words):
            if paraphrased_word in original_words:
                improved_sentence = improved_sentence.replace(paraphrased_word, original_words[i])

        improved_sentences.append(improved_sentence)

    improved_text = ' '.join(improved_sentences)
    return improved_text



def summarize_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]

    # Calculate word frequencies
    word_frequencies = nltk.FreqDist(filtered_text)
    most_frequent_words = [word for word, frequency in word_frequencies.most_common(10)]

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in most_frequent_words:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    # Sort sentences by score in descending order
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Filter out short sentences
    filtered_sentences = [sentence for sentence in ranked_sentences if len(word_tokenize(sentence)) > 8]

    # Generate summary
    summary = " ".join(filtered_sentences)

    return summary


# User input
print("Enter the text to be summarized: ")
text = input()

# Paraphrase the input text
paraphrased_text = paraphrase_sentence(text)
print("Paraphrased Text:")
print(paraphrased_text)

# Summarize the paraphrased text
summary = summarize_text(paraphrased_text)
print("Summary:")
print(summary)