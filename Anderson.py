import math
import random
def Anderson_formula(T,G,N):

    P = T*G/N
    return P

def Class(a):
    if (a >= 0.9):
        classpass = "So Weak"
    elif (a >= 0.8 and a<0.9):
        classpass = "Weak"
    elif (a>=0.5 and a<0.8):
        classpass = "Medium"
    elif (a >= 0.3 and a< 0.5):
        classpass = "Secure"
    elif (a < 0.3):
        classpass = "Very Secure"
    return classpass

def Salting(matkhau):
    dodaimatkhau, khonggiandodai, N = LengthPass(matkhau)
    dodaimuoi = random.randint(1,9)
    #list_mat_khau = list(matkhau)
    print("do dai muoi: " + str(dodaimuoi))
    dodaimatkhaumoi = dodaimatkhau + dodaimuoi
    print("do dai mat khau moi: " + str(dodaimatkhaumoi))
    list_muoi = []
    for i in range (1,dodaimuoi + 1):
        a = random.randint(1,4)
        if (a == 1):
            char = chr(random.randint(48,57))
        if (a == 2):
            char = chr(random.randint(65,90))
        if (a == 3):
            char = chr(random.randint(97,122))
        elif (a == 4):
            char = "_"
        print(str(i) + " " + str(a) + ": " + char)
        list_muoi.append(char)
    muoi = ''.join(list_muoi)
    print(muoi)
    matkhaumoi = matkhau + muoi
    print("Mat khau moi: " + matkhaumoi)
    return muoi,matkhaumoi

def LengthPass(a):
    dodai = len(a)
    cackieu = []
    list = set(a)
    # 3: 97 - 122 : a - z
    # 2: 65 - 90 : A - Z
    # 1: 48 - 57 : 0 - 9\
    # 4: _
    m = 0
    for i in a:
        ASC = int(ord(i))
        if ( ASC >= 48 and ASC <= 57):
            m = 1
            cackieu.append(m)
        elif (ASC >= 65 and ASC <= 90):
            m = 2
            cackieu.append(m)
        elif (ASC>= 97 and ASC <= 122):
            m = 3
            cackieu.append(m)
        elif (ASC == 95):
            m = 4
            cackieu.append(m)

    #print(cackieu)
    set_kieu = set(cackieu)
    #print(set_kieu)
    khonggiandodai = 0
    for i in set_kieu:
        if (i == 1):
            khonggiandodai = khonggiandodai + 10
        elif (i == 2):
            khonggiandodai = khonggiandodai + 26
        elif (i == 3):
            khonggiandodai = khonggiandodai + 26
        elif (i == 4):
            khonggiandodai = khonggiandodai + 1
    #print("Khong gian ky tu mat khau: " + str(khonggiandodai))
    #print("do dai pass: " + str(dodai))

    return dodai,khonggiandodai,pow(khonggiandodai,dodai)


def Salting(matkhau):
    dodaimatkhau, khonggiandodai, N = LengthPass(matkhau)
    dodaimuoi = random.randint(1,9)
    #list_mat_khau = list(matkhau)
    print("do dai muoi: " + str(dodaimuoi))
    dodaimatkhaumoi = dodaimatkhau + dodaimuoi
    print("do dai mat khau moi: " + str(dodaimatkhaumoi))
    list_muoi = []
    for i in range (1,dodaimuoi + 1):
        a = random.randint(1,4)
        if (a == 1):
            char = chr(random.randint(48,57))
        if (a == 2):
            char = chr(random.randint(65,90))
        if (a == 3):
            char = chr(random.randint(97,122))
        elif (a == 4):
            char = "_"
        print(str(i) + " " + str(a) + ": " + char)
        list_muoi.append(char)
    muoi = ''.join(list_muoi)
    print(muoi)
    matkhaumoi = matkhau + muoi
    print("Mat khau moi: " + matkhaumoi)
    return muoi,matkhaumoi
# a = "Abeg144_"
G = math.pow(10,7)
T = 80*3*24*60*60
# dodaimatkhau,khonggiandodai, N = LengthPass(a)
# Ander = Anderson_formula(T,G,N)
#
# print("Anderson: " + str(Ander))
# print(Class(Ander))
#
# muoi,matkhaumoi = Salting(a)
#
# dodaimatkhau,khonggiandodai, N = LengthPass(matkhaumoi)
# Ander = Anderson_formula(T,G,N)
# print(Class(Ander))