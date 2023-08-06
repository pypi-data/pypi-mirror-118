'''
2021/9/1
'''
import random

def key_zero(number):
    messages = "123456789"
    mess = random.sample(messages,1)
    da_mess = mess
    str_mess = "".join(da_mess)
    if int(number) > 1:
        for numbe in range(int(number)):
            ran = random.random()
            str_ran = f"{ran}"
            rans = str_ran.replace('.', f'{str_mess}')
            print(rans)
    if int(number) <= 1:
            rans = random.random()
            str_rans = f"{rans}"
            ranss = str_rans.replace('.', f'{str_mess}')
            print(ranss)
def key_list(message, number):
    lists = random.sample(message,int(number))
    #print(lists)
    data_list = lists
    str_list = "".join(data_list)
    print(str_list)

def key_str(number):
    message = "~`1!2@3#4$5%6^7&8*9(0)-_=+qQwWeErRtTyYuUiIoOpP[{]}\|aAsSdDfFgGhHjJkKlL:;zZxXcCvVbBnNmM,<.>/?"
    mess = random.sample(message,int(number))
    data_mess = mess
    str_mess = "".join(data_mess)
    print(str_mess)
#key_app("haskjfhjshfggeahgihegwegj8924ty542hbty149",'20')
def key_letter(number):
    message = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    mess = random.sample(message,int(number))
    da_mess = mess
    str_mess = "".join(da_mess)
    print(str_mess)

def key_int(number, numbers, sl):
    messages = "123456789"
    mess = random.sample(messages,1)
    da_mess = mess
    str_mess = "".join(da_mess)
    
    if int(sl) <= 1:
        dom = random.uniform(number,numbers)
        str_dom = f"{dom}"
        doms = str_dom.replace('.', f"{str_mess}")
        print(doms)
    else:
        for i in range(int(sl)):
            ran = random.uniform(number,numbers)
            str_ran = f"{ran}"
            rans = str_ran.replace('.', f'{str_mess}')
            print(rans)
#key_str#92
#key_letter#52
