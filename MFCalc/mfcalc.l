%{
#include "calc.h"
#include "mfcalc.tab.h"
#include <stdlib.h>
%}
%%

[0-9]+"."*[0-9]* { 	yylval.NUM = atof(yytext); 
				  	return NUM;	}

[a-z][a-z0-9]*	{ 	symrec* s = getsym(yytext);
					if(!s) 
						s = putsym(strdup(yytext), VAR);
					yylval.VAR = s;
			  		return s->type;
				}	

":q"			{	exit(0);	}

[ ]

\n 				{	return '\n';	}

[+-/*=()^] 		{	return *yytext;	}

%%
