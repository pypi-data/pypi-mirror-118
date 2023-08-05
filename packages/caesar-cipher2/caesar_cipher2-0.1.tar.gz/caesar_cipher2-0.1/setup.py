import setuptools
description0 = 'this package can be used to make app to chat with someone with secrets messages' \
			   'or send secrets messages to someone\'s number or email, hope u can have more ideas.' \
			   'this cipher can decode symbols and numbers'
setuptools.setup(name='caesar_cipher2',
				 version="0.1",
				 author="Lennix Robles",
				 author_email="ocho.contact.08@gmail.com",
				 description=description0,
				 license="MIT",
				 url='https://pypi.org/project/caesar_cipher2',
				 packages= setuptools.find_packages(),
				 classifiers=['Programming Language :: Python',
       						  'Programming Language :: Python :: 3.9']
				 )
