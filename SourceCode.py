#This file includes the source code for downloading expert comments from the seekingalpha and calculating the sentimental value of comments
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
from collections import defaultdict
import datetime
from nltk.stem import WordNetLemmatizer
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('-–headless')
chrome_options.add_argument("–window-size=1024,1024")
chrome_options.add_argument("--disable-browser-side-navigation");
chrome_options.add_argument("enable-automation");
chrome_options.add_argument("start-maximized");
chrome_options.add_argument("--disable-blink-features");
chrome_options.add_argument("--disable-blink-features=AutomationControlled");
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe"

browser = webdriver.Chrome('C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe',
                           chrome_options=chrome_options)
browser.get("https://seekingalpha.com")
dict_one_to_more = defaultdict(list)
wcontant = {}
value = []
contantkey = ''
contanttempvalue = ''
contantvalue = ''
contantlist = []
action_chains = ActionChains(browser)

mainWindow = browser.current_window_handle
j = 1

incut=["AAPL","LMPX","KMX","LMPX"]
stoname=["Apple Inc","LMP Automotive","KMX","LMPX"]
#查找页面上是否存在相关的元素
wnl = WordNetLemmatizer()
file = 'Fin_word_v1.0.json'
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
class ElementExist(object):
    @classmethod
    def isElementExist(cls, driver, elements):

        try:
            WebDriverWait(browser, 80).until(EC.visibility_of_element_located(
                (By.XPATH, elements)))

            browser.find_element_by_xpath(elements)

            return True
        except:

            return False

import re
count = 0
text=''
#日期格式化函数
def divide(DATA):

    x = DATA[DATA.index(',') + 1:].lstrip()
    mm=str(int(x[x.index(' '):len(x)], 10))
    try:
        if  len(x)<=8:
            x = DATA[DATA.index(',') + 1:DATA.index('.')].lstrip() + ' ' + mm + ' ' + '2022'
            time_format = datetime.datetime.strptime(x, '%b %d %Y')
        else:
             time_format = datetime.datetime.strptime(x, '%B %dth %Y')
    except:
        try:
            time_format = datetime.datetime.strptime(x, '%B %dst %Y')
        except:
            try:
                time_format = datetime.datetime.strptime(x, '%B %dnd %Y')
            except:
               try:
                time_format = datetime.datetime.strptime(x, '%B %drd %Y')
               except:
                   time_format = datetime.datetime.strptime(x, '%b %d %Y')
    return time_format


sentioncontent = []
sentionoutput = []
collection = []
tip=[]
collectionmarket = {}
def getminusday(y, m, d, y1, m1, d1):
    the_date = datetime.datetime(y, m, d)
    after_date = datetime.datetime(y1, m1, d1)
    result_date = (the_date - after_date).days

    return result_date
def getday(y,m,d,n):
   the_date = datetime.datetime(y,m,d)
   result_date = the_date - datetime.timedelta(days=n)
   d   = result_date.strftime('%Y-%m-%d')
   return d

def day1(year1,month1,day1):

  time.sleep(10)
  WebDriverWait(browser, 180).until(
      EC.visibility_of_element_located((By.XPATH,
                                        "//div[@class='highcharts-container ']")))

  node = browser.find_element_by_xpath("//div[@class='highcharts-container ']")

  for i in range(1000):
      pyautogui.moveTo(1196- i, 300, duration=0.5)

      EC.visibility_of_element_located((By.XPATH,
                                        "//*[name()='svg']//*[name()='g'][9]//*[name()='text']"))
      hos = node.find_element_by_xpath("//*[name()='svg']//*[name()='g'][9]//*[name()='text']").text

      month = int(hos[0:2])
      day = int(hos[3:5])
      year = int(hos[6:10])
      if getminusday(year1, month1, day1, year, month, day)>=0:
          nnc = browser.find_elements_by_xpath(
              "//div[@data-test-id='charting-legend-badge-value']")
          t=nnc[0].text
          break

  return    t
def day(year1,month1,day1):

  time.sleep(10)


  gg = browser.find_element_by_css_selector(
      "div[data-test-id='about-symbol-chart']>ul>li:nth-child(8)>a").get_attribute('href')
  browser.get(gg)
  WebDriverWait(browser, 180).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR,
                                        "button[data-test-id='charting-intervals-fiveYear']")))
  yy = browser.find_element_by_css_selector(
      "button[data-test-id='charting-intervals-fiveYear']")
  browser.execute_script("arguments[0].click();", yy)
  scroll_to_bottom(browser)
  time.sleep(10)

  WebDriverWait(browser, 180).until(
      EC.visibility_of_element_located((By.XPATH,
                                        "//div[@class='highcharts-container ']")))

  node = browser.find_element_by_xpath("//div[@class='highcharts-root']")
  for i in range(1000):
    pyautogui.moveTo(1196 - i, 300, duration=0.5)
    try:
      EC.visibility_of_element_located((By.XPATH,
                                        "//*[name()='svg']//*[name()='g'][9]//*[name()='text']"))
      hos = node.find_element_by_xpath("//*[name()='svg']//*[name()='g'][9]//*[name()='text']").text

      month = int(hos[0:2])
      day = int(hos[3:5])
      year = int(hos[6:10])

      if getminusday(year, month, day, year1, month1, day1) >= 8:
          continue
      elif getminusday(year, month, day, year1, month1, day1) == 7:
          nnc = browser.find_elements_by_xpath("//div[@data-test-id='charting-legend-badge-value']")
          t = nnc[0].text
          break
      elif getminusday(year, month, day, year1, month1, day1) < 7:
          tiwen = 1196 - i
          for j in range(1, 1000):
              pyautogui.moveTo(tiwen + 2 * j, 300, duration=0.5)
              EC.visibility_of_element_located((By.XPATH,
                                                "//*[name()='svg']//*[name()='g'][9]//*[name()='text']"))
              hos = node.find_element_by_xpath(
                  "//*[name()='svg']//*[name()='g'][9]//*[name()='text']").text

              months = int(hos[0:2])
              days = int(hos[3:5])
              years = int(hos[6:10])
              if getminusday(years, months, days, year1, month1, day1) >= 7:
                  nnc = browser.find_elements_by_xpath(
                      "//div[@data-test-id='charting-legend-badge-value']")
                  t = nnc[0].text
                  break
          break
    except: continue
  return t


sentencevalue=0
sentiment=''
#Total sentimental value of sentences
def  SumOfSentiment(text,sentiment):
    sentencevalue = 0
    switch = 0
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.lower().split()

    for index in range(len(words)):

        try:
            words[index] = wnl.lemmatize(words[index])
        except:
            continue
    for word in words:
        for temp in dict_one_to_more:
            if word == temp:
                if   sentiment == 'Buy':
                     switch = float(dict_one_to_more[temp][2] / 100)
                     sentencevalue += float(dict_one_to_more[temp][0] * switch)
                if   sentiment == 'Sell':
                     switch = float(dict_one_to_more[temp][1] / 100)
                     sentencevalue += float(dict_one_to_more[temp][0] * switch)

                if   sentiment == 'Hold':
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
#Web page drop-down function
def scroll_to_bottom(driver):
    js = "return action=document.body.scrollHeight"
    #
    height = 0

    new_height = driver.execute_script(js)

    while height < new_height:
        #
        for i in range(height, new_height, 2):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
        time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = driver.execute_script(js)

l1=[]
l2=[]
l3=[]
l4=[]
over='false'
import csv
outputsum=[]
sentencevaluelist=[]   #Sentimental value list of Comments

def countSegments(self, s):
    """
    :type s: str
    :rtype: int
    """
    return len(s.split(" "))


mainWindow = browser.current_window_handle
height = 0
#
sentioncontent = []
sentionoutput = []
collection = []
tip=[]
collectionmarket = {}

x = browser.find_elements_by_css_selector("div[data-test-id='post-list']>article")
collection=[]
collectionmarket = {}

for i in range(1, len(x)):
        WebDriverWait(browser, 180).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "div[data-test-id='post-list']>article:nth-child(%s)>div>div>h3>a" % i)))

        uu = browser.find_element_by_css_selector(
            "div[data-test-id='post-list']>article:nth-child(%s)>div>div>h3>a" % i)
        tempcharacter = str(uu.get_attribute("href"))
        collection.append(tempcharacter)
        try:

            uu = browser.find_element_by_css_selector(
                "div[data-test-id='post-list']>article:nth-child(%s)>div>div>footer>span" % i)
            collectionmarket[tempcharacter] = uu.text
        except:
            continue
insertvalue = 'doubt'
hh=len(collection)
CONLL=[]
insertvalue = 'doubt'
price=[]

minus=0

positive=0

truepositive=0
datatogether1=[]        #Issue date of stock comments
result=[]
sectiontitle1=[]        #Title of stock comments
insertvalueinter1=[]     #Investment strategies given by stock comments
minus1=[]
positive1=[]
truepositive1=[]
fd1=[]
StockDifferent=[]   # List of real stock price difference
A = 'doubt'
B = 'doubt'
C = 'doubt'
D = 'doubt'
E = 'doubt'
F = 'doubt'
for j in range(1, len(collection)):

    over = 'false'
    for k, v in collectionmarket.items():
        if k is collection[j]:
            insertvalue = v
            break
    browser.switch_to_window(browser.current_window_handle)
    Crhandle = browser.current_window_handle

    today = datetime.date.today()

    time_format = datetime.datetime.strptime(str(today), '%Y-%m-%d')
    if insertvalue is 'doubt' or  'Yesterday' in insertvalue or 'Today' in insertvalue:
        continue
    else:

        try:
            browser.get(collection[j])
            if (ElementExist.isElementExist(browser, '//h2[@data-test-id="article-summary-title"]') is False):
                continue
            WebDriverWait(browser, 180).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(1)")))
            A = browser.find_element_by_css_selector(
                "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(1)")
            B = browser.find_element_by_css_selector(
                "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(2)")

            C = browser.find_element_by_css_selector(
                "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(3)")
            D = browser.find_element_by_css_selector(
                "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(4)")
            if 'Looking for a helping hand in the market?' in D.text:
                D = 'doubt'
            E = browser.find_element_by_css_selector(
                "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(5)")
            if 'Looking for a helping hand in the market?' in E.text:
                E = 'doubt'
            F = browser.find_element_by_css_selector(
                "section[data-test-id='card-container']>div>div>div>ul>li:nth-child(6)")
            if 'Looking for a helping hand in the market?' in F.text:
                F = 'doubt'
        except:
            try:
                  key=0
                  WebDriverWait(browser, 180).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "section[data-test-id='about-article-card']>div>div:nth-child(2)>div>div:nth-child(2)>div:nth-child(2)>div>a>span>span")))

                  insertvalueinter=browser.find_element_by_css_selector(
                      "section[data-test-id='about-article-card']>div>div:nth-child(2)>div>div:nth-child(2)>div:nth-child(2)>div>a>span>span").text
                  aim1 = browser.find_element_by_css_selector(
                      "section[data-test-id='about-article-card']>div>div:nth-child(2)>div>div:nth-child(3)>div:nth-child(2)>div").text

                  if insertvalueinter == 'Strong Buy':
                    insertvalueinter='Buy'
                  if insertvalueinter == 'Strong Sell':
                    insertvalueinter='Sell'

            except:


                      continue

            div = browser.find_element_by_css_selector("h1[data-test-id='post-title']")
            sectiontitle = div.text
            browser.execute_script(
                    "window.scrollTo(0, 400); var lenOfPage=document.body.scrollHeight; return lenOfPage;")

            fd=''
            DATA = insertvalue
            if (A is not 'doubt') & (over == 'false'):
                outputsum.append(SumOfSentiment(A.text, insertvalueinter))
            if (B is not 'doubt') & (over == 'false'):
                outputsum.append(SumOfSentiment(B.text, insertvalueinter))
            if (C is not 'doubt') & (over == 'false'):
                outputsum.append(SumOfSentiment(C.text, insertvalueinter))
            if (D is not 'doubt') & (over == 'false'):
                if 'Looking for a helping hand in the market?' not in D.text:
                    outputsum.append(SumOfSentiment(D.text, insertvalueinter))
            if (E is not 'doubt') & (over == 'false'):
                if 'Looking for a helping hand in the market?' not in E.text:
                    outputsum.append(SumOfSentiment(E.text, insertvalueinter))
            if (F is not 'doubt') & (over == 'false'):
                if 'Looking for a helping hand in the market?' not in F.text:
                    outputsum.append(SumOfSentiment(F.text, insertvalueinter))
            else :
                WebDriverWait(browser, 180).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "//div[@class='highcharts-tooltip-container']")))
                time.sleep(10)
                node1 = browser.find_element_by_xpath("//div[@class='highcharts-tooltip-container']")

                time.sleep(10)

                WebDriverWait(browser, 180).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "//*[name()='svg']//*[name()='g']//*[name()='text']//*[name()='tspan'][7]")))

                ll = divide(insertvalue)
                month = int(ll.month)
                day = int(ll.day)
                year = int(ll.year)
                xi,yi=pyautogui.position()

                for i in range(1000):
                        pyautogui.moveTo(xi+i, yi, duration=0.5)
                        try:

                            node12 = browser.find_element_by_xpath("//div[@class='highcharts-container ']")
                            hos2 = node12.find_element_by_xpath(
                                "//*[name()='svg']//*[name()='g']//*[name()='text']//*[name()='tspan'][1]").text
                            month1 = int(hos2[0:2])
                            day1 = int(hos2[3:5])
                            year1 = int(hos2[6:10])
                            if getminusday(year1, month1, day1, year, month, day) < 7:
                                continue
                            elif getminusday(year1, month1, day1, year, month, day) >= 7:
                                aim2 = node12.find_element_by_xpath(
                                    "//*[name()='svg']//*[name()='g']//*[name()='text']//*[name()='tspan'][4]").text
                                hos2 = node12.find_element_by_xpath(
                                    "//*[name()='svg']//*[name()='g']//*[name()='text']//*[name()='tspan'][1]").text
                                break

                        except:
                            continue


                datatogether = hos2
                sel = aim1
                sel1 = aim2
                for i in range(0, len(outputsum)):
                    if outputsum[i] == -1:
                        minus = minus + 1

                    if outputsum[i] == 0:
                        positive = positive + 1

                    if outputsum[i] == 1:
                        truepositive = truepositive + 1

                if (minus >= positive and minus >= truepositive):
                    if minus == positive or minus == truepositive:
                                  sentencevaluelist.append('0')

                    if (minus > positive and minus > truepositive):

                        sentencevaluelist.append(-minus/len(outputsum))

                elif (positive >= minus and positive >= truepositive):
                    if minus == positive or positive == truepositive:
                                  sentencevaluelist.append('0')

                    if (positive > minus and positive > truepositive):
                        sentencevaluelist.append('0')

                else:
                    if minus == truepositive or positive == truepositive:
                                  sentencevaluelist.append('0')

                    if (truepositive > minus and truepositive > positive):
                        sentencevaluelist.append(truepositive/len(outputsum))
                # Find the difference between the stock price on the day of the news release and the stock price seven days later
                different = float(sel1.strip('%'))-float(sel.strip('%').strip('$'))

                value = ''
                insertvalue = 'doubt'
                #Save result to CSV file
                Fname = 'C:\\Users\Administrator\Desktop\\' + 'RENN1' + '.csv'
                datatogether1.append(datatogether)
                sectiontitle1.append(sectiontitle)
                insertvalueinter1.append(insertvalueinter)
                StockDifferent.append(different)
                minus = 0
                positive = 0
                outputsum=[]
                truepositive = 0
                csvfile = open(Fname, 'wt', encoding="UTF-8")
                csvfile.truncate()
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerows(
                    zip(datatogether1, sectiontitle1, insertvalueinter1, sentencevaluelist, StockDifferent))
                csvfile.close()

                over = 'true'

browser.quit()
