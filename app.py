from flask import Flask, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import json

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def textSummarizer():
    blog = request.args['blog']
    unwanted_chars = [';', ':', '!', "*", '#', '@', '$', '%', '^', '(', ')', '`', '?','[',']']
    for i in unwanted_chars:
        blog = blog.replace(i, '')
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(blog)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    sentences = sent_tokenize(blog)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues / len(sentenceValue))
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2* average)):
            print(summary)
            summary += " " + sentence
    summary_dictionary = {"summary": summary}
    json_summary = json.dumps(summary_dictionary);
    return json_summary


if __name__ == '__main__':
    app.run()
