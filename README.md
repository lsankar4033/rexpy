###### What?
rexpy is a regular expression parser built in python, primarily as an exercise.

In the interest of simplicity, I only support the following operations:
1. kleene star, denoted by '*'
2. union, denoted by '|'
3. concatentation
4. parenthesization

###### Why?
I was originally inspired to build this while reading about regular languages and finite automata in Michael
Sipser's excellent [Introduction to the Theory of Computation](https://www.amazon.com/Introduction-Theory-Computation-Michael-Sipser/dp/113318779X).
This book also inspired me to build [pycc](https://github.com/lsankar4033/pycc).

###### How?
Regular expressions are compiled to nondeterministic finite automata (NFA) and matching is then implemented as
a breadth-first search through the NFA while sequentially reading the string. For more on this technique, see
[here](https://swtch.com/~rsc/regexp/regexp1.html).

The main  entry point is the `rexpy.regex.match` method.

Example usage:

```python
> import rexpy.regex
> regex.match("(a|bc)d", "bcd")
True
> regex.match("(a|bc)d", "acd")
False
```

###### TODO
- (optional) convert nested calls in parse code to sequential calls
- add escape characters functionality
- add capture functionality
