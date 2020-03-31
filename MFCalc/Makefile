mfcalc: mfcalc.lex.o mfcalc.tab.o calc.o
	gcc calc.o mfcalc.lex.o mfcalc.tab.o -o mfcalc -lfl -lm

mfcalc.lex.o: mfcalc.lex.c mfcalc.tab.c calc.c
	gcc -c calc.c mfcalc.lex.c mfcalc.tab.c

mfcalc.lex.c: mfcalc.l
	flex -omfcalc.lex.c mfcalc.l 

mfcalc.tab.c: mfcalc.y
	bison -d mfcalc.y

clean:
	rm -fv calc.o mfcalc mfcalc.lex.c mfcalc.lex.o mfcalc.tab.c mfcalc.tab.h mfcalc.tab.o
