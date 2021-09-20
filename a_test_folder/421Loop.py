start=253538
end=start+5

def dec_to_ter(num):
    l = []
    while True:
        num,reminder = divmod(num,3)
        l.append(str(reminder))
        if num == 0:
            return "".join(l[::-1])
def f(x,m):
    if x%2==0:
        #print("the %d th is %d"%(m,x))
        return int(x//2)
    
    else:
        #print("the %d th is %d"%(m,x))
        return 3*x+1

while start<end:
    p=start
    m=0
    while p!=1:
        p=f(p,m)
        m+=1
        if p==1:
            print(f"the {start} ends at {m} steps")
            start+=1
print(f"all numbers less than {end} are tested")
    
