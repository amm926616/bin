import random

lst = ['~', '!', '@', '#', '$', '^', '&', '*', '_', '+']
num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
small_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def create_pw():
	for i in range(50):
		rd_lst = random.choice(lst)
		rd_num = random.choice(num)
		rd_small_letters = random.choice(small_letters)
		rd_capital_letters = random.choice(capital_letters)
		random_lst = [rd_lst, rd_num, rd_small_letters, rd_capital_letters]
		random.shuffle(random_lst)

		pw_string = ''
		pw_string = pw_string.join(str(random_lst[i]) for i in range(4))
		print(pw_string)
		with open('pw_strings.txt', 'a') as f:
			f.write(pw_string + '\n')

create_pw()

