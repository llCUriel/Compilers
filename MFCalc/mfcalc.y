%{
#include <stdio.h>
#include <math.h>
#include "calc.h"   /* Contains definition of 'symrec'. */
int yylex (void);
void yyerror (char const * error){
	printf("Hay un error %s\n", error);
}
%}



%define api.value.type union /* Generate YYSTYPE from these types: */
%token <double>  NUM     /* Double precision number. */
%token <symrec*> VAR FUN /* Symbol table pointer: variable/function. */
%type  <double>  exp

%precedence '='
%left '-' '+'
%left '*' '/'
%precedence NEG /* negation--unary minus */
%right '^'      /* exponentiation */



%% /* The grammar follows. */

input:
  %empty
| input line
;


line:
  '\n'
| exp '\n'   { printf ("\t%.10g\n", $1); }
| error '\n' { yyerrok;                }
;


exp:
  NUM
| VAR                { $$ = $1->value.var;              }
| VAR '=' exp        { $$ = $3; $1->value.var = $3;     }
| FUN '(' exp ')'    { $$ = $1->value.fun ($3);         }
| exp '+' exp        { $$ = $1 + $3;                    }
| exp '-' exp        { $$ = $1 - $3;                    }
| exp '*' exp        { $$ = $1 * $3;                    }
| exp '/' exp        { $$ = $1 / $3;                    }
| '-' exp  %prec NEG { $$ = -$2;                        }
| exp '^' exp        { $$ = pow ($1, $3);               }
| '(' exp ')'        { $$ = $2;                         }
;

/* End of grammar. */
%%


/* The lexical analyzer returns a double floating point
  number on the stack and the token NUM, or the numeric code
  of the character read if not a number.  It skips all blanks
  and tabs, and returns 0 for end-of-input.  */

#include <ctype.h>


struct init
{
  char const *name;
  func_t *fun;
};


struct init const arith_funs[] = {
  { "atan", atan },
  { "cos",  cos  },
  { "exp",  exp  },
  { "ln",   log  },
  { "sin",  sin  },
  { "sqrt", sqrt },
  { 0, 0 },
};


/* The symbol table: a chain of 'struct symrec'. */
symrec *sym_table;


/* Put arithmetic functions in table. */
static void init_table (void){
  for (int i = 0; arith_funs[i].name; i++)
    {
      symrec *ptr = putsym (arith_funs[i].name, FUN);
      ptr->value.fun = arith_funs[i].fun;
    }
}

int main (int argc, char const* argv[])

{
  /* Enable parse traces on option -p. 
  if (argc == 2 && strcmp(argv[1], "-p") == 0)
    yydebug = 1;
  */
  init_table ();
  return yyparse ();
}

