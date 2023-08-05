# mss.py

#import ssmn

import cryptocode

def reverse(strdata1): #문자열 뒤집기
    reverse_1 = strdata1[::-1]

    return reverse_1

def plb():
    print("Loading bar")

    return 0

def loading(전체, 번째):
    try:
        if 전체 < 번째:
            raise Exception("전체보다 ~번째에 수가 더 큽니다")
        entire1 = int(전체)  # 전체 개수
        th1 = int(번째)
        loadingv1 = entire1 - th1
        text1 = "□" * loadingv1
        loadingv2 = entire1 - loadingv1
        text2 = "■" * loadingv2
        print("-----[" + text2 + text1 + "]-----")
    except Exception as e:
        print("예외가 발생했습니다.", e)

    return 0

def howd():
    print("Hello, World!")

def encrypt(text, key):
    str_encoded = cryptocode.encrypt(text, key)
    return str_encoded

def decrypt(encrypted_text, key):
    str_decoded = cryptocode.decrypt(encrypted_text, key)

    return str_decoded