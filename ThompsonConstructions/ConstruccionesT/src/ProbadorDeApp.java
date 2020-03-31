
import java.util.LinkedList;

public class ProbadorDeApp {

    private ConversorDeExpresion m;

    public ProbadorDeApp() {

        m = new ConversorDeExpresion();

    }

    public String probarApp(String expresionInfija) {

        String expresionPostFija;

        expresionPostFija = m.convertirExpresionInfijaAPostfija(expresionInfija);

        return expresionPostFija.trim().replace(" ", "");
    }

    public LinkedList convertirCadenaALista(String cadena) {
        char m[] = cadena.toCharArray();
        LinkedList n = new LinkedList();
        for (int i = 0; i < m.length; i++) {
            n.add(String.valueOf(m[i]));
        }
        return n;
    }
    
    /*
     public void obtenerOperacionesInternas(String expresionPostFija) {

     System.out.println(expresionPostFija);

     String simbols = "+|*.()";

     String expresionPostFija_ = expresionPostFija.trim().replace(" ", "");

     LinkedList lista = convertirCadenaALista(expresionPostFija_);

     Stack< String> aux = new Stack<String>();

     for (int i = 0; i < lista.size(); i++) {

     String temporaryStr = (String) lista.get(i);

     if (!simbols.contains(temporaryStr)) {
     aux.add(temporaryStr);
     } else {

     int valor = obtenerOperandosNecesarios(temporaryStr), cnt = 0;
     if (valor == 1) {

     } else if (valor == 2) {

     }

     }

     }

     }

     public int obtenerOperandosNecesarios(String operador) {
     int valor = 0;
     if (operador.equals("+") || operador.equals("*")) {
     valor = 1;
     }

     if (operador.equals("|") || operador.equals(".")) {
     valor = 2;
     }
     return valor;
     }
     */
}
