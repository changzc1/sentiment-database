#Source code for testing and calculating the emotional value of comments
import re
import json
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()


dict_one_to_more = defaultdict(list)

file = 'NTUSD-Fin/Fin_word_v1.0.json'
# 上面路径是我的json文件所在地，后面包含中文编码
with open(file, 'r', encoding='utf-8') as f:
    pop_data = json.load(f)
    for line in pop_data:
        bear_cfidf = line['bear_cfidf']
        bull_cfidf = line['bull_cfidf']

        market_sentiment = line['market_sentiment']
        token = line['token']
        dict_one_to_more[token].append(market_sentiment)
        dict_one_to_more[token].append(bear_cfidf)
        dict_one_to_more[token].append(bull_cfidf)
def  SumOfSentiment(text,sentiment):
    sentencevalue = 0
    switch = 0
    text = re.sub(r'[^a-zA-Z]', ' ',text)
    words = text.lower().split()

    for index in range(len(words)):


      try:
        words[index]=wnl.lemmatize(words[index])
      except:
        continue
    for word in words:
        for temp in dict_one_to_more:
            if word == temp:
                if   sentiment is 'Buy':
                     switch = float(dict_one_to_more[temp][2] / 100)
                     sentencevalue += float(dict_one_to_more[temp][0] * switch)
                if   sentiment is 'Sell':
                     switch = float(dict_one_to_more[temp][1] / 100)
                     sentencevalue += float(dict_one_to_more[temp][0] * switch)

                if   sentiment is 'Hold':
                     switch = float((dict_one_to_more[temp][1]+dict_one_to_more[temp][2]) / 200)
                     sentencevalue += float(dict_one_to_more[temp][0] * switch)
            else:
                continue
    if sentencevalue > 0.2:
        return  1
    if sentencevalue < -0.2:
        return   -1
    if -0.2<sentencevalue < 0.2:
        return   0
tt='AAPL continues to have strong demand for every product category but still appears expensive.'
hh='Analysts have lowered their expectations for June-Q due to several strong headwinds that are expected to place a drag on AAPL\'s earnings.'
ll='Key suppliers of AAPL that operate in China have cut shipment forecasts and continue to face Covid-19 shutdowns.'
pp = 'Additionally, analysts are projecting a noticeable stagnation in growth for FY22 and FY23.'
uu = 'Under relative and absolute valuation metrics, AAPL appears overvalued.'
positive = 0
minus = 0
truepositive = 0

outputsum = []
outputsum.append(SumOfSentiment(tt, 'Hold'))
outputsum.append(SumOfSentiment(hh, 'Hold'))
outputsum.append(SumOfSentiment(ll, 'Hold'))
outputsum.append(SumOfSentiment(pp, 'Hold'))
outputsum.append(SumOfSentiment(uu, 'Hold'))
sentencevaluelist=0
for i in range(0, len(outputsum)):
    if outputsum[i] == -1:
        minus = minus + 1

    if outputsum[i] == 0:
        positive = positive + 1

    if outputsum[i] == 1:
        truepositive = truepositive + 1

if (minus >= positive and minus >= truepositive):
    if minus == positive or minus == truepositive:
        sentencevaluelist=0

    if (minus > positive and minus > truepositive):
        sentencevaluelist=-minus / len(outputsum)

elif (positive >= minus and positive >= truepositive):
    if minus == positive or positive == truepositive:
        sentencevaluelist=0

    if (positive > minus and positive > truepositive):
        sentencevaluelist=0

else:
    if minus == truepositive or positive == truepositive:
        sentencevaluelist=0

    if (truepositive > minus and truepositive > positive):
        sentencevaluelist=truepositive / len(outputsum)
sentencevaluelist
