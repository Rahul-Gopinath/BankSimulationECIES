# BankSimulationECIES

The objectives of secure banking application: 
1. Implements class level-based access for viewing of users’ personal records. 
2. Gives an idea about how transactions are secured in a bank. 
3. Allows the user to encrypt his/her personal data using ECIES.
4. Maintains a record of the users’ transactions and provides security for it. 

Methodology adapted:
Key generation: The parameters that must be agreed upon are the elliptic curve parameters: p (prime no.) as the finite field size, a and b as the curve parameters, G as the generator point, n as the order of G, and h as the cofactor. Let P be the private key of the user. Then, the public key Q can be determined by the expression: 
Q=[P].G 

Encryption Scheme: 
Algorithm used- ECIES (Elliptic Curve Integrated Encryption Scheme): 
INPUT: Q where Q is the public key of other party, m where m is the intended message   
OUTPUT: e where e is the encrypted message, C (x,y) where C is the chosen point 
  ALGORITHM: 
  1. Choose random value k [1,n-1]  
2. C = [k].G 
3. R = [k].Q  
4. e = (Rx*m) modulo p  
5. Return (e,C) 

Decryption Scheme:  
INPUT: e where e is the encrypted message  
C where C is the chosen point  
Pk where Pk is the private key of receiver  
OUTPUT: d where d is the decoded message  
ALGORITHM:  
1. R = [Pk].C  
2. d = (e*(Rx)-1) modulo p  
3. Return(d)
