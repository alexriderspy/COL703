Type 
python solve.py <formula.txt> <proof.txt>
where formula.txt is the file containing the cnf formula and proof.txt is the file containing the proofs.
eg in my folder, I have proof1, proof2 and proof3 out of which proof1 is correct and the other 2 are wrong, so
type
python solve.py formula.txt proof1.txt
prints : 
Correct
python solve.py formula.txt proof2.txt
prints : 
Incorrect
python solve.py formula.txt proof3.txt
prints : 
Incorrect
