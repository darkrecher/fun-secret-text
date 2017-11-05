print("pouet")


CHARACTER_SET_INITIAL = 'abcdefghijklmnopqrstuvwxyw ABCDEFGHIJKLMNOPQRSTUVWXYW'

message_clear = 'The fucking quick brown fox fucked THE LAZY DOG'

key = (4, 7, 5, 1)


character_set = CHARACTER_SET_INITIAL

dict_cipher = {
	char: index
	for index, char
	in enumerate(character_set)
}

print(dict_cipher)


