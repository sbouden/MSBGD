import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class DEPLOY {
	
	public static void main(String[] args) throws IOException, InterruptedException {
		 List<String> lines = Files.readAllLines(Paths.get("machines"));
		 String hostname = "sbouden@";
		 ProcessBuilder processBuilder = new ProcessBuilder();
		 
		 try {
		 
		   for(String line: lines) {
		   String[] machines = line.split("/n");
		  
		   for (String machine: machines) {
			   System.out.println("Machine: " + machine);
			   
		      //--------Vérification si machine allumée-----------------
			   
			   processBuilder.command("ssh", hostname+machine, "ls");
			   processBuilder.command("mkdir -p SLAVE /tmp/sbouden/");
           	   //process.waitFor();
			   processBuilder.command("exit");
           	   processBuilder.command("scp -r -p /home/sonia/eclipse-workspace/SLAVE/SLAVE.jar sbouden@", machine,":/cal/homes/sbouden/SLAVE/");
			   
			   Process process = processBuilder.start();
			   
			   
			   BufferedReader reader =
	                    new BufferedReader(new InputStreamReader(process.getErrorStream()));

	            String linecmd;
	            while ((linecmd = reader.readLine()) != null) {
	            	System.out.println(linecmd);
	            	
	                //System.out.println("La machine " + machine + " : " linecmd + "/n");
	            }
		   }
}
	 } catch (IOException e) {
         e.printStackTrace();
     }
}
}