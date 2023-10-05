from deepsegment import DeepSegment

def segment(text):
    segmenter = DeepSegment('en')
    sentences = segmenter.segment(text)
    for i in range(len(sentences)):
        sentences[i] = sentences[i].capitalize()
    segmentedText = '.\n'.join(sentences)
    return segmentedText+'.'
