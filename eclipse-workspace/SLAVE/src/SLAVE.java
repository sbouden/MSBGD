import java.util.List;
import java.io.*;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class SLAVE {

	//public static void main(String[] args) throws InterruptedException {
		//Thread.sleep(10000); 
		//int somme= 3+5;
		//System.out.println("Somme de 3 + 5 = " + somme);
        //System.err.println("Somme de 3 + 5 = " + somme);
		

			  public static void main (String[] argv) throws IOException
			    { 

				  int indice=Integer.parseInt(argv[0]);
				  
				  //for(int indice = 0; indice <= 2; indice++) {
				  List<String> lines = Files.readAllLines(Paths.get("/home/sonia/eclipse-workspace/SPLITS/S"+ indice + ".txt"));
				   
				   Map<String,Integer> dictionary = new HashMap<>();
				   String chaine="";
				   
		
				   for(String line: lines) {
				   String[] mots = line.split(" ");
				   for (String mot: mots) {
					   
					   if(!dictionary.containsKey(mot)) {
						   dictionary.put(mot, 1);
						   chaine=chaine+ ' '+mot+ ' '+"1";
						   //System.out.println("chaine : "+ chaine);

					   }

					   else {
						   dictionary.put(mot, dictionary.get(mot)+1);
						   chaine=chaine+ ' '+mot+ ' '+"1";
					   }
				   }
				   }
				   //System.out.println("Dictionnaire"+ indice +": \n" + dictionary);
				   String outputFile = "/home/sonia/eclipse-workspace/MAPS/UM"+indice+".txt";
				   File file = new File(outputFile);
				   FileWriter writer = new FileWriter(file); 
				   writer.write(chaine);
				   writer.close();
				   
				  //}
		

	}

}
