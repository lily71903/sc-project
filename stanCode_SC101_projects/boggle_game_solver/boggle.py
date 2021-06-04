"""
File: boggle.py
Name: chu chia hsuan
----------------------------------------
TODO:
"""
import time
# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
a_dict = {}
ans_l = []


def main():
	"""
	遊戲'boggle'，一開始會先請玩家輸入四組單字，排出一個 4 x 4 的字母lst，
	接著串連在字母盤上相連的字母，去找出存在於這個 4 x 4 的方形字母拼盤的所有英文單字。
	"""
	boggle = boggle_input()
	# boggle = ['f', 'y', 'c', 'l', 'i', 'o', 'm', 'g', 'o', 'r', 'i', 'l', 'h', 'j', 'h', 'u'] 			 # boggle長相
	start = time.time()
	if len(boggle) == 16:
		read_dictionary(boggle)
		boggle = [boggle[i:i + 4] for i in range(0, len(boggle), 4)]
		# boggle = [['f', 'y', 'c', 'l'], ['i', 'o', 'm', 'g'], ['o', 'r', 'i', 'l'], ['h', 'j', 'h', 'u']] # boggle長相
		find_boggle(boggle)
		print(f'There are {len(ans_l)} words in total.')
		end = time.time()
		print("執行時間：%f 秒" % (end - start))


def boggle_input():
	"""
	讓使用者輸入boggle的文字，並檢查是否輸入正確。
	:return: (lst)boggle
	"""
	illegal_switch = 1
	boggle = []

	for i in range(1, 5):
		if illegal_switch == 1:
			row = input(f'{i} row of letters: ')
			row = row.lower().split()
			for st in row:
				if len(st) != 1 or len(row) != 4 or st.isalpha() == False:
					print('Illegal input')
					illegal_switch *= -1
					break
				else:
					boggle.append(st)
			# boggle = [st for st in row]
	return boggle


def read_dictionary(boggle):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python dict
	:param boggle:(lst) list of word that users input for 'boggle'.
	"""
	global a_dict
	with open(FILE, mode='r') as f:
		for line in f:
			a = line.strip()

			# 字典內所有字彙字元皆需存在boggle list中
			if a[0] in boggle and len(a) >= 4:		# 先篩選起始字元及長度
				correct_count = 0					# 計算正確字元出現次數
				wrong_count = 0						# 計算錯誤字元出現次數
				for i in list(a):
					if i in boggle:
						correct_count += 1
					else:
						wrong_count += 1
					if wrong_count == 1:
						break
					if correct_count == len(a):		# 若字彙長度和正確字元次數相等，則列入字典
						a_dict[a] = 1


def find_boggle(b_list):
	"""
	設定每次開始找尋的起始文字位置，並丟入find_boggle_helper進行排序。
	:param b_list:list of word that users input for 'boggle'.
	:return: no return
	"""
	for i in range(4):
		for j in range(4):
			start_point = [i, j]
			find_boggle_helper(b_list, start_point, [], '')


def find_boggle_helper(b_list, s_point, current_l, word_test):
	"""
	以s_point為起始文字位置，排序所有文字組合，並逐次檢查該組合文字，是否有對應之文字排序存在字典中(a_dict)，
	並將長度大於4，且存在於字典的文字列印出來，並加入ans_l(lst)中。
	:param b_list: (lst) list of word that users input for 'boggle'.
	:param s_point:(lst) [start_x,start_y],the start point of the first word.
	:param current_l: (lst) the list of every word's point(x,y).
	:param word_test: (str) change the current_l (x,y) to word(str).
	:return: no return
	"""
	global a_dict, ans_l

	if has_prefix(word_test):
		# BASE CASE
		if word_test in a_dict and len(word_test) >= 4:				# 存在於字典且長度大於4之文字
			print(f'Found: "{word_test}"')
			ans_l.append(word_test)
			del a_dict[word_test]									# 於字典刪除已找到的文字，為之後比對更長文字組合使用 ex:room & roomy
			find_boggle_helper(b_list, [current_l[-1][0], current_l[-1][1]], current_l, word_test)

		# Not BASE CASE
		else:
			if not current_l:										# 如果目前的組合為None,則(x,y)為find_boggle的起始文字位置
				start_x, start_y = s_point[0], s_point[1]
			else:
				start_x, start_y = current_l[-1][0], current_l[-1][1]	 # 若目前的組合非None，則以最後一個文字的位置做為比對起始位置
			for i in range(-1, 2, 1):								# 字串可以串每個位置的+-1
				for j in range(-1, 2, 1):							# 字串可以串每個位置的+-1
					x = start_x + i
					y = start_y + j
					if 0 <= x < 4:
						if 0 <= y < 4:
							if [x, y] not in current_l:				# 已在排序組合之位置不使用
								# choose
								current_l.append([x, y])			# 串上新位置
								word_test += b_list[x][y]			# 位置轉換為文字
								# explore
								find_boggle_helper(b_list, s_point, current_l,word_test)	# 找下一格字
								# un-choose
								current_l.pop()						# 刪除已不需要之位置
								word_test = word_test[:-1]			# 刪除不需要之文字


def has_prefix(word):
	"""
	比對字典中是否有word開頭之字彙
	:param word: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""

	if len(word) > 1:
		for i in a_dict:
			if i.startswith(word):
				return True
		return False
	return True


if __name__ == '__main__':
	main()
