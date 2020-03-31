%{
#include "subc-compiler.tab.h"
#include <stdlib.h>
%}
alpha [a-zA-Z]
digit [0-9]

%%
[ \t]			;
[ \n]  			{ yylineno = yylineno + 1;}

"int"			return INT;

"while"			return WHILE;
"if"			return IF;

{digit}+       	{ 	yylval.NUM = atoi(yytext); 
				  	return NUM;	}

{alpha}({alpha}|{digit})* 	{yylval.ID = yytext;
							return ID;}

"="     		return ASGN;

"<="    		{yylval.LE = yytext;
							return LE;}
">="    		{yylval.GE = yytext;
							return GE;}
"=="    		{yylval.EQ = yytext;
							return EQ;}
"!="    		{yylval.NE = yytext;
							return NE;}
">"				{yylval.GT = yytext;
							return GT;}
"<"				{yylval.LT = yytext;
							return LT;} /*
"||" 			return LOR;
"&&"  			return LAND; */
[+-/*=()^] 		{	return *yytext;	}

\/\/.* 				;
\/\*(.*\n)*.*\*\/ 	;
.       		return yytext[0];
%%
