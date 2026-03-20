import Franke_filtration as F
import fractions as Fr
import time

def frac(num):
    return Fr.Fraction(num)



print("Number of non-isomorphic cuspidal automorphic representations in the cuspidal support (insert a positive integer and press enter):")
x=input()
x=int(x)
list=[]

for i in range(0,x):
    print("Size of the general linear group of the ", i+1,". representation (insert a positive integer and press enter):")
    y = input()
    y = int(y)
    print("Sequence of exponents of the ",i+1,". representation (insert rational numbers in the form a/b or just a if the exponent is an integer."
                                              "Press enter after each entry. Letter 'x' denotes the end of the sequence):")
    x=0
    br=0

    list1 = []
    while 1:

        x=input()
        if x=='x':
            break
        br+=1
        list1.append(Fr.Fraction(x))

    list1.sort(reverse=True, key=frac)
    list1.append(y)
    list.append(list1)

print(list)
print("Do you want a detalied description? (y/n)")
c=input()
print(c)
start = time.perf_counter()
if c =='y':

    A, Z, iota_Z, seq = F.detailed_filtration(list)
    print("PARTITIONS IN SEGMENTS ( LEN = ", len(seq), ") :")
    for i in seq:
        print(i)
    print("")
    F.print_filtration(A)

    print("")
    print("Z = ", Z)
    print("")
    print("iota_Z = ", iota_Z)
elif c=='n':
    A=F.filtration(list)
    F.print_filtration(A)



"""FUNCTIONS THAT MAKE SEGMENTATIONS OF ELEMENTS OF 'list'"""



end = time.perf_counter()
elapsed = end - start
print(f'Time taken: {elapsed:.6f} seconds')