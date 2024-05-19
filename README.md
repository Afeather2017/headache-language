# headache-language

这是一个简易的编译器与编译器套件，主要是两年前我写的代码，以后考虑可能重构，它有：

1. 使用正则实现的 lexer
2. 翻译 LL(1)、LALR(1)、LR(1) 文法的分析表生成
3. 利用栈的无抽象文法树的 LL(1)、LR(1) 文法语言转换为中间代码的翻译，类似于制导翻译
4. 使用二元式、利用栈的中间代码的执行器 icode.py
5. 一些使用例子

## 终结符映射

在 `*compiler` 中，有 `Func`、`Var` 等到关键字到某个终结符的映射，他们映射到 c、v 上。

而字符串、整数都当作字面量，映射到 m 上。

如果你想添加其他关键字，添加即可，修改也是同理。

## icode.py 的执行原理

因为 icode.py 使用的是 python，所以所有类型检查实际上都是 python 做的。它只支持二元式。

### Label

格式为

```
LABLE:
... 指令
back
```

back 表示了该 label 的结束

### Func

格式为:

```
func FUNC_NAME:
... 指令
func_back
```

同理，`func_back` 表示了该 func 的结束

### 执行原理

它执行中间代码使用了 3 个栈：

```
label_stack: ['label 名': 行号, ...]
prog_stack : [{'变量名': 值, ...}, ...]
temp_stack : [计算中间结果, ...]
```

当要执行加法的时候，实际上只操作了 `temp_stack`。如 `r = 1 + r` 翻译为的中间代码:

```
push r
push 1
add
pop r
```

表示先将 r 和 1 压入 `temp_stack`，add 取出这两个值计算后，结果再次压入栈中，最后 pop r 将栈顶值给 r。

每一个栈帧都使用 Spliter 分隔。这是为了方便在函数返回时，或者某个 label 执行完的时候清理栈。

`label_stack` 的 `'label 名': 行号` 是为了解决函数调用结束、返回的时候无法定位到上一层函数的调用位置的问题。

考虑以下代码:

```c
int func() {}
int main() { func(); puts("1");}
```

main 调用 func，func 结束后要调用 puts，可是如果不记录 main 调用 func 的位置，将无法确定下一个语句。

## 文法文件 .grammar 的格式

这是纯文本格式文件。第一行是所有终结符，第二行是所有非终结符，第三行是起始符号，剩下的是文法规则。

文法规则格式：

```
A -> B 'ccd'
## 注释
# i   解析完倒数第 i 个符号的动作
```

终结符需要用单引号括起来。上面 'ccd' 表示了 3 个终结符。

这一行

```
# i   解析完倒数第 i 个符号的动作
```

的含义是，解析完倒数第 i 个符号的时候做的动作。如下文法

```
## 倒数第 2  1  0 个符号
E ->      T '+' E
# 2 add
```

表示 T 解析完成后，马上执行 add。
