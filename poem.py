import os
import re
import json
import random

from pypinyin import pinyin
from zhconv import convert

MAX_SENTENCE = 9
SIMPLE_CONV = True

dataset = {
	'shi':"json",
	'ci':"ci",
}

shi_dir = "./shi"
ci_dir = "./ci"
RE_SEP = r"，|。|、|；|？|\,|\.|\?|\;"


class PoemProcessor():
	def __init__(self,sentence):
		self.sentence = sentence
  
	def first_letter_all_match(self,letters):
		index = 0
		yin_index = 0
		words = ""
		for each in pinyin(self.sentence):
			yin = each[0][0]
			if letters[yin_index] == yin:
				yin_index += 1
				words += (self.sentence[index])
			if yin_index == 3:
				return words
			index += 1
	
	def last_name_in_poem(self,last_name):
		if last_name in self.sentence:
			first_name = self.sentence.split(last_name)[1]
			if len(first_name) >= 2:
				return last_name+first_name[:2]


class Output():
	def __init__(self,final_result):
		self.final_result = final_result
  
	def print_cli(self):
		for poem in self.final_result:
			paras,title,poet = poem
			print("《{}》- {}".format(title,poet))
			for para in paras:
				print(para)
			print()

	def print_file(self,filename):
		write_str = ""
		for poem in self.final_result:
			paras,title,poet = poem
			write_str += "《{}》- {}\n".format(title,poet)
			for para in paras:
				write_str += (para[0]+" "+para[1]+"\n")
			write_str += "\n"
			with open(filename,"w+") as file:
				file.write(write_str)

	def get_web_string(self):
		write_str = ""
		for poem in self.final_result:
			paras,title,poet = poem
			write_str += "《{}》- {}\n".format(title,poet)
			for para in paras:
				write_str += (para[0]+" "+para[1]+"\n")
			write_str += "\n"
		
		return write_str.replace("\n","<br>")
			
def process_sentence(sentence,method,args):
    
	if SIMPLE_CONV:
		sentence = convert(sentence, 'zh-hans')
  
	result = getattr(PoemProcessor(sentence),method)(*args)
	if result is not None:
		return [sentence,result]
	else:
	 	return None

# return: [["xxx","xxxxx"],["yyy","yyyyy"]]
def process_article(article,method,args):
	result = []
	try:	
		title = article['rhythmic']
	except KeyError:
		title = article['title']
	paras = article['paragraphs']
	author = article['author']
 
	if SIMPLE_CONV:
		title = convert(title, 'zh-hans')
		author = convert(author, 'zh-hans')

	for long_sentence in paras:
		sentences = re.split(RE_SEP,long_sentence)
		for sentence in sentences:
			if len(sentence) > MAX_SENTENCE:
				continue
			temp_result = process_sentence(sentence,method,args)
			if temp_result is not None:
				result.append(temp_result)
	if len(result) > 0:
		return [result,title,author]
	else:
		return None


def read_brief():
	articles = []
	articles1 = json.loads(open("ci/宋词三百首.json",'r').read())
	articles2 = json.loads(open("shi/唐诗三百首.json",'r').read())
	for k in articles1:
		articles.append(k)
	for k in articles2:
		articles.append(k)
	print("[+] 数据集中包含唐诗三百首和宋词三百首，{}诗词。".format(len(articles)))
	return articles

def read_all(tangshi=False,songshi=False,songci=False):
	articles = []
 # 唐诗
	if tangshi == True:
		for p,d,poem_files in os.walk(shi_dir):
			for poem_file in poem_files:
				if poem_file.startswith("poet.tang."):
					poems = json.loads(open(shi_dir + "/" + poem_file).read())
					for poem in poems:
						articles.append(poem)

# 宋诗
	if songshi == True:
		for p,d,poem_files in os.walk(shi_dir):
			for poem_file in poem_files:
				if poem_file.startswith("poet.song."):
					poems = json.loads(open(shi_dir + "/" + poem_file).read())
					for poem in poems:
						articles.append(poem)

# 宋词
	if songci == True:
		for p,d,poem_files in os.walk(ci_dir):
			for poem_file in poem_files:
				if poem_file.startswith("ci.song"):
					poems = json.loads(open(ci_dir + "/" + poem_file).read())
					for poem in poems:
						articles.append(poem)

	print("[+] 数据集中包含了{}首诗词。".format(len(articles)))
	return articles

def read_random(tangshi=False,songshi=False,songci=False,num=100):
	poets = read_all(tangshi,songshi,songci)
	if num > len(poets):
		print("[!] 数据集不够大，只有{}首诗词".format(len(poets)))
		num = len(poets)
	print("[+] 随机选取了{}首诗词".format(num))
	return random.sample(poets, num)

def start_task(method,args,dataset_type,dsargs=[]):
	final_result = []

	if dataset_type == "brief":
		poets = read_brief()
	elif dataset_type == "random":
		tangshi,songshi,songci=dsargs[0],dsargs[1],dsargs[2]
		num = dsargs[3]
		poets = read_random(tangshi,songshi,songci,num)
	elif dataset_type == "read_all":
		tangshi,songshi,songci=dsargs[0],dsargs[1],dsargs[2]
		poets = read_all(tangshi,songshi,songci)
	else:
		print("[!] dataset_type 输入错误")
		
	for poet in poets:
		result = process_article(poet,method,args)
		if result is not None:
			final_result.append(result)
	# print(final_result)
	return final_result


#result = start_task("first_letter_all_match",['ljm'],"random",[True,True,True,10000])
#result = start_task("first_letter_all_match",['gyj'],"brief")
# result = start_task("last_name_in_poem",["江"],"brief")
# result = start_task("last_name_in_poem",["江"],"random",[True,True,True,10000])

#Output(result).print_cli()
# result = start_task("first_letter_all_match",['ljm'],"read_all",[False,False,True])