import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from textblob.classifiers import  NaiveBayesClassifier
from textblob import TextBlob

train = [
  ('damaged', 'negative'),
  ('not working', 'negative'),
  ('making noise', 'negative'),
  ('fine', 'positive')
]
cl = NaiveBayesClassifier(train)

"""
nlp = spacy.load('../../res/models/en_core_web_sm-3.5.0')
nlp.add_pipe('spacytextblob')
text = 'I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.'
doc = nlp(text)
print(doc._.blob.polarity)
"""

def analyseSentiments(compDesc):
    nlp = spacy.load('../../res/models/en_core_web_sm-3.5.0')
    nlp.add_pipe('spacytextblob')
    print('SA:', compDesc)
    for component in compDesc.keys():
        compDescList = compDesc[component]
        for desc in compDescList:
            doc = nlp(desc['sentence'])
            desc['polarity'] = doc._.blob.polarity
            print(desc['sentence'], desc['polarity'], doc)
    return compDesc


def analyseSentiment(compDesc):
    cl = NaiveBayesClassifier(train)
    print('SA:', compDesc)
    for component in compDesc.keys():
        compDescList = compDesc[component]
        for desc in compDescList:
            blob = TextBlob(desc['sentence'], classifier=cl)
            print(blob, blob.classify(), blob.polarity)
            desc['sentiment'] = blob.classify()
    return compDesc