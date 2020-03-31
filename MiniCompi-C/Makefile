C-compiler:lex.yy.o subc-compiler.tab.o
	gcc subc-compiler.tab.o lex.yy.o -o C-compiler -lfl -lm

lex.yy.o: lex.yy.c subc-compiler.tab.c
	gcc -c subc-compiler.tab.c lex.yy.c

lex.yy.c: subc-compiler.l
	flex --header-file=flex.h subc-compiler.l 

subc-compiler.tab.c: subc-compiler.y
	bison -d subc-compiler.y

clean:
	rm -fv C-compiler flex.h lex.yy.c lex.yy.o subc-compiler.tab.c subc-compiler.tab.h subc-compiler.tab.o
