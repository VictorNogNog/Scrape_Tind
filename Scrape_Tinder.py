import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from numpy.random import normal
import numpy as np
import os
import requests
import cv2
import re
import glob2 as glob
import pandas as pd
from bs4 import BeautifulSoup as BS

cwd = os.getcwd()
noise = normal(2.0, 1.5,1)
sleep_val = 2+noise
small_noise = normal(1.0, 0.65,1)
micro_sleep = 0.35
small_sleep = 1 +small_noise
path = r"C:\webdrivers\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(path, options=chrome_options)

pers_pass = 'ENTER_PASS_HERE'
pers_mail = 'ENTER_MAIL_HERE'

uni_words = ['university', 'bachelor\'s', 'ba', 'ms', 'phd', 'ph.d', 'major', 'postgraduate', 'postgrad', 'grad',
				 'degree', 'college', 'academy', 'institution', 'school']


def remove_dups (seq):
	seen = set ()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add (x))]


class Tinder ():
	
	def __init__ (self):
		self.driver = webdriver.Chrome (path, options = chrome_options)
		self.txt_data = dict ()
		self.img_data = []
		self.bs = BS ()
	
	def login (self):
		self.driver.get (
				  'https://www.facebook.com/'
		)
		email = self.driver.find_element_by_id ('email')
		email.send_keys (pers_mail)
		pw = self.driver.find_element_by_id ('pass')
		pw.send_keys (pers_pass)
		logbut = self.driver.find_element_by_id ('loginbutton')
		logbut.click ()
		self.driver.get (
				  'http://tinder.com'
		)
		
		# Wait for the facebook log in button
		time.sleep (2)
		self.driver.find_element_by_xpath (
				  "//*[@id=\"modal-manager\"]/div/div/div[2]/div/div[3]/div[2]/button/span"
		).click ();
		
		# Wait for Tinder to load
		time.sleep (2.5)
		
		return print ('Successfully logged onto Tinder')
	
	def tutorial (self):
		self.driver.find_element_by_xpath (
				  "//*[@id='content']/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div"
		).click ()
		
		self.driver.find_element_by_xpath (
				  "//*[@id='content']/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1] "
		).click ()
		return print ("Clicked Through Tutorial")
	
	def right_swipe (self):
		actions = ActionChains (self.driver)
		time.sleep (sleep_val)
		actions.send_keys (Keys.ARROW_RIGHT).perform ()
		return print ("Succesful right sweep")
	
	def left_Swipe (self):
		actions = ActionChains (self.driver)
		actions.send_keys (Keys.ARROW_LEFT).perform ()
		time.sleep (sleep_val)
	
	def get_data (self):
		time.sleep (sleep_val)
		this_list = []
		that_list = []
		for a in self.driver.find_elements_by_xpath (
				  './/*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div'):
			for x in range (10):
				time.sleep (0.05)
				b = a.get_attribute ("innerHTML")
				that_list.append (b)
				this_list.append (b.split ("url(&quot;") [1].split ("&quot;);") [0])
				self.driver.key_down (Keys.SPACE).key_up (Keys.SPACE)
		self.img_data = remove_dups (this_list)
		actions = ActionChains (self.driver)
		time.sleep (small_sleep)
		actions.send_keys (Keys.ARROW_UP).perform ()
		
		age = self.driver.find_element_by_xpath (
			"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/span").text;
		
		# Get Prof info
		try:
			elem1 = self.driver.find_element_by_xpath (
				"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]").text;
		except NoSuchElementException:
			elem1 = 'N/A'
		try:
			elem2 = self.driver.find_element_by_xpath (
				"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]").text;
		except NoSuchElementException:
			elem2 = 'N/A'
		
		try:
			elem3 = self.driver.find_element_by_xpath (
				"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]").text;
		except NoSuchElementException:
			elem3 = 'N/A'
		name = self.driver.find_element_by_xpath (
			"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/span").text;
		try:
			song = self.driver.find_element_by_xpath (
				"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div[1]").text;
		except NoSuchElementException:
			song = 0
		try:
			profile_txt = self.driver.find_element_by_xpath (
				"//*[@id=\"content\"]/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div").text;
		except NoSuchElementException:
			profile_txt = 0
		# Complicated ass parsing, since Tinder won't give us consistent X paths.
		elem_coll = [str.lower (x) for x in list ((elem1, elem2, elem3))]
		elem1, elem2, elem3 = str.lower (elem1), str.lower (elem2), str.lower (elem3)
		elem_coll = [elem1] + [elem2] + [elem3]
		dist_filt = (dist_elem for dist_elem in elem_coll if 'miles' in dist_elem)
		dist = next (dist_filt)
		uni_filt = (uni_elem for uni_elem in elem_coll if any (s in uni_elem for s in uni_words))
		try:
			uni = next (uni_filt)
		except StopIteration:
			uni = 0
		if len (elem_coll) == 3 and \
				  uni != 0 and \
				  dist != 0:
			job = list (set (elem_coll) - set ([uni, dist])) [0]
		else:
			job = 0
		int_dist = re.sub ("[^0-9]", "", dist)
		list_of_values = [str (job), str (uni), str (int_dist), str (name)]
		list_of_keys = ['job', 'uni', 'dist', 'name']
		self.txt_data = dict (zip (list_of_keys, list_of_values))
		self.bs = BS (self.driver.page_source, 'lxml')
		return print (
			"USER DATA \n--------------------------\n Age:  {}\n Name:  {}\n Occupation:  {}\n University Info:  {}\n Distance:  {}\n Song  {}:\n Profile text\n {}".format (
				age, name, job, uni, dist, song, profile_txt))
	
bb = Tinder ()
bb.login ()
bb.tutorial ()
BS (bb.driver.page_source, 'html5lib').find ('div', attrs = {'class': "react-swipeable-view-container"})