```
Grammar is:
CFG:(V 26 = {<VD>, <FA>, <EX>, <FD>, <VN>, <EB>, <IF>, <R'>, <ST>, <CA>, <VL>, <PR>, <SO>, <X'>, <E'>, <ER>, <ES>, <B'>, <AP>, <RT>, <TE>, <EP>, <BL>, <EL>, <LP>, <T'>},
T 29 = {m, =, -, %, r, $, (, l, v, i, ,, }, /, a, ), s, {, q, ;, n, c, g, f, e, <, o, *, >, +},
P 55 = {<EL>->e<BL>, <BL>->{<ST>}, <B'>->q<EP><B'>, <E'>->-<TE><E'>, <B'>->g<EP><B'>, <T'>->%<FA><T'>, <ST>-><EX>;<ST>, <B'>->s<EP><B'>, <T'>->/<FA><T'>, <FA>->i<CA>, <R'>->o<EB><R'>, <ST>-><RT><ST>, <IF>->f(<EX>)<BL><EL>, <X'>->'', <B'>->><EP><B'>, <EB>-><EP><B'>, <PR>-><ST>, <LP>->l(<EX>)<BL>, <B'>->'', <FA>->-<FA>, <AP>->'', <CA>->(<ES>), <AP>->,<ES>, <ES>-><ER><AP>, <ST>-><VD><ST>, <ST>->'', <FA>->(<ER>), <PR>-><FD><PR>, <E'>->+<TE><E'>, <T'>->'', <EP>-><TE><E'>, <ST>-><IF><ST>, <R'>->a<EB><R'>, <EX>-><ER><X'>, <ES>->'', <VD>->vi;, <T'>->*<FA><T'>, <RT>->r<EX>;, <X'>->=<ER><X'>, <ER>-><EB><R'>, <E'>->'', <FD>->ci(<VL>)<BL>, <VN>->,<VL>, <EL>->'', <CA>->'', <VN>->'', <TE>-><FA><T'>, <VL>->'', <FA>->m, <VL>->vi<VN>, <ST>-><LP><ST>, <R'>->'', <B'>-><<EP><B'>, <B'>->n<EP><B'>, <SO>-><PR>$},
S = <SO>)

```
| | $ | % | ( | ) | * | + | , | - | / | ; | < | = | > | a | c | e | f | g | i | l | m | n | o | q | r | s | v | { | } |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| AP |  |  |  | `AP->` |  |  | `AP->,ES` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
| B' |  |  |  | `B'->` |  |  | `B'->` |  |  | `B'->` | `B'-><EPB'` | `B'->` | `B'->>EPB'` | `B'->` |  |  |  | `B'->gEPB'` |  |  |  | `B'->nEPB'` | `B'->` | `B'->qEPB'` |  | `B'->sEPB'` |  |  |  | 
| BL |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `BL->{ST}` |  | 
| CA |  | `CA->` | `CA->(ES)` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` | `CA->` |  |  |  | `CA->` |  |  |  | `CA->` | `CA->` | `CA->` |  | `CA->` |  |  |  | 
| E' |  |  |  | `E'->` |  | `E'->+TEE'` | `E'->` | `E'->-TEE'` |  | `E'->` | `E'->` | `E'->` | `E'->` | `E'->` |  |  |  | `E'->` |  |  |  | `E'->` | `E'->` | `E'->` |  | `E'->` |  |  |  | 
| EB |  |  | `EB->EPB'` |  |  |  |  | `EB->EPB'` |  |  |  |  |  |  |  |  |  |  | `EB->EPB'` |  | `EB->EPB'` |  |  |  |  |  |  |  |  | 
| EL | `EL->` |  | `EL->` |  |  |  |  | `EL->` |  |  |  |  |  |  |  | `EL->eBL` | `EL->` |  | `EL->` | `EL->` | `EL->` |  |  |  | `EL->` |  | `EL->` |  | `EL->` | 
| EP |  |  | `EP->TEE'` |  |  |  |  | `EP->TEE'` |  |  |  |  |  |  |  |  |  |  | `EP->TEE'` |  | `EP->TEE'` |  |  |  |  |  |  |  |  | 
| ER |  |  | `ER->EBR'` |  |  |  |  | `ER->EBR'` |  |  |  |  |  |  |  |  |  |  | `ER->EBR'` |  | `ER->EBR'` |  |  |  |  |  |  |  |  | 
| ES |  |  | `ES->ERAP` | `ES->` |  |  |  | `ES->ERAP` |  |  |  |  |  |  |  |  |  |  | `ES->ERAP` |  | `ES->ERAP` |  |  |  |  |  |  |  |  | 
| EX |  |  | `EX->ERX'` |  |  |  |  | `EX->ERX'` |  |  |  |  |  |  |  |  |  |  | `EX->ERX'` |  | `EX->ERX'` |  |  |  |  |  |  |  |  | 
| FA |  |  | `FA->(ER)` |  |  |  |  | `FA->-FA` |  |  |  |  |  |  |  |  |  |  | `FA->iCA` |  | `FA->m` |  |  |  |  |  |  |  |  | 
| FD |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `FD->ci(VL)BL` |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
| IF |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `IF->f(EX)BLEL` |  |  |  |  |  |  |  |  |  |  |  |  | 
| LP |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `LP->l(EX)BL` |  |  |  |  |  |  |  |  |  | 
| PR | `PR->ST` |  | `PR->ST` |  |  |  |  | `PR->ST` |  |  |  |  |  |  | `PR->FDPR` |  | `PR->ST` |  | `PR->ST` | `PR->ST` | `PR->ST` |  |  |  | `PR->ST` |  | `PR->ST` |  |  | 
| R' |  |  |  | `R'->` |  |  | `R'->` |  |  | `R'->` |  | `R'->` |  | `R'->aEBR'` |  |  |  |  |  |  |  |  | `R'->oEBR'` |  |  |  |  |  |  | 
| RT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `RT->rEX;` |  |  |  |  | 
| SO |  |  | `SO->PR$` |  |  |  |  | `SO->PR$` |  |  |  |  |  |  | `SO->PR$` |  | `SO->PR$` |  | `SO->PR$` | `SO->PR$` | `SO->PR$` |  |  |  | `SO->PR$` |  | `SO->PR$` |  |  | 
| ST | `ST->` |  | `ST->EX;ST` |  |  |  |  | `ST->EX;ST` |  |  |  |  |  |  |  |  | `ST->IFST` |  | `ST->EX;ST` | `ST->LPST` | `ST->EX;ST` |  |  |  | `ST->RTST` |  | `ST->VDST` |  | `ST->` | 
| T' |  | `T'->%FAT'` |  | `T'->` | `T'->*FAT'` | `T'->` | `T'->` | `T'->` | `T'->/FAT'` | `T'->` | `T'->` | `T'->` | `T'->` | `T'->` |  |  |  | `T'->` |  |  |  | `T'->` | `T'->` | `T'->` |  | `T'->` |  |  |  | 
| TE |  |  | `TE->FAT'` |  |  |  |  | `TE->FAT'` |  |  |  |  |  |  |  |  |  |  | `TE->FAT'` |  | `TE->FAT'` |  |  |  |  |  |  |  |  | 
| VD |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `VD->vi;` |  |  | 
| VL |  |  |  | `VL->` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `VL->viVN` |  |  | 
| VN |  |  |  | `VN->` |  |  | `VN->,VL` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
| X' |  |  |  | `X'->` |  |  |  |  |  | `X'->` |  | `X'->=ERX'` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
