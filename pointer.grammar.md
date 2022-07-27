```
Grammar is:
CFG:(V = {E, V, S},
T = {*, x, =},
P = {V->*E, E->V, V->x, S->E, S->V=E},
S = S)

```
| | * | = | x |
| - | - | - | - |
| E | {E->V} | set() | {E->V} | 
| S | {S->E, S->V=E} | set() | {S->E, S->V=E} | 
| V | {V->*E} | set() | {V->x} | 
