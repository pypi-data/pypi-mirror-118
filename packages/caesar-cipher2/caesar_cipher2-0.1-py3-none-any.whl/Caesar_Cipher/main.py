from __init__ import Caeser_cipher

while True:

	cipher = Caeser_cipher()
	try:
		shift = int(input('shift: '))
		message = input('message: ')
	except:
		continue

	alpha = cipher.encoded_alphabet(user=message, shift=shift)
	saved_alpha = cipher.save_alpha(alpha=alpha)
	load_alpha = cipher.use_saved_alpha()
	text = cipher.encode(txt=message, alpha=load_alpha)
	reveal = cipher.decode(txt=text, reversed_alpha=alpha)
	decode_txt = cipher.cipher(txt=message, shift=7)
	print(text)
	print(reveal)
	print(load_alpha)
	print(decode_txt)