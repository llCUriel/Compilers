#include <stdio.h>


int main(){
  printf("<!DOCTYPE html><html><head><title>Sample page</title><link rel=\"stylesheet\" href=\"estilo.css\"></head><body>");
  yylex();
  printf("</body></html>");
  return 0;
}
