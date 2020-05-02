import os
import re # import thư viện re
import ntpath
from bs4 import BeautifulSoup # inport thư viện BeautifulSoup
import nltk # import thư viện nltk
from string import punctuation #import tập dấu câu từ thư viện string
from nltk.corpus import stopwords # import tập hư từ
from nltk.tokenize import word_tokenize, sent_tokenize # import các hàm xử lý tách từ, tách câu
from nltk.stem import PorterStemmer
my_stopwords = set(stopwords.words('english') + list(punctuation))

# Đọc file từ thư mục
list_path = []
for root, dirs, files in os.walk('./input'):
    for file in files:
        list_path.append(root+"/"+file)

i = 0 
for i in range(len(list_path)):
    read_file = open(list_path[i], "r")
    a = read_file.read()

#lấy dữ liệu từ file
def get_text(file):
    read_file = open(file, "r")
    text = read_file.readlines()
    text  =  ' '.join(text);
    return text

#loại bỏ các thẻ của html trong file
def clear_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


#loại bỏ các ký tự đặc biệt
def remove_special_character(text): # text là 1 string
    string  = re.sub('[^\w\s]', '',text) #Thay thế các ký tự đặc biệt bằng ''
    string = re.sub('\s+', ' ', string) #Xử lý các khoảng trắng thừa ở giữa chuỗi
    string  = string.strip() #Xử lý các khoảng trắng thừa ở đầu và cuối chuỗi
    return string

j = 0
for j in range(len(list_path)):
    text = get_text(list_path[j])
    text_cleared = clear_html(text)
    #Tách câu
    sents = sent_tokenize(text_cleared)
    #Loại bỏ ký tự đặc biệt trong câu
    sents_cleared = [remove_special_character(s) for s in sents]
    #Nối các câu lại thành text
    text_sents_join = ''.join(sents_cleared)
    #Tách từ
    words = word_tokenize(text_sents_join)
    #Đưa về chữ thường
    words = [word.lower() for word in words]
    #Loại bỏ hư từ
    words = [word for word in words if word not in my_stopwords]



# tu tu danh sach lien ket
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
# lay ten file cu doi qua ten file moi
def rename_files(string):
    listString = string.split('.')
    return listString[0]+"_word."+listString[1]

def listToString(s):  
    
    str1 = ""  
    
    for ele in s:  
        str1 += ele   
     
    return str1  

def write_file(string_file, words):
    dir_name_file = './output/'+string_file

    os.makedirs(os.path.dirname(dir_name_file), exist_ok=True)
    with open(dir_name_file, "w") as f:
        f.write(listToString(words))



# chuan hoa tu
ps = PorterStemmer()
words = [ps.stem(word) for word in words]

k = 0 
for k in range(len(list_path)):
    list_file_des = rename_files(path_leaf(list_path[k]))
    
    write_file(list_file_des, words)

print(words)