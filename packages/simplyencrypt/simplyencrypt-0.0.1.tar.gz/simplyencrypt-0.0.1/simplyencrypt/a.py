
"""In this file encrypt and new_random_password is defined"""



import secrets

UTF_16 = 65_536
UTF_16_PLUS = UTF_16 + 1


def new_random_password(length: int) -> list:
	"""To create Random Password
	
	Secrets module is used to create random values.
	
	Parameters: 
	  "length": Length of the password to be generated.
	
	Return Value:
	 This function returns Random Password in the form of list.
	"""
	if length > 5120:
		raise Exception("Length cannot be more then 5120!!")

	random_values = []
	
	while length != len(random_values):
		random_values.append(secrets.randbelow(UTF_16_PLUS))
	
	key = []
	for c in random_values:
		key.append(c)
	
	return key


def encrypt(keys: list, data: str) -> "Cipher Text":
	
	if len(data) > len(keys):
		raise Exception("\
Length of string to be encrypted cannot be more than length of key.")
	
	length = len(keys)
	cipher_list = []
	count = 0
	
	for c in data:
		cipher_char = ord(c) - ord(keys[count])
		
		if cipher_char < 0:
			cipher_char *= (-1)
		
		count += 1
		cipher_list.append(cipher_char)
	cipher_text = ""
	for t in cipher_list:
		cipher_text += chr(t)
	
	return cipher_text


if __name__ == "__main__":
	print(help(__name__))
	"""
	ct = encrypt(new_random_password(1024), "Aಅ手ض")
	print(bytes(ct , "utf-16"))
	exit(0)
	"""
