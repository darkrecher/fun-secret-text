"""

python main.py --cipher msg="The quick brown duck duct-taped the happy ape" keys=4-7-5-1-2 > game_data.json

python main.py --decipher key_index=C key_val=5

"""

import sys
import json


CHAR_GROUP_1 = 'aeiouyAEIOUY ' # voyelles
CHAR_GROUP_2 = 'ckqbdptvfCKQBDPTVF' # consonnes 1
CHAR_GROUP_3 = 'ghjlmnrswxzGHJLMNRSWXZ' # consonnes 2

# TODO : ajout caractères à l'arrache
CHAR_GROUPS = [ CHAR_GROUP_1 + '-,.', CHAR_GROUP_2, CHAR_GROUP_3 ]

CHARACTER_SET_INITIAL = ''.join(CHAR_GROUPS)


def which_group(char):
	for index_group, char_group in enumerate(CHAR_GROUPS):
		if char in char_group:
			return index_group
	raise Exception("Char not in any char_group. Not supposed to happen. char : " + char)


def cipher(message_clear, key, character_set):

	index_from_char = {
		char: index
		for index, char
		in enumerate(character_set)
	}
	char_from_index = list(character_set)

	message_indexes = [ index_from_char[char] for char in message_clear ]
	nb_repeat_key = len(message_clear) // len(key) + 1
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


def try_decipher_char(char_ciphered, key_solution, key_proposed, char_groups, index_group_candidates):

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
	index_char_clear = (index_char_ciphered - key_solution + char_set_len) % char_set_len
	char_clear = char_from_index[index_char_clear]

	if key_solution == key_proposed:
		return char_clear

	# La clé pour le caractère n'est pas la bonne. On redécale avec la clé proposée.
	# Mais on redécale dans le group de caractère restreint.
	# Ça renverra un caractère "pas si incorrect que ça", au lieu de "totalement incorrect".

	group_candidates = [ char_groups[index_group] for index_group in index_group_candidates ]
	character_set_restricted = ''.join(group_candidates)
	char_set_len = len(character_set_restricted)
	try:
		index_char_clear = character_set_restricted.index(char_clear)
	except:
		print("Not supposed to happen. char_clear not in group_candidates. char_clear :", char_clear, "char_groups :", char_groups, "index_group_candidates :", index_group_candidates)
		raise
	index_char_uncorrect = (index_char_clear + key_solution - key_proposed + char_set_len) % char_set_len
	char_uncorrect = character_set_restricted[index_char_uncorrect]
	return char_uncorrect


def create_index_group_candidates(which_group, key_correct_offset_backw, key_correct_offset_forw, nb_groups):
	index_group_candidates = [ which_group ]
	if not key_correct_offset_backw:
		index_suppl = (which_group - 1 + nb_groups) % nb_groups
		index_group_candidates.append(index_suppl)
	if not key_correct_offset_forw:
		index_suppl = (which_group + 1) % nb_groups
		index_group_candidates.append(index_suppl)
	return index_group_candidates


def try_decipher(message_ciphered, keys_solution, keys_proposed, char_groups, whiches_group):

	if len(keys_solution) != len(keys_proposed):
		raise Exception("Not supposed to happen. keys_solution and keys_proposed should have same length.")

	keys_correct = [ key_solution == key_proposed for (key_solution, key_proposed) in zip (keys_solution, keys_proposed) ]
	keys_correct_offset_backw = keys_correct[1:] + [ keys_correct[0] ]
	keys_correct_offset_forw = [ keys_correct[-1] ] + keys_correct[:-1]

	# TODO : un itérateur qui loope à l'infini sur une liste
	nb_repeat_key = len(message_ciphered) // len(keys_solution) + 1
	repeated_keys_solution = keys_solution * nb_repeat_key
	repeated_keys_proposed = keys_proposed * nb_repeat_key
	repeated_keys_correct_offset_backw = keys_correct_offset_backw * nb_repeat_key
	repeated_keys_correct_offset_forw = keys_correct_offset_forw * nb_repeat_key

	index_groups_candidates = [
		create_index_group_candidates(which_group, key_correct_offset_backw, key_correct_offset_forw, len(CHAR_GROUPS))
		for (which_group, key_correct_offset_backw, key_correct_offset_forw)
		in zip(whiches_group, repeated_keys_correct_offset_backw, repeated_keys_correct_offset_forw)
	]

	chars_maybe_deciphered = [
		try_decipher_char(char_ciphered, key_solution, key_proposed, char_groups, index_group_candidates)
		for char_ciphered, key_solution, key_proposed, index_group_candidates
		in zip(message_ciphered, repeated_keys_solution, repeated_keys_proposed, index_groups_candidates)
	]
	return ''.join(chars_maybe_deciphered)


def generate_ciphered_data():

	message_clear = None
	str_keys = None
	for arg in sys.argv[1:]:
		if arg.startswith('msg='):
			message_clear = arg[len('msg='):]
		elif arg.startswith('keys='):
			str_keys = arg[len('keys='):]
	if message_clear is None or str_keys is None:
		print("TODO. usage. main.py --cipher msg=bla_bla keys=5-9-7-2")
		raise Exception("Missing argument(s).")

	keys_solution = str_keys.split('-')
	# TODO : checker valeurs numérique avant de faire planter
	keys_solution = [ int(key) for key in keys_solution ]

	character_set = CHARACTER_SET_INITIAL
	message_ciphered, whiches_group = cipher(message_clear, keys_solution, character_set)

	json_data = {
		'message_ciphered': message_ciphered,
		'infos': keys_solution,
		'groups': whiches_group,
		'additional_chars': 'TODO',
	}
	print(json.dumps(json_data))


def get_key_elem_from_argv():
	key_index = None
	key_val = None
	# TODO : checker valeurs numérique avant de faire planter
	# TODO : checker que l'index est in-bounds.
	for arg in sys.argv[1:]:
		if arg.startswith('key_index='):
			key_index = arg[len('key_index='):].upper()
			if len(key_index) == 1 and ('A' <= key_index <= 'Z'):
				key_index = ord(key_index) - ord('A')
			else:
				key_index = int(key_index)
		elif arg.startswith('key_val='):
			key_val = arg[len('key_val='):]
			key_val = int(key_val)
	if key_index is None or key_val is None:
		print("TODO. usage. main.py --decipher key_index=B key_val=7")
		raise Exception("Missing argument(s).")
	return key_index, key_val


def read_game_data_json():
	with open('game_data.json', 'r', encoding='utf-8') as file_game_data_json:
		game_data_json = file_game_data_json.read()
	game_data = json.loads(game_data_json)
	return game_data


def read_keys_proposed(nb_keys):
	try:
		with open('keys_proposed.json', 'r', encoding='utf-8') as file_keys_proposed_json:
			keys_proposed_json = file_keys_proposed_json.read()
		keys_proposed = json.loads(keys_proposed_json)
	# TODO : excepter des exceptions plus précises.
	except Exception:
		keys_proposed = [ 0, ] * nb_keys

	if len(keys_proposed) != nb_keys:
		raise Exception("Not supposed to happend. nb keys different. keys_proposed :", keys_proposed, "nb_keys :", nb_keys)

	return keys_proposed


def write_keys_proposed(keys_proposed):
	keys_proposed_json = json.dumps(keys_proposed)
	with open('keys_proposed.json', 'w', encoding='utf-8') as file_keys_proposed_json:
			file_keys_proposed_json.write(keys_proposed_json)


def get_key_to_change_from_input(keys_solution):

	# TODO : passer en param le len(keys_solution), et non pas keys_solution.

	key_index_letter_end = chr(ord('A') - 1 + len(keys_solution))
	key_index_letter = input("Indiquez la lettre correspondant à la question. (de A à %s) : " % key_index_letter_end)
	if not key_index_letter:
		print("fail input.")
		return None
	# TODO : if isdigit, prendre la valeur direct.
	key_index_letter = key_index_letter[0].upper()
	key_index = ord(key_index_letter) - ord('A')
	if key_index < 0 or key_index >= len(keys_solution):
		print("fail input. Il faut indiquer une lettre de A à %s" % key_index_letter_end)
		return None

	key_val = input("Indiquez la réponse (un nombre) : ")
	if not key_val.isdigit():
		print("fail input. Il faut indiquer un nombre")
		return None

	return key_index, key_val


def main():

	if '--cipher' in sys.argv[1:]:

		generate_ciphered_data()

	elif '--decipher' in sys.argv[1:]:

		character_set = CHARACTER_SET_INITIAL
		game_data = read_game_data_json()
		keys_solution = game_data['infos']
		message_ciphered = game_data['message_ciphered']
		whiches_group = game_data['groups']
		keys_proposed = read_keys_proposed(len(keys_solution))

		(key_index, key_val) = get_key_elem_from_argv()
		keys_proposed[key_index] = key_val

		message_tried = try_decipher(message_ciphered, keys_solution, keys_proposed, CHAR_GROUPS, whiches_group)
		print(message_tried)
		write_keys_proposed(keys_proposed)

	else:

		character_set = CHARACTER_SET_INITIAL
		game_data = read_game_data_json()
		keys_solution = game_data['infos']
		message_ciphered = game_data['message_ciphered']
		whiches_group = game_data['groups']
		keys_proposed = read_keys_proposed(len(keys_solution))

		statements = game_data['statements']
		len_statements = max([ len(statement) for statement in statements ])

		print('')
		print('-' * 50)
		print('')

		for key_index in range(len(keys_solution)):
			key_index_letter = chr(ord('A') + key_index)
			key_proposed = keys_proposed[key_index]
			statement = statements[key_index]
			if key_proposed != 0:
				print("%s : %s (clé actuelle : %s)" % (key_index_letter, statement.ljust(len_statements), str(key_proposed)))
			else:
				print("%s : %s" % (key_index_letter, statement))
			print('')

		# TODO : moche. Il faut faire un join.
		print('-' * 50)
		print('')

		info_key_to_change = get_key_to_change_from_input(keys_solution)

		if info_key_to_change is not None:
			key_index, key_val = info_key_to_change
			keys_proposed[key_index] = int(key_val)
		else:
			print('')

		message_tried = try_decipher(message_ciphered, keys_solution, keys_proposed, CHAR_GROUPS, whiches_group)
		print(message_tried)
		write_keys_proposed(keys_proposed)


if __name__ == '__main__':
	main()
