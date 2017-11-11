print("pouet")


CHARACTER_SET_INITIAL = 'abcdefghijklmnopqrstuvwxyw ABCDEFGHIJKLMNOPQRSTUVWXYW-'

def apply_key(message, key, direct_sense):
	message_indexes = [ cipher_index_from_char[char] for char in message_clear ]
	nb_repeat_key = len(message) // len(key) + 1
	repeated_key = key * nb_repeat_key
	sense_factor = { True: 1, False: -1 }[direct_sense]
	char_set_len = len(character_set)
	message_offsetted = [
		(index + key_elem*sense_factor) % char_set_len
		for index, key_elem
		in zip(message_indexes, repeated_key)
	]
	message_result = [ cipher_char_from_index[index] for index in message_offsetted ]
	message_result = ''.join(message_result)
	return message_result


message_clear = 'The quick brown duck duct-taped the ape'


key = (4, 7, 5, 1, 2)


character_set = CHARACTER_SET_INITIAL

cipher_index_from_char = {
	char: index
	for index, char
	in enumerate(character_set)
}

cipher_char_from_index = list(character_set)

print(cipher_index_from_char)

print(message_clear)

print(apply_key(message_clear, key, True))

