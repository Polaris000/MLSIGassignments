import html.parser
import re
import wordninja

class Tweet():

	def __init__(self, line):
		self.line_raw = line


	def get_id(self):
		
		self.line = "".join(self.line_raw).split("\t")
		self.id = self.line[0][:-1]

		return self.id.strip()


	def get_text(self):
		
		self.line = "".join(self.line_raw).split("\t")
		self.text = self.line[1]

		return self.text.strip()

	def get_emotion(self):
		
		self.line = "".join(self.line_raw).split("\t")
		self.emotion = self.line[2][3:]

		return self.emotion.strip()

	

	def clean_text(self, phrase):

		#convert &quot -> '"', etc..
		html_parser = html.parser.HTMLParser()
		html_cleaned_phrase = html_parser.unescape(phrase)

		# removing special characters and a few emoticons
		special_char_cleaned = ' '.join(re.sub("[/)<>☑☺❤♥✽•¨✽*(&:-]", "", html_cleaned_phrase).split())

		#removing multiple spaces
		special_char_cleaned = ' '.join(re.sub("  " , " ", special_char_cleaned).split())

		#change .... -> ., ???? -> ?, !!!! -> !
		special_char_cleaned = ' '.join(re.sub("[.]+" , ".", special_char_cleaned).split())
		special_char_cleaned = ' '.join(re.sub("[?]+" , "?", special_char_cleaned).split()) 
		special_char_cleaned = ' '.join(re.sub("[!]+" , "!", special_char_cleaned).split()) 

		#removing unnecessary $ symbols, but keeping them in such cases: $300, $ 230, etc.
		special_char_cleaned = ' '.join(re.sub("([a-zA-Z]*[$]) | [$][^0-9]+" , "", special_char_cleaned).split())  

		
		def caps_clean(match):
			return match.group(0).lower()

		#make unnecessary CAPS terms to lowercase
		caps_cleaned = ' '.join(re.sub("[A-HJ-Z]+", caps_clean, special_char_cleaned).split())


		#change @lkdsfj -> *NAME*
		name_cleaned = ' '.join(re.sub("(@([0-9A-Za-z_]+))", "*NAME*", caps_cleaned).split())
		name_cleaned = ' '.join(re.sub(" rt ", "", name_cleaned).split())

		# empty list to hold the separated words as elements
		word_split_list = []
		
		def split_hashed_words(phrase):

			for i in phrase.split():
				if '#' in i:
					i = " ".join(wordninja.split(i))

				word_split_list.append(i)
			return " ".join(word_split_list)


		word_split = split_hashed_words(name_cleaned)

		# making the @ to "at"
		word_split = ' '.join(re.sub("@", "at", word_split).split()) 
		
		return word_split

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||	


if __name__ == "__main__":
	with open("jan9-2012.txt", "r") as f:
		with open("final_cleaned_data.csv", "w") as w:
			
			for line in f:
				t = Tweet(line)

				w.write(t.get_id() + "|" + t.clean_text(t.get_text()) + "|" + t.get_emotion() + '\n')
			
			