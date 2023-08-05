import json


class Caeser_cipher:

	def encoded_alphabet(self, user, shift=int):
		"""this function creates a alphabet dictionary
		and change the order of the alphabet dictionary depending on what the user type in the terminal.
		the function doesn't need a list"""
		string = ''
		string += user
		alpha = {}
		list0 = []
		for chars in string:
			list0.append(chars)
			if ' ' in list0:
				list0.remove(' ')

			else:
				list0 = list(set(list0))
				list0.sort()
		# in the line 24 changes the order by the shift
		############ starts in ######## ends in ###################
		shifted = list0[shift:] + list0[:shift]

		for index in range(len(shifted)):
			alpha[shifted[index]] = list0[index]
		return alpha

	def save_alpha(self, alpha=dict):
		""" after the alphabet dictionary have been created,
		you add the alphabet dictionary as a argument and it saves the
		alphabet dictionary in a json file"""
		file = 'alphabet.json'
		with open(file, 'w') as f:
			save = json.dump(alpha, f)
			return save


	def use_saved_alpha(self, file=None):
		"""this function what actually do is.. use the alphabet dictionary
		of a json file, you can put a json file in the argument file
		that have a dictionary saved"""
		if file:
			with open(file, 'r') as f:
				load = json.load(f)
				return load
		else:
			# as default this function already have a json file
			jfile = 'alphabet.json'
			with open(jfile, 'r') as f:
				load = json.load(f)
				return load


	def encode(self, txt=str, alpha=dict):
		""" the encode function takes the users message and encode character by character
		by adding a alphabet dictionary"""
		text = ''
		for chars in txt:
			if chars not in alpha.keys():
				text = text + chars
			else:
				text = text + alpha[chars]
		return str(text.strip())


	def decode(self, txt=str, reversed_alpha=dict):
		""" this function does the fun and confusing part.
		the decode function reverse the alphabet dictionary and then
		replace those characters to the original order"""
		string = ""
		# this is how i reversed the alphabet dictionary
		##########################################################
		reversed_alpha = {v: k for k, v in reversed_alpha.items()}
		##########################################################
		for chars in txt:
			if chars not in reversed_alpha.keys():
				string = string + chars
			else:
				string = string + reversed_alpha[chars]
		return str(string.strip())

	def cipher(self, txt=str, shift=int, encode_txt=False):
		"""this is a function that decodes and encode messages
		is a combination of 'encode' and 'decode' functions"""
		if encode_txt == False:
			text = ''
			chars = []
			alpha = {}
			for char in txt:
				chars.append(char)

				if ' ' in chars:
					chars.remove(' ')

				else:
					chars = list(set(chars))
					chars.sort()

			shifted = chars[shift:] + chars[:shift]
			for index in range(len(shifted)):
				alpha[chars[index]] = shifted[index]

			for characters in txt:
				if characters not in alpha.keys():
					text = text + characters
				else:
					text = text + alpha[characters]

			return text
		elif encode_txt == True:

			text = ''
			chars = []
			alpha = {}
			for char in txt:
				chars.append(char)

				if ' ' in chars:
					chars.remove(' ')

				else:
					chars = list(set(chars))
					chars.sort()

			shifted = chars[shift:] + chars[:shift]
			for index in range(len(shifted)):
				alpha[shifted[index]] = chars[index]

			for characters in txt:
				if characters not in alpha.keys():
					text = text + characters
				else:
					text = text + alpha[characters]

			return text


""" NOTE """
"""
# Dictionary is important for this package, if you want to use your own dictionary
# make sure to add 26 key-value pairs just in case the program doesn't crash

# to understand this code better, just remember that to encode a message you must sort
# the characters in the values of the dictionary in alphabetical order; {'c':#'a', 'e':#'b', g:#'c'} and so on
# to decode the message just reverse the dictionary, the characters in the keys of the dictionary must be sorted
# in alphabetical order
"""