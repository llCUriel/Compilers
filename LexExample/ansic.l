D			[0-9]
L			[a-zA-Z_]
H			[a-fA-F0-9]
E			[Ee][+-]?{D}+
FS			(f|F|l|L)
IS			(u|U|l|L)*

%{
#include <stdio.h>

%}

%%
"/*"			{ }

"auto"			{ printf("<span class='res'>%s</span>", yytext); }
"break"			{ printf("<span class='res'>%s</span>", yytext); }
"case"			{ printf("<span class='res'>%s</span>", yytext); }
"char"			{ printf("<span class='res'>%s</span>", yytext); }
"const"			{ printf("<span class='res'>%s</span>", yytext); }
"continue"		{ printf("<span class='res'>%s</span>", yytext); }
"default"		{ printf("<span class='res'>%s</span>", yytext); }
"do"			{ printf("<span class='res'>%s</span>", yytext); }
"double"		{ printf("<span class='res'>%s</span>", yytext); }
"else"			{ printf("<span class='res'>%s</span>", yytext); }
"enum"			{ printf("<span class='res'>%s</span>", yytext); }
"extern"		{ printf("<span class='res'>%s</span>", yytext); }
"float"			{ printf("<span class='res'>%s</span>", yytext); }
"for"			{ printf("<span class='res'>%s</span>", yytext); }
"goto"			{ printf("<span class='res'>%s</span>", yytext); }
"sizeof"		{ printf("<span class='res'>%s</span>", yytext); }
"volatile"		{ printf("<span class='res'>%s</span>", yytext); }
"while"			{ printf("<span class='res'>%s</span>", yytext); }

{L}({L}|{D})*		{ printf("<span class='const'>%s</span>", yytext); }

0[xX]{H}+{IS}?		{ printf("<span class='const'>%s</span>", yytext); }
0{D}+{IS}?		{ printf("<span class='const'>%s</span>", yytext); }
{D}+{IS}?		{ printf("<span class='const'>%s</span>", yytext); }
L?'(\\.|[^\\'])+'	{ printf("<span class='const'>%s</span>", yytext); }

{D}+{E}{FS}?		{ printf("<span class='const'>%s</span>", yytext); }
{D}*"."{D}+({E})?{FS}?	{ printf("<span class='const'>%s</span>", yytext); }
{D}+"."{D}*({E})?{FS}?	{ printf("<span class='const'>%s</span>", yytext); }

L?\"(\\.|[^\\"])*\"	{ printf("<span class='const'>%s</span>", yytext); }

"..."			{ printf("<span class='op'>%s</span>", yytext); }
">>="			{ printf("<span class='op'>%s</span>", yytext); }
"<<="			{ printf("<span class='op'>%s</span>", yytext); }
"+="			{ printf("<span class='op'>%s</span>", yytext); }
"-="			{ printf("<span class='op'>%s</span>", yytext); }
"*="			{ printf("<span class='op'>%s</span>", yytext); }
"/="			{ printf("<span class='op'>%s</span>", yytext); }
"%="			{ printf("<span class='op'>%s</span>", yytext); }
"&="			{ printf("<span class='op'>%s</span>", yytext); }
"^="			{ printf("<span class='op'>%s</span>", yytext); }
"|="			{ printf("<span class='op'>%s</span>", yytext); }
">>"			{ printf("<span class='op'>%s</span>", yytext); }
"<<"			{ printf("<span class='op'>%s</span>", yytext); }
"++"			{ printf("<span class='op'>%s</span>", yytext); }
"--"			{ printf("<span class='op'>%s</span>", yytext); }
"->"			{ printf("<span class='op'>%s</span>", yytext); }
"&&"			{ printf("<span class='op'>%s</span>", yytext); }
"||"			{ printf("<span class='op'>%s</span>", yytext); }
"<="			{ printf("<span class='op'>%s</span>", yytext); }
">="			{ printf("<span class='op'>%s</span>", yytext); }
"=="			{ printf("<span class='op'>%s</span>", yytext); }
"!="			{ printf("<span class='op'>%s</span>", yytext); }
";"			{ printf("<span class='sep'>%s</span>", yytext); }
("{"|"<%")		{ printf("<span class='sep'>%s</span>", yytext); }
("}"|"%>")		{ printf("<span class='sep'>%s</span>", yytext); }
","			{ printf("<span class='sep'>%s</span>", yytext); }
":"			{ printf("<span class='op'>%s</span>", yytext); }
"="			{ printf("<span class='sep'>%s</span>", yytext); }
"("			{ printf("<span class='sep'>%s</span>", yytext); }
")"			{ printf("<span class='sep'>%s</span>", yytext); }
("["|"<:")		{ printf("<span class='sep'>%s</span>", yytext); }
("]"|":>")		{ printf("<span class='op'>%s</span>", yytext); }
"."			{ printf("<span class='op'>%s</span>", yytext); }
"&"			{ printf("<span class='op'>%s</span>", yytext); }
"!"			{ printf("<span class='op'>%s</span>", yytext); }
"~"			{ printf("<span class='op'>%s</span>", yytext); }
"-"			{ printf("<span class='op'>%s</span>", yytext); }
"+"			{ printf("<span class='op'>%s</span>", yytext); }
"*"			{ printf("<span class='op'>%s</span>", yytext); }
"/"			{ printf("<span class='op'>%s</span>", yytext); }
"%"			{ printf("<span class='op'>%s</span>", yytext); }
"<"			{ printf("<span class='op'>%s</span>", yytext); }
">"			{ printf("<span class='op'>%s</span>", yytext); }
"^"			{ printf("<span class='op'>%s</span>", yytext); }
"|"			{ printf("<span class='op'>%s</span>", yytext); }
"?"			{ printf("<span class='op'>%s</span>", yytext); }

[ \t\v\n\f]		{ }
.			{ }

%%

int main(void){
  printf("<!DOCTYPE html><html><head><title>Sample page</title><link rel=\"stylesheet\" href=\"estilo.css\"></head><body>");
  yylex();
  printf("</body></html>");
  return 0;
}
