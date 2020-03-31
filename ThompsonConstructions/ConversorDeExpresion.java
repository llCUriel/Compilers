
import java.util.Stack;

public class ConversorDeExpresion {

    private Stack< String> E;

    private Stack< String> P;

    private Stack< String> S;

    public ConversorDeExpresion() {
        this.E = new Stack<String>();
        this.P = new Stack<String>();
        this.S = new Stack<String>();
    }

    public String convertirExpresionInfijaAPostfija(String expresionInfija) {

        String expr = depurarExpresionInfija(expresionInfija);
        String[] arrayInfix = expr.split(" ");

        for (int i = arrayInfix.length - 1; i >= 0; i--) {
            E.push(arrayInfix[i]);
        }

        try {
            while (!E.isEmpty()) {
                switch (establecerPrioridadDeOperador(E.peek())) {
                    case 1:
                        P.push(E.pop());
                        break;
                    case 3:
                        
                    case 4:
                        while (establecerPrioridadDeOperador(P.peek()) >= establecerPrioridadDeOperador(E.peek())) {
                            S.push(P.pop());
                        }
                        P.push(E.pop());
                        break;
                    case 2:
                        while (!P.peek().equals("(")) {
                            S.push(P.pop());
                        }
                        P.pop();
                        E.pop();
                        break;
                    default:
                        S.push(E.pop());
                }
            }

            return S.toString().replaceAll("[\\]\\[,]", "");

        } catch (Exception ex) {
            return null;
        }
    }

    private String depurarExpresionInfija(String expresionInfija) {
        expresionInfija = expresionInfija.replaceAll("\\s+", "");
        expresionInfija = "(" + expresionInfija + ")";
        String simbols = "+|*.()";
        String str = "";

        for (int i = 0; i < expresionInfija.length(); i++) {
            if (simbols.contains("" + expresionInfija.charAt(i))) {
                str += " " + expresionInfija.charAt(i) + " ";
            } else {
                str += expresionInfija.charAt(i);
            }
        }
        return str.replaceAll("\\s+", " ").trim();
    }

    private int establecerPrioridadDeOperador(String operador) {
        int prf = 99;

        if (operador.equals("*") || operador.equals("+")) {
            prf = 5;
        }
        if (operador.equals("|") || operador.equals(".")) {
            prf = 3;
        }
        if (operador.equals(")")) {
            prf = 2;
        }
        if (operador.equals("(")) {
            prf = 1;
        }
        return prf;
    }

}
