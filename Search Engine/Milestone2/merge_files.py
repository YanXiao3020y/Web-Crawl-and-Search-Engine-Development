import string

# error token:
# abdelwahed,: {'4:3', '6:1'}
# abdelwahed:: {'4:3'} ???

#append each line to correspond files, include duplicate token with distinct  posting
def append_to_files(folderPath, numberURL):
    numberRun = 0
    for i in range (0, numberURL):
        print(str(numberRun)) #counter
        numberRun += 1

        filePath = folderPath + "\\" + str(i) + ".txt"

        #open url file and begin to read line by line until the end of file
        with open(filePath, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                word_first_letter = line.split()[0][0].lower()
                if(word_first_letter.isalpha()):
                    word_file = folderPath + "\\a_z_special\\" + word_first_letter + ".txt"
                else:
                    word_file = folderPath + "\\a_z_special\\special.txt"

                #append line to end of file without reading, please check whether 'a' and write()
                # correct or not???
                with open(word_file, 'a', encoding='utf-8', errors='ignore') as file:
                    file.write(line.lower()) #assume line contain "\n", plz check ???


#merge duplicate to one distinct word, and sorted
#example output: arrows: {['5:1', '8:1']}
def merge_to_files(folderPath):
    numberRun = 0
    alphabet_string = string.ascii_lowercase #Create a string of all lowercase letters
    files_list = list(alphabet_string) #Create a list of all lowercase letters
    files_list.append("special") #add special file #how to need to order last file???
    for f in files_list:
        word_dict = {}  # key : list() #key is token, list is postings
        file_name = folderPath + "\\" + f + ".txt"
        with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line_list = line.strip().split()
                posting = (line_list[2] + line_list[3])[1:-1]  # [1:-1] omits {}, keep the format 0:0
                if (not word_dict.__contains__(line_list[0])):  # no key yet, then create, else then append into list
                    word_dict[line_list[0]] = {posting}
                else:
                    word_dict[line_list[0]].add(posting)  # append posting to list of posting in word_dict
        new_file_name = folderPath + "\\new\\" + f + ".txt"
        # rewrite the whole file from begining using word_dict #make sure it overwrite whole date???
        with open(new_file_name, 'w', encoding='utf-8', errors='ignore') as file:
            for key, value in sorted(word_dict.items()):
                #sorted(value, key=lambda s: s.split('_', 1)[0])
                word_str = key + ": " + str(value) + "\n"  # ??? "key: {...}\n" format
                file.write(word_str)
            print("final:" + str(numberRun)) #counter
            numberRun +=1


if __name__ == "__main__":
    #order of calling function:
    folderPath = r'C:\Users\yanxi\PycharmProjects\proj3 M2\token'

    word_file = r'C:\Users\yanxi\PycharmProjects\proj3 M2\token\a_z_special'

    numberURL = 55392+1
    append_to_files(folderPath, numberURL)
    merge_to_files(word_file)

