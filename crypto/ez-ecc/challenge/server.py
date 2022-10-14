#!/usr/bin/sage
from sage.all import *
import json 
import random
from flag import FLAG 

def level_one():
    print("Welcome to EZ-ECC Interview Level 1")
    print("To pass this level you need to answer the following questions")
    for i in range(3):
        while True:
            try:
                p = random_prime(1024) 
                F = Zmod(p)
                a = F(random_prime(1024))
                b = F(random_prime(1024))
                E = EllipticCurve(F, [a,b])
                point = E.random_point()
                point_1 = E.random_point()
            except:
                pass
            finally:
                break
        print(f"We have an elliptic Curve generated with sagemath E = EllipticCurve(Zmod({p}), [a,b]) Q(x,y,z), R(x1,y1,z1) are points {point} {point_1}")
        print('What is the value of b ?')
        input_b = int(input(' > '))
        if int(b) != input_b:
            print('You are wrong sadly')
            return False
        else:
            print('That is true !')
    return True



    
def level_two():
    print("Congratulations on passing to the level two !")
    print('This time we are dealing with a special type of curves. ')
    curves = json.loads(open('level_2_curves.json','r').read())
    for i in range(3):
        index = random.randint(0,len(curves))
        curve = curves[index]
        p = curve['p']; a = curve['a']; b = curve['b'];
        C = EllipticCurve(GF(p),[a,b])
        point = C.random_point()
        print(f"Now, we have a = {curve['a']} p = {p} b = {curve['b']} and Q = {point} ")
        s = random_prime(512)
        q = s*point 
        print(f's*Q = {q}')
        print('What is the value of s ?')
        n = int(input('>> '))
        if n != s:
            print('Well that is not correct gentlmen')
            return False
        else:
            print('That is correct !!')
    return True





def level_three():
    print('You are rocking ! and we are now on the last level')
    print('In this level we will deal with a special attack on elliptic curves')
    curves = json.loads(open('level_3_curves.json','r').read())
    for i in range(3):
        index = random.randint(0,len(curves))
        curve = curves[index]
        p = curve['p']; a = curve['a']; b = curve['b'];
        C = EllipticCurve(GF(p),[a,b])
        point = C.random_point()
        print(f"Now, we have a = {curve['a']} p = {p} b = {curve['b']} and Q = {point} ")
        s = random_prime(512)
        q = s*point 
        print(f's*Q = {q}')
        print('What is the value of s ?')
        n = int(input('>> '))
        if n != s:
            print('Well that is not correct gentlmen')
            return False
        else:
            print('That is correct !!')
    return True






def main():
    print("Welcome to our interview about ECC ")
    print("In order to get the job you need to answer correctly to all the questions ranging from different levels")
    print("Are you ready ? [Y/N]")
    ready_text = str(input())
    if ready_text == 'Y':
        if level_one():
            if level_two():
                if level_three():
                    print(f'Here is your flag  {FLAG}')

    elif ready_text =='N':
        print("Well you can leave us your documents an we will call you during this week :)")
    else:
        print("We are not playing games here !")





if __name__ == "__main__":
    main()





