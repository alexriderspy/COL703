final_O = -1
P = []
F = []
flag = 0

def obtain_prop(line):
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

def read(lis, index):
    line = lis[index]
    i = 0
    c1 = ''
    c2 = ''
    while line[i] != ' ':
        c1 += line[i]
        i += 1
    i+=1
    while i<len(line):
        c2 += line[i]
        i += 1
    return c1,c2
    
def obtain (c,O):
    global F
    line_num = int(c[:-1])
    type = c[-1]
    if type == 'f':
        line_num -=3
        return F[line_num]
    else:
        line_num-=1
        return O[line_num][1]

def obtainlis (O):
    lis = []
    for tup in O:
        lis.append(tup[1])
    return lis

#O is output file in the form of tuple (x,y)

#if final_O == -1, then replace with np

def union(clis1,cl1,clis2,cl2):
    clis = clis1[:]
    clis += clis2
    clis.remove(cl1)
    clis.remove(cl2)
    clis = remove_dup(clis)
    return clis

def checksame(lis1,lis2):
    if len(lis1)!=len(lis2):
        return False
    for i in range(len(lis1)):
        if lis1[i]!=lis2[i]:
            return False
    return True

def dfs(O,i):
    global final_O,P,F,flag
    if i == len(P):
        if len(O[-1][1]) == 0:
            #print(O[0][1])
            final_O = O
            flag=1
            return
        else:
            return
    c1,c2 = read(P,i)
    #2 clauses
    if c1 == "??":
        clauses = obtain(c2,O)
        #list
        clauses = sorted(clauses,key = abs)
        for clause in clauses:
            proofs = obtainlis (O)
            for j in range(len(proofs)):
                if -clause in proofs[j]:
                    newlis = union(clauses, clause, proofs[j], (-clause))
                    dfs(O + [(str(j+1) + 'p',newlis)], i+1)
                    if flag == 1:
                        return
            for j in range(len(F)):
                if -clause in F[j]:
                    newlis = union(clauses, clause, F[j], (-clause))
                    dfs(O + [(str(j+3) + 'f',newlis)], i+1)
                    if flag == 1:
                        return

    elif c2 == "??":
        clauses = obtain(c1,O)
        #list
        clauses = sorted(clauses,key = abs)
        for clause in clauses:
            proofs = obtainlis (O)
            for j in range(len(proofs)):
                if -clause in proofs[j]:
                    newlis = union(clauses, clause, proofs[j], (-clause))
                    dfs(O + [(str(j+1) + 'p',newlis)], i+1)
                    if flag == 1:
                        return
            for j in range(len(F)):
                if -clause in F[j]:
                    newlis = union(clauses, clause, F[j], (-clause))
                    dfs(O + [(str(j+3) + 'f',newlis)], i+1)
                    if flag == 1:
                        return

    else:
        clauses1 = obtain(c1,O)
        clauses2 = obtain(c2,O)
        clauses1 = sorted(clauses1,key = abs)
        for clause in clauses1:
            if -clause in clauses2:
                newlis = union(clauses, clause, clauses2, (-clause))
                dfs(O + [('',newlis)], i+1)
                if flag == 1:
                    return
    
    
def output(type, final_lis,output_file):
    global P
    if type == False:
        final_output = ''
        for x in P:
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
            final_output+='\n'
        output_file.write(final_output)
    else:
        final_output = ''
        
        for i in range(len(final_lis)):
            final_lis[i] = (final_lis[i][0],sorted(final_lis[i][1],key = abs))
            #print(final_lis[i][1])
            if final_lis[i][0] == '':
                continue
            c1,c2 = read(P,i)
            if c1 == '??':
                final_output = final_output + final_lis[i][0] + ' ' + c2 +' '
            elif c2 == '??':
                final_output = final_output + c1 + ' ' + final_lis[i][0] +' '
            else:
                final_output = final_output + c1 + ' ' + c2 + ' '
            for x in final_lis[i][1]:
                final_output += str(x) + ' '
            final_output += '0\n'
        output_file.write(final_output)

def solve(formula_path, proof_path, output_path):
    formula = open(formula_path, "r").read()
    global F,P

    formula = formula.split('\n')
    for i in range(2,len(formula)):
        F.append(obtain_prop(formula[i]))

    proof = open(proof_path,"r").read()
    proof = proof.split('\n')
    if proof[-1] == '':
        proof.pop(-1)
    output_file = open(output_path,"w")
    #F is formula file

    #P is proof file

    for i in range(len(proof)):
        P.append(proof[i])

    dfs([],0)
    output(final_O!=-1,final_O,output_file)

#solve('formula1.txt','proof_with_holes1.txt','output.txt')