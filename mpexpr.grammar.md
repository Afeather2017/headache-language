```
Grammar is:
CFG:(V = {F, T, <EP>, <TP>, E},
T = {i, $, +, ), (, *},
P = {<TP>->*F<TP>, <TP>->'', E->T<EP>, T->F<TP>, <EP>->'', <EP>->+T<EP>, F->(E), F->i, S->E$},
S = E)

```
| | $ | ( | ) | * | + | i |
| - | - | - | - | - | - | - |
| EP | <EP>->'' |  | <EP>->'' |  | <EP>->+T<EP> |  | 
| TP | <TP>->'' |  | <TP>->'' | <TP>->*F<TP> | <TP>->'' |  | 
| E |  | E->T<EP> |  |  |  | E->T<EP> | 
| F |  | F->(E) |  |  |  | F->i | 
| T |  | T->F<TP> |  |  |  | T->F<TP> | 
