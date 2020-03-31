%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "flex.h"
extern FILE *fp;
FILE * f1;
void yyerror(char *s);

void begin_main();
void end_main();
void codegen_assign(int);
void begin_if();
void begin_while();
void end_if();
void end_while();

void check();
void push();
int get_Value();

void STMT_DECLARE();

void printCode();

%}
%define api.value.type union /* Generate YYSTYPE from these types: */
%token INT
%token WHILE
%token IF
%token <int> NUM 
%token <char *> ID
%right ASGN 
%left <char *> EQ NE 
%left <char *> LE GE LT GT
%left '+' '-' 
%left '*' '/'
%type <int> EXP

%%

pgmstart		: TYPE ID {push();begin_main();} '(' ')' STMTS {end_main();}
				;

TYPE			: INT
				;

STMTS 			: '{' STMT1 '}'|
				;
STMT1			: STMT  STMT1
				|
				;

STMT 			: STMT_DECLARE
				| STMT_ASSGN  
				| STMT_IF
				| STMT_WHILE
				| ';'
				;

STMT_DECLARE 	: TYPE ID {STMT_DECLARE();} IDS
				;

STMT_ASSGN		: ID {push();check();}ASGN EXP {codegen_assign($4);} ';'
				;

IDS 			: ';'
				| ','  ID {STMT_DECLARE();} IDS 
				;

EXP				: EXP '+' EXP {$$=$1+$3;}
				| EXP '-' EXP {$$=$1-$3;}
				| EXP '*' EXP {$$=$1*$3;}
				| ID {check();$$ = get_Value(); }
				| NUM 
				;


STMT_IF 		: IF '('L_EXP ')'  {begin_if();} STMTS {end_if();}
				;

STMT_WHILE		: WHILE '(' L_EXP ')' {begin_while();} WHILEBODY  
				;

WHILEBODY		: STMTS {end_while();}
				| STMT {end_while();}
				;

L_EXP			: ID {check();push();} L_OP {push();} NUM {push();}
				;

L_OP 			: LT
		   		| LE
				| GT
				| GE
				| NE
				| EQ
				;

%%

#include <ctype.h>

char temp[20];
int i=0;

char st[1000][10];
int top=0;

int label[200];
int ltop=0;
int lab=1;

struct Table{
	char id[20];
	int dir;
	int value;
}table[10000];
int tableCount=0;

void yyerror(char *s){
	printf("Syntax Error en la linea: %d\n%s %s\n", yylineno, s, yytext );
}

void begin_main(){
	fprintf(f1,"\t.globl\t%s\n", st[top]);
	fprintf(f1,"\t.type\t%s, @function\n", st[top]);
	fprintf(f1,"%s:\n",st[top]);
	fprintf(f1,".LFB0:\n");
	fprintf(f1,"\t.cfi_startproc\n");
	fprintf(f1,"\tpushq\t%rbp\n");
	fprintf(f1,"\t.cfi_def_cfa_offset 16\n");
	fprintf(f1,"\t.cfi_offset 6, -16\n");
	fprintf(f1,"\tmovq\t%rsp, %rbp\n");
	fprintf(f1,"\t.cfi_def_cfa_register 6\n");
}

void end_main(){
	fprintf(f1,"\tmovl\t$0, %%eax\n");
	fprintf(f1,"\tpopq\t%rbp\n");
	fprintf(f1,"\t.cfi_def_cfa 7, 8\n");
	fprintf(f1,"\tret\n");
	fprintf(f1,"\t.cfi_endproc\n");
	fprintf(f1,".LFE0:\n");
	fprintf(f1,"\t.size\t%s, .-%s\n", st[top], st[top]);
	top--;
}

void codegen_assign(int a) {
	for(i = 0; i < tableCount; i++) {
		if(!strcmp(table[i].id,st[top])) {
			table[i].value = a;
			fprintf(f1,"\tmovl\t$%d, -%d(%rbp)\n", a, 4*table[i].dir);
			break;
		}
	}
	top--;
}

void begin_if(){
	char comp[4];
	int mns =0;
	if (!strcmp(st[top-1], "<")){strcpy(comp, "jg");mns=1;}
	else if(!strcmp(st[top-1], ">")){strcpy(comp, "jle");}
	else if(!strcmp(st[top-1], "<=")){strcpy(comp, "jg");}
	else if(!strcmp(st[top-1], ">=")){strcpy(comp, "jle"); mns=1;}
	else if(!strcmp(st[top-1], "==")){strcpy(comp, "jne");}
	else if(!strcmp(st[top-1], "!=")){strcpy(comp, "je");}

	for(i = 0; i < tableCount; i++) {
		if(!strcmp(table[i].id,st[top-2])) {
			fprintf(f1, "\tcmpl\t$%d, -%d(%rbp)\n", atoi(st[top])-mns, 4*table[i].dir);
			break;
		}
	}
	
	label[++ltop] = ++lab;
	fprintf(f1, "\t%s\t.L%d\n",comp,lab);
	top-=3;
}

void end_if(){
	fprintf(f1,	".L%d:\n", label[ltop]);
	ltop--;
}

void begin_while(){
	label[++ltop] = ++lab;
	fprintf(f1, "\tjmp\t.L%d\n", lab);
	label[++ltop] = ++lab;
	fprintf(f1, ".L%d:\n",lab);

}

void end_while(){
	char comp[4];
	int mns =0;
	if (!strcmp(st[top-1], "<")){strcpy(comp, "jle");mns=1;}
	else if(!strcmp(st[top-1], ">")){strcpy(comp, "jg");}
	else if(!strcmp(st[top-1], "<=")){strcpy(comp, "jle");}
	else if(!strcmp(st[top-1], ">=")){strcpy(comp, "jg"); mns=1;}
	else if(!strcmp(st[top-1], "==")){strcpy(comp, "je");}
	else if(!strcmp(st[top-1], "!=")){strcpy(comp, "jne");}

	for(i = 0; i < tableCount; i++) {
		if(!strcmp(table[i].id,st[top-2])) {
			fprintf(f1, ".L%d:\n", label[ltop-1]);
			fprintf(f1, "\tcmpl\t$%d, -%d(%rbp)\n", atoi(st[top])-mns, 4*table[i].dir);
			break;
		}
	}
	
	fprintf(f1, "\t%s\t.L%d\n",comp,label[ltop]);
	ltop-=2;
	top-=3;	
}

void push(){
  	strcpy(st[++top],yytext);
}

int get_Value(){
	strcpy(temp,yytext);
	for(i = 0; i < tableCount; i++) {
		if(!strcmp(table[i].id,temp)) {
			return table[i].value;
		}
	}

}

void check() {
	char temp[20];
	strcpy(temp,yytext);
	int flag=0;
	for(i = 0; i < tableCount; i++) {
		if(!strcmp(table[i].id,temp)) {
			flag=1;
			break;
		}
	}

	if(!flag) {
		yyerror("Variable no declarada:");
		exit(0);
	}
}

void STMT_DECLARE() {
	char temp[20];
	int i,flag;
	flag=0;
	strcpy(temp,yytext);
	for(i=0;i<tableCount;i++)
	{
		if(!strcmp(table[i].id,temp))
			{
			flag=1;
			break;
				}
	}
	if(flag)
	{
		yyerror("Se encuentra una declaracion previa de: ");
		exit(0);
	}
	else
	{
		strcpy(table[tableCount].id,temp);
		table[tableCount].dir = tableCount+1;
		tableCount++;
	}
}

void printCode() {
	int Labels[100000];
	char buf[100];
	f1=fopen("output.s","r");
	int flag=0,lineno=1;
	memset(Labels,0,sizeof(Labels));
	while(fgets(buf,sizeof(buf),f1)!=NULL)
	{
		if(buf[0]=='$'&&buf[1]=='$'&&buf[2]=='L')
		{
			int k=atoi(&buf[3]);
			Labels[k]=lineno;
		}
		else
		{
			lineno++;
		}
	}
	fclose(f1);
	f1=fopen("output.s","r");
	lineno=0;

	printf("\n********************* Ensamblador ***************************\n\n");
	while(fgets(buf,sizeof(buf),f1)!=NULL)
	{
		//printf("%s",buf);
		if(buf[0]=='$'&&buf[1]=='$'&&buf[2]=='L')
		{
			;
		}
		else
		{
			flag=0;
			lineno++;
			printf("%3d:\t",lineno);
			int len=strlen(buf),i,flag1=0;
			for(i=len-3;i>=0;i--)
			{
				if(buf[i]=='$'&&buf[i+1]=='$'&&buf[i+2]=='L')
				{
					flag1=1;
					break;
				}
			}
			if(flag1)
			{
				buf[i]=='\0';
				int k=atoi(&buf[i+3]),j;
				//printf("%s",buf);
				for(j=0;j<i;j++)
					printf("%c",buf[j]);
				printf(" %d\n",Labels[k]);
			}
			else printf("%s",buf);
		}
	}
	fclose(f1);
}

int main(int argc, char *argv[]){
	yyin = fopen(argv[1], "r");
	f1=fopen("output.s","w");
	
   if(!yyparse())
		printf("Analisis completo\n");	
	else{
		printf("Error al analizar...\n");
		exit(0);
	}
	
	fclose(yyin);
	fclose(f1);
	printCode();
    return 0;
}
