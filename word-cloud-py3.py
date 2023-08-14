#!/usr/bin/env python -OO
# -*- coding: ascii -*-

import numpy as np
import matplotlib.pyplot as plt
from os import path
import sqlite3
import os
import re

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

def main():
	keyword = input("Provide a Jeopardy answer for a clue map!\n")
	write_text_output_for_clue(keyword)
	create_word_cloud_for_clue(keyword)

def write_text_output_for_clue(keyword):

	db = sqlite3.connect('clues.db')
	cursor = db.cursor()
	clue_output = cursor.execute("""
		SELECT clue, answer
	 FROM clues 
	 JOIN documents ON clues.id = documents.id
	 WHERE answer LIKE '%{}%';
	 """.format(keyword))

	outfile = open("{}.txt".format(keyword), "w")
	for row in clue_output:
		row = str(row)
		outfile.write("\n%s\n" % row)
	outfile.close()

def create_word_cloud_for_clue(keyword):
	stopwords = set(STOPWORDS)
	stopwords.add(keyword)

	text = open(path.join(d, "{}.txt".format(keyword))).read()

	#text pre-processing

	text = text.replace("u'", "")
	text = text.replace("'", "")
	text = re.sub(r"\b[a-zA-Z]\b", "", text) #all single chars

	wc = WordCloud(max_words=1000, stopwords=stopwords, margin=10,
               random_state=1).generate(text)
	
	default_colors = wc.to_array()
	plt.title("{}".format(keyword))
	plt.imshow(wc, interpolation="bilinear")
	wc.to_file("{}.png".format(keyword))
	plt.axis("off")
	plt.show()


main()
