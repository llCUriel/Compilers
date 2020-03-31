%{
  #include<stdio.h>
  int cc=0, cl=0;
%}
%%
\n {cl++; cc++;}
. {cc++;}
%%
int main(void){
  yylex();
  printf("chars %d, lineas %d", cc, cl);
  return 0;
}
