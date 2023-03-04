# Circuit-Solver
-You shall place the netlist in the dist folder ; besides the .exe file


NetList Format
-----------------------

W  value                                                                                     //The entered angular frequency

R<num> node1 node2 resistance
  
C<num> node1 node2 capacitance
  
L<num> node1 node2 Inductance
  
V<num> node1 node2 value phase                                           // value refers to the magnitude  
  
I<num> node1 node2 value phase                                            // value refers to the magnitude
  
F<num> node1 node2 ElemID DependencyFactor                    //ElemID is the ID of the element where the cuurent passing through it is the same current the cccs depends on 
  
H<num> node1 node2 ElemID DependencyFactor                    //ElemID is the ID of the element where the cuurent passing through it is the same current the cccs depends on 
  
G<num> node1 node2 Dnode1 Dnode2 DependencyFactor   //Dnode1 and Dnode2 are the nodes where the controlled voltage is across    
  
E<num> node1 node2 Dnode1 Dnode2 DependencyFactor    //Dnode1 and Dnode2 are the nodes where the controlled voltage is across



Elements ID
------------------

R is the ID for Resistor

C is the ID for Capacitor

L is the ID for Inductor

I is the ID for InDependent cs

V is the ID for InDependent vs

F is the ID for cccs

H is the ID for ccvs

G is the ID for vccs

E is the ID for vcvs

-In any current source: the node at the arrow's tail is ('node1') in the netlist, and the node at the arrow's head is ('node2')  (i.e. a positive current flows into node1 and out of node2.)

-In any Voltage source: ('node1') is the positive node to be written in the netlist and ('node2') is the negative one

-But for the ccvs ('H') : ('node1') is the negative node to be written in the netlist and ('node2') is the positive one


-If you have in your circuit more than one current controlled source that depends on the same current, you shall write at the end of these sources 'repeated' except for the first one

i.e 

W 5

R1 3 0 1000

V1 3 1 5 0

C1 1 0 0.015

F1 2 1 R1 35

R2 2 4 5000

H1 2 5 R1 5 repeated

R3 5 4 2500

L1 4 0 0.01

Example circuits
-----------------------
e.g1 

W 1

I1 0 1 3 0

C1 0 1 0.333333

R1 1 2 4

V1 1 2 10 45

L1 2 0 6

R2 2 0 12


(Note that: Fractions like 22/7 are not allowed)

e.g2

W 3000

V1 1 0 20 0

R1 1 2 2000

C1 2 0 0.000001

L1 2 3 2

R2 2 4 3000

E1 4 0 3 0 2

R3 3 0 1000


e.g3

W 1

I1 0 1 16 60

R1 0 1 2

V1 1 6 48 0

C1 6 5 4

R2 1 2 1

L1 2 3 2

C2 3 0 1

L2 3 4 2

R3 4 5 1

H1 0 5 R2 4


e.g4

W  1

R1 1 0 4

C1 2 1 0.5

I1 2 3 5 0

R2 2 4 8

L1 4 3 4

G1 0 3 2 3 0.2


e.g5

W 1

I1 0 1 15 0

R1 1 2 2

C1 2 0 0.25

R2 1 3 4

L1 3 4 3

F1 4 0 R1 0.5


(Note that: C1 is written from '2' to '0' as the 'i0' supposed to flow and R1 is written from '1' to '2' as the 'i0' supposed to flow )
