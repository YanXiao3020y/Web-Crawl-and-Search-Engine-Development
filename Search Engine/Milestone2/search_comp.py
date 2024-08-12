#M2
import re

# get user input and tokenized into a dictionary {token: first letter}
def get_input(str_input):
    token_dictionary = dict()
    for word in list(str_input.strip().split()):
        token_dictionary[word] = word[0]
    return token_dictionary

# read file and return dictionary of found {'token': 'token:posting\n'}
def read_tokenfile(folderpath, token_dictionary):
    result = dict()
    for token in token_dictionary:
        if(token_dictionary[token].isalpha()):
            filePath = folderpath + '\\' + str(token_dictionary[token].lower()) + '.txt'

        else:
            filePath = folderpath + 'special.txt'

        with open(filePath, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                afterline = re.split("{'|:|', '|'|}", line)[2:-2]
                word = line.split()[0][:-1]
                #print('here is the word:', word)
                #print('the token', token)
                #print('are they equal? --> ', str(token) == str(word))
                if str(token) == str(word):
 
                    result[token] = afterline

                    #result[token] = line[0:-1] #to delete \n
                    break
    return result
    
def get_posting_dict(result_dict):
    # result_dict = {str(word_key): list(posting_list)}
    word_post_dict = dict() # {str(word): nested_dict{posting}}
    for word in result_dict:
        posting_dict = dict()
        posting_lst = result_dict[word]
        index = 0
        while index != len(posting_lst):
            posting_dict[int(posting_lst[index])] = int(posting_lst[index + 1])
            index += 2

        word_post_dict[word] = posting_dict

    return word_post_dict


def find_intersect(word_post_dict):
    #format: {"word" : set(doc_id)}
    words_id_dict = dict()
    for word in word_post_dict:
        id_set = set()
        for doc_id in word_post_dict[word]:
            id_set.add(doc_id)
        words_id_dict[word] = id_set

    # list of query word
    words_list = [word for word in words_id_dict.keys()]

    final_set_default_word = words_list[0]
    final_set = words_id_dict[final_set_default_word]
    for word in words_list:
        if word != final_set_default_word:
            #pre-check to see if the intersection has zero duplicates.
            temp_set = final_set
            common_set = temp_set.intersection(words_id_dict[word])
            if(len(common_set) != 0):
                final_set = common_set
    
    return final_set

#sum all frequency according to doc_id
def get_query_frequency (final_set, word_post_dict):
    sum_dict = dict() # format: {doc_id : total_frequency}
    for doc_id in final_set:
        frequency_sum = 0
        for word in word_post_dict:
            frequency_sum += word_post_dict[word][doc_id]
        sum_dict[doc_id] = frequency_sum
    sum_dict = sorted(sum_dict.items(), key=lambda x: x[1], reverse=True)
    return sum_dict

def top_five_links(sum_dict):
    text_file = "document_id.txt"
    #top_five_doc_id
    five_most_urls = list()
    top_five = sum_dict[0:5]
    five_ids = [posting_set[0] for posting_set in top_five]
    for result_id in five_ids: 
        with open(text_file, "r") as file:
            for search_id, line in enumerate(file):
                if result_id == search_id:
                    five_most_urls.append(line.rstrip().split(": ")[-1])
                    break
                
    return five_most_urls

        
if __name__ == "__main__":
    # folder path need to be changed
    folderpath = r'C:\Users\wizop\Downloads\assignment3\token\a_z_special\new'
    print('***** Search Engine Starts! *****')
    command = ''
    while command != 'N':
        str_input = str(input('Search[Type anything]: ')).lower()
        token_dictionary = get_input(str_input)
        result_dict = read_tokenfile(folderpath, token_dictionary)
        word_post_dict = get_posting_dict(result_dict)
        final_set = find_intersect(word_post_dict)
        sum_dict = get_query_frequency(final_set, word_post_dict)
        top_five_urls = top_five_links(sum_dict)
        print('\nHere are the top 5 results:\n')
        for url in top_five_urls:
            print(url)
        command = str(input('\nContinue?(Y\\N)'))
