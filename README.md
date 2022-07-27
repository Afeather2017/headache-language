# headache-language
You could change grammar by a grammar file in `program.grammar`, and try to run `llparsergen.py program.grammar`. You may should change you grammar when program shows a Warn that `This grammar is not LL(1)`.
You may think that "what if I runs other script?" I don't know what'll happend. I just completed the LL(1) compiler.
There is no abstruct tree because that I'd like to finish the mission directly by the grammar.
You could see that there is several line with `#` in the front, that is the corrosponding command.
You could change is in this form: `# when_to_pop command %convert_descriptor`.
when_to_pop means pop the corrosponding command when meet the count from right to left with start 0.
For example:
```
LP -> 'l(' EX ')' BL
# 0 pop
# 0 while_if -%t
# 1 %w:
# 1 while %l
# 4 :%t
```
`LP -> 'l(' EX ')' BL` is the grammar, which is followed by corrosponding command.
And `# 0 pop` means when `BL` poped, the command appear to program.
Also, `# 4 :%t` means when the fourth charactor `l` poped, `:%t` added to the program.
And, `:%t` means a JUMP-TAG, program'll jumps here for some of situations.
