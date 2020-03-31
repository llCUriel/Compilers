#include <stdlib.h> /* malloc. */
#include <string.h> /* strlen. */
#include "calc.h"
symrec * putsym (char const *name, int sym_type)
{
  symrec *res = (symrec *) malloc (sizeof (symrec));
  res->name = strdup (name);
  res->type = sym_type;
  res->value.var = 0; /* Set value to 0 even if fun. */
  res->next = sym_table;
  sym_table = res;
  return res;
}


symrec * getsym (char const *name)
{
  for (symrec *p = sym_table; p; p = p->next)
	if (strcmp (p->name, name) == 0)
	  return p;
  return NULL;
}

