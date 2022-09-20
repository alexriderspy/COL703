import sys

final_O = -1
P = []
F = []

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
    
def get (c,O):
    line_num = int(c[:-1])
    type = c[-1]
    if type == 'f':
        line_num -=3
        return F[line_num]
    else:
        line_num-=1
        return O[line_num][1]

def getlis (O):
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

def dfs(O,i):
    global final_O
    if i == len(P):
        if len(O[-1][1]) == 0:
            final_O = O
            return
        else:
            return
    c1,c2 = read(P,i)
    #2 clauses
    if c1 == "??":
        clauses = get(c2,O)
        #list
        sorted(clauses,key = abs)
        for clause in clauses:
            proofs = getlis (O)
            for j in range(len(proofs)):
                if -clause in proofs[j]:
                    newlis = union(clauses, clause, proofs[j], (-clause))
                    dfs(O + [(str(j+1) + 'p',newlis)], i+1)
            for j in range(len(F)):
                if -clause in F[j]:
                    newlis = union(clauses, clause, F[j], (-clause))
                    dfs(O + [(str(j+3) + 'f',newlis)], i+1)

    elif c2 == "??":
        clauses = get(c1,O)
        #list
        sorted(clauses,key = abs)
        for clause in clauses:
            proofs = getlis (O)
            for j in range(len(proofs)):
                if -clause in proofs[j]:
                    newlis = union(clauses, clause, proofs[j], (-clause))
                    dfs(O + [(str(j+1) + 'p',newlis)], i+1)
            for j in range(len(F)):
                if -clause in F[j]:
                    newlis = union(clauses, clause, F[j], (-clause))
                    dfs(O + [(str(j+3) + 'f',newlis)], i+1)

    else:
        clauses1 = get(c1,O)
        clauses2 = get(c2,O)
        sorted(clauses1,key = abs)
        for clause in clauses1:
            if -clause in clauses2:
                newlis = union(clauses, clause, clauses2, (-clause))
                dfs(O + [('',newlis)], i+1)
    
    
def output(type, final_lis):
    output_file = open(str(sys.argv[3]),"w")
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
        F.append(get_prop(formula[i]))

    proof = open(proof_path,"r").read()
    proof = proof.split('\n')
    #F is formula file

    #P is proof file

    for i in range(len(proof)):
        P.append(proof[i])

    dfs([],0)
    output(final_O!=-1,final_O)
