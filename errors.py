import string

result_fl = open('text.txt')
label_fl = open('lines.txt')
output_file = open('statistics.txt','w+')

def levenshteinDistance(s1, s2):
	if len(s1) > len(s2):
		s1, s2 = s2, s1

	distances = range(len(s1) + 1)
	for i2, c2 in enumerate(s2):
		distances_ = [i2+1]
		for i1, c1 in enumerate(s1):
			if c1 == c2:
				distances_.append(distances[i1])
			else:
				distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
		distances = distances_
	return distances[-1]

def words_error(words_result, words_labels):
	word_accuracy = []
	char_accuracy = []
	word_accuracy.append([1 if word_res == word_lab else 0
					for [word_res,word_lab] in zip(words_result,words_labels)])

	char_accuracy.append([levenshteinDistance(word_res, word_lab)
					for [word_res,word_lab] in zip(words_result,words_labels)])

	return [word_accuracy,char_accuracy]

def parse_data(data, words_to_ignore, split):
	words = []
	idx_wrd = []
	for line in data:
		if split:
			idx_wrd.append(line.split()[0].split('/')[1])
			words.append(line.split()[words_to_ignore:])
		else:
			idx_wrd.append(line.split()[0])
			words.append(line.split()[words_to_ignore:][0].split('|'))

	for sentence in words:
		for idx,word in enumerate(sentence):
			if word in string.punctuation:
				sentence[idx-1]+=sentence[idx]
				del sentence[idx]

	return dict(zip(idx_wrd,words))

def main():
	res_data = result_fl.readlines()
	label_data = label_fl.readlines()[23:]

	dict_words_result = parse_data(res_data, 1, True)
	dict_words_labels = parse_data(label_data, 8, False)

	print dict_words_result
	print dict_words_labels

	result = []
	for key, line in dict_words_result.iteritems():
		if key in dict_words_labels:
			result.append(words_error(line, dict_words_labels[key]))

	for res in result:
		print res[0]

if __name__ == "__main__":
	main()



