import copy,math
import sys
from typing import final

formula = open(str(sys.argv[1]), "r")
formula_lines = []
for x in formula:
  formula_lines.append(x)
proof = open(str(sys.argv[2]),"r")
proof_lines = []
for x in proof:
    proof_lines.append(x)

all_lists_f = []
all_lists_p =[]
output_lines=[]
corr = True

final_output = ''

output_file = open(str(sys.argv[3]),"w")

def get_prop(line):
    lis =  []
    tmp = ''
    for i in range(len(line)):
        if line[i]==' ':
            if tmp == '':
                continue
            lis.append(int(tmp))
            tmp = ''
            continue
        elif line[i]=='0':
            break
        else:
            tmp+=line[i]
    return lis

def remove_dup (lis):
    return [*set(lis)]

def check(lis,lis1,lis2):
    lis1 = lis1 + lis2
    lis1 = remove_dup(lis1)
    for i in range(len(lis1)):
        for j in range(i+1,len(lis1)):
            if lis1[i] == -lis1[j]:
                tmp = copy.deepcopy(lis1)
                tmp.remove(lis1[i])
                tmp.remove(lis1[j])
                tmp.sort()
                if tmp == lis:
                    return True
    return False

def dec(lis,type1,ln1,type2,ln2):
    output = ''
    output += str(ln1) + type1 + ' ' + str(ln2) + type2 + ' '
    for x in lis:
        output += str(x) + ' '
    output += str(0) + '\n'
    return output

def find(all, x):
    x = -x
    bl = False
    val = -1
    l=[]
    for l in all:
        for pi in range(len(l)):
            if l[pi] == x:
                bl=True
                val = pi
                return bl,val+1,l
    return bl,val+1,l


for x in range(2,len(formula_lines)):
    all_lists_f.append(get_prop(formula_lines[x]))
    

for i in range(len(proof_lines)):
    line = proof_lines[i]
    
    ptr = -1

    if line[0] == '?':
        ptr = 0
    else:
        num0 = int(line[0])-1
        file0 = line[1]
    
    if line[3] == '?':
        ptr = 3
    else:
        num1 = int(line[3])-1
        file1 = line[4]
    
    if ptr == -1:
        pass            
        # lis1 = []
        # lis2 = []
        # if file0 == 'p':
        #     line1 = proof_lines[num0]
        #     if num0 > i+1:
        #         corr = False
        #         break
        #     lis1 = get_prop(line1[5:])
        # else:
        #     line1 = formula_lines[num0]
        #     lis1 = get_prop(line1)
        
        # if file1 == 'p':
        #     line2 = proof_lines[num1]
        #     if num1 > i+1:
        #         corr = False
        #         break
        #     lis2 = get_prop(line2[5:])
        # else:
        #     line2 = formula_lines[num1]
        #     lis2 = get_prop(line2)
        # line = line[5:]
        # lis = get_prop(line)
        
        # if(check(lis,lis1,lis2) == False):
        #     corr = False
        #     break
    elif ptr == 0: #1st part has the ?
        
        lis2 = []
        
        if file1 == 'p':
            lis2 = all_lists_p[num1]
        else:
            lis2 = all_lists_f[num1-2]

        sorted(lis2,key = abs)
        corr = False
        for x in lis2:
            bl, ln,l = find(all_lists_p,x)
            if bl:
                lis2.remove(x)
                l.remove(-x)
                lis2 += l
                lis2 = remove_dup(lis2)
                final_output += (dec(lis2,'p',ln+1,file1,num1+1))
                all_lists_p.append(lis2)
                corr=True
                break
            else:
                bl,ln,l = find(all_lists_f,x)
                if bl:
                    lis2.remove(x)
                    l.remove(-x)
                    lis2 += l
                    lis2 = remove_dup(lis2)
                    final_output += (dec(lis2,'f',ln+3,file1,num1+1))
                    all_lists_p.append(lis2)
                    corr = True
                    break
        if corr == False:
            break
        
    else:
        
        lis1 = []
        
        if file0 == 'p':
            lis1 = all_lists_p[num0]
        else:
            lis1 = all_lists_f[num0-2]

        sorted(lis1,key = abs)
        corr = False
        for x in lis1:
            bl, ln,l = find(all_lists_p,x)
            if bl:
                lis1.remove(x)
                l.remove(-x)
                lis1+=l
                lis1 = remove_dup(lis1)
                final_output += (dec(lis1,file0,num0+1,'p',ln+1))
                all_lists_p.append(lis1)
                corr = True
                break
            else:
                bl,ln,l = find(all_lists_f,x)
                if bl:
                    lis1.remove(x)
                    l.remove(-x)
                    lis1+=l
                    lis1 = remove_dup(lis1)
                    final_output += (dec(lis1,file0,num0+1,'f',ln+3))
                    all_lists_p.append(lis1)
                    corr=True
                    break
        if corr == False:
            break

print(final_output)
if corr == True:
    output_file.write(final_output)
else:
    final_output = ''
    for x in proof_lines:
        f=0
        for j in range(len(x)):
            if x[j] == '?' and f==0:
                final_output += 'n'
                f+=1
            elif x[j]=='?' and f==1:
                final_output+='p'
                f+=2
            else:
                final_output+= x[j]
    output_file.write(final_output)

formula.close()
proof.close()
output_file.close()
