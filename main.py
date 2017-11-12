print("pouet")


CHAR_GROUP_1 = 'aeiouyAEIOUY ' # voyelles
CHAR_GROUP_2 = 'ckqbdptvfCKQBDPTVF' # consonnes 1
CHAR_GROUP_3 = 'ghjlmnrswxzGHJLMNRSWXZ' # consonnes 2

# TODO : ajout tiret à l'arrache
CHAR_GROUPS = [ CHAR_GROUP_1 + '-', CHAR_GROUP_2, CHAR_GROUP_3 ]

CHARACTER_SET_INITIAL = ''.join(CHAR_GROUPS)


def which_group(char):
	for index_group, char_group in enumerate(CHAR_GROUPS):
		if char in char_group:
			return index_group
	raise Exception("Char not in any char_group. Not supposed to happend. char : " + char)


def cipher(message, key, character_set):

	index_from_char = {
		char: index
		for index, char
		in enumerate(character_set)
	}

	message_indexes = [ index_from_char[char] for char in message_clear ]
	nb_repeat_key = len(message) // len(key) + 1
	repeated_key = key * nb_repeat_key
	char_set_len = len(character_set)
	message_offsetted = [
		(index + key_elem) % char_set_len
		for index, key_elem
		in zip(message_indexes, repeated_key)
	]
	message_result = [ char_from_index[index] for index in message_offsetted ]
	message_result = ''.join(message_result)
	whiches_group = [ which_group(char) for char in message_clear ]
	return message_result, whiches_group


def try_decipher_char(char_ciphered, key_elem_correct, key_elem_proposed, char_groups, index_group_candidates):

	character_set = ''.join(char_groups)

	# TODO : Pas optimisé car on recalcule tout ça à chaque fois.
	index_from_char = {
		char: index
		for index, char
		in enumerate(character_set)
	}
	char_from_index = list(character_set)
	char_set_len = len(character_set)
	index_char_ciphered = index_from_char[char_ciphered]
	index_char_clear = (index_char_ciphered - key_elem_correct + char_set_len) % char_set_len
	char_clear = char_from_index[index_char_clear]

	if key_elem_correct == key_elem_proposed:
		return char_clear

	# La clé pour le caractère n'est pas la bonne. On redécale avec la clé proposée.
	# Mais on redécale dans le group de caractère restreint.
	# Ça renverra un caractère "pas si incorrecte que ça", au lieu de "totalement incorrect".

	group_candidates = [ char_groups[index_group] for index_group in index_group_candidates ]
	character_set_restricted = ''.join(group_candidates)
	char_set_len = len(character_set_restricted)
	try:
		index_char_clear = character_set_restricted.index(char_clear)
	except:
		print("Not supposed to happen. char_clear not in group_candidates. char_clear : " + char_clear + " char_groups : " + char_groups + " index_group_candidates : " + index_group_candidates)
		raise
	index_char_uncorrect = (index_char_clear + key_elem_correct - key_elem_proposed + char_set_len) % char_set_len
	char_uncorrect = character_set_restricted[index_char_uncorrect]
	return char_uncorrect


def try_decipher(message_ciphered, key_correct, key_proposed, char_groups):

	if len(key_correct) != len(key_proposed):
		raise Exception("Not supposed to happen. key_correct and key_proposed should have same length.")

	# TODO
	index_group_candidates = [ 0, 1, 2 ]

	nb_repeat_key = len(message_ciphered) // len(key_correct) + 1
	repeated_key_correct = key_correct * nb_repeat_key
	repeated_key_proposed = key_proposed * nb_repeat_key

	chars_maybe_deciphered = [
		try_decipher_char(char_ciphered, key_elem_correct, key_elem_proposed, char_groups, index_group_candidates)
		for char_ciphered, key_elem_correct, key_elem_proposed
		in zip(message_ciphered, repeated_key_correct, repeated_key_proposed)
	]
	return ''.join(chars_maybe_deciphered)


message_clear = 'The quick brown duck duct-taped the ape'


key_correct = (4, 7, 5, 1, 2)

character_set = CHARACTER_SET_INITIAL

char_from_index = list(character_set)

print(message_clear)

message_ciphered, whiches_group = cipher(message_clear, key_correct, character_set)
print(message_ciphered)
print(whiches_group)

key_proposed = (4, 7, 0, 1, 1)
print(try_decipher(message_ciphered, key_correct, key_proposed, CHAR_GROUPS))

key_proposed = (0, 0, 0, 0, 0)
print(try_decipher(message_ciphered, key_correct, key_proposed, CHAR_GROUPS))

