### 1. Scrapeing youtube comments

import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

import csv
from transformers import pipeline

import numpy as np
from wordcloud import WordCloud,STOPWORDS
from matplotlib import pyplot as plt


def scrape():

    print('Scapeing Youtube Comments Started.....')
    start = time.time()
    
    url = input()   # https://www.youtube.com/watch?v=2NsTBdqYtp0

    # specify the path to chromedriver.exe (download and install from https://chromedriver.chromium.org/downloads)
    service = Service("C:/Windows/chromedriver_win32/chromedriver.exe")

    # open the YouTube video in Chrome
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # scroll down to load more comments
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # extract all comments
    comments = driver.find_elements("xpath", '//*[@id="content-text"]')
    comment_list = [comment.text for comment in comments]

    # save the comments to a CSV file
    with open("comments.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Comment"])
        for comment in comment_list:
            writer.writerow([comment])

    # wait for 10 seconds before closing the browser window
    time.sleep(10)
    print('Step-1 Scraping Youtube Comments Completed')
    end = time.time()

    elapsed_time1 = end - start
    print('Time Elapsed',elapsed_time1,'seconds')

    # close the browser window
    driver.close()    # 2.24min for reading 1482 comments

def sentiment_analysis():

    print('Sentiment Analysis of Youtube Comments started.....')

    start = time.time()

    # load the BERT sentiment analysis model
    model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment",truncation=True,max_length=512)
    # model = pipeline("text-classification", model="roberta-large-mnli")

    # open the CSV file and read the comments
    with open("comments.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        comments = [row["Comment"] for row in reader]

    # perform sentiment analysis on the comments
    results = model(comments)

    # write the sentiment analysis results to a new CSV file
    with open("sentiment_analysis_results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Comment", "sentiment"])
        for i in range(len(results)):
            writer.writerow([comments[i], results[i]["label"]])

    print("Step-2 Sentiment analysis complete.")    # 1.40min for analysis
    end = time.time()

    elapsed_time2 = end - start
    print('Time Elapsed',elapsed_time2,'seconds')

def comments_wordcloud():

    print('Comments WordCloud in Progress.....')

    start = time.time()

 # Load the comments from the CSV file
    comments = []
    with open('comments.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comments.append(row['Comment'])

    # Join all comments into a single string
    text = ' '.join(comments)

    # Generate the word cloud image
    wordcloud = WordCloud(width=1500, height=1000, background_color='salmon', max_words=1000,stopwords=STOPWORDS,
                        contour_width=3, contour_color='steelblue', collocations=False).generate(text)
    
    print('Comments WordCloud is ready to show')

    # Display the word cloud image
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('Comments_wordcloud.png')
    # plt.show()

    end = time.time()

    elapsed_time3 = end - start
    print('Time Elapsed',elapsed_time3,'seconds')


### new code
# using sentiment_analysis_results.csv file if sentiment is greater than equal to 3 stars then it is positive else negative ,
# write two separate files for positive and negative sentiment comments and form wordcloud using each file

## using sentiment_analysis_result.csv file, classify the sentiments into positive and negative and then make their wordcloud separately

def positive_negative_wordcloud():

    print('WordCloud for Positive and Negative sentiment started.....')

    start = time.time()

    # Define the file path
    sentiment_file = 'sentiment_analysis_results.csv'

    # Define the tag cloud configuration
    max_words = 100

    # Load the comments and their sentiment scores from the CSV file
    positive_comments = []
    negative_comments = []
    with open(sentiment_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['Comment']
            sentiment_score = float(row['sentiment'].replace('stars','').replace('star',''))
            if sentiment_score >= 3:
                positive_comments.append(comment)
            else:
                negative_comments.append(comment)

    # Write positive comments to a file
    with open('positive_comments.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment'])
        for comment in positive_comments:
            writer.writerow([comment])

    # Write negative comments to a file
    with open('negative_comments.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment'])
        for comment in negative_comments:
            writer.writerow([comment])

    # Load the comments from the CSV file
    positive = []
    with open('positive_comments.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            positive.append(row['Comment'])
    # Join all comments into a single string
    text1 = ' '.join(positive)

    # Generate the word cloud image
    positive_wordcloud = WordCloud(width=800, height=500, background_color='black', max_words=1000,stopwords=STOPWORDS,
                        contour_width=3, contour_color='steelblue', collocations=False).generate(text1)
    
    # plt.show('postive wordcloud',positive_wordcloud)

    plt.imshow(positive_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('positive_wordcloud.png')


    # Load the comments from the CSV file
    negative = []
    with open('negative_comments.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            negative.append(row['Comment'])
    # Join all comments into a single string
    text2 = ' '.join(negative)

    # Generate the word cloud image
    negative_wordcloud = WordCloud(width=800, height=500, background_color='salmon', max_words=1000,stopwords=STOPWORDS,
                        contour_width=3, contour_color='steelblue', collocations=False).generate(text2)
    
    # plt.show('negative wordcloud',negative_wordcloud)

    plt.imshow(negative_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('negative_wordcloud.png')

    print('WordCloud for Positive and Negative sentiment is ready to show.....')

    end = time.time()

    elapsed_time4 = end - start
    print('Time Elapsed',elapsed_time4,'seconds')






scrape()
sentiment_analysis()
comments_wordcloud()
positive_negative_wordcloud()

