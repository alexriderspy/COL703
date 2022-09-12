import copy
import sys

formula = open(str(sys.argv[1]) + ".txt", "r")
formula_lines = []
for x in formula:
  formula_lines.append(x)
proof = open(str(sys.argv[2]) + ".txt","r")
proof_lines = []
for x in proof:
    proof_lines.append(x)

corr = True

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

try:
    for i in range(len(proof_lines)):
        line = proof_lines[i]
        num0 = int(line[0])-1
        file0 = line[1]
        num1 = int(line[3])-1
        file1 = line[4]
        line1 = ''
        lis1 = []
        lis2 = []
        if file0 == 'p':
            line1 = proof_lines[num0]
            if num0 > i+1:
                corr = False
                break
            lis1 = get_prop(line1[5:])
        else:
            line1 = formula_lines[num0]
            lis1 = get_prop(line1)
        
        if file1 == 'p':
            line2 = proof_lines[num1]
            if num1 > i+1:
                corr = False
                break
            lis2 = get_prop(line2[5:])
        else:
            line2 = formula_lines[num1]
            lis2 = get_prop(line2)
        line = line[5:]
        lis = get_prop(line)
        if(check(lis,lis1,lis2) == False):
            corr = False
            break

    if corr == True:
        print("Correct")
    else:
        print("Incorrect")

except:
    print("Incorrect formatting of file")