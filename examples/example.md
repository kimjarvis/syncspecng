{{import="import.txt", head=2, tail=2, eof=True}}a
b
line 1
line 2
line 3
c
d{{}}

{{source="text1", head=2, tail=2 }}1
2
line A
line B
line C
3
4{{}}

{{include="text1", head=2, tail=2 }}a
b
line A
line B
line C
c
d{{}}
