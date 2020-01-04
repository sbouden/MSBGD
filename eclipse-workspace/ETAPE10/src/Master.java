import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Master 
{	
	public static void main(String[] args) throws IOException, InterruptedException 
	{
			 List<String> lines = Files.readAllLines(Paths.get("machines"));
			 String hostname = "sbouden@";
			 
			 ProcessBuilder processBuilder = new ProcessBuilder();
			 int i = 0;
//			 
//			 for(String line: lines) {
//				   String[] machines = line.split("/n");
//				   String[] file = {"S0.txt","S1.txt","S2.txt"};
//				   
//				  
//				   for (String machine: machines) {
//					   System.out.println("Machine: " + machine);
//					   System.out.println("File: " + file[i]);
//
//					   processBuilder.command("ssh", hostname+machine, "mkdir -p /tmp/sbouden/SPLITS");
//					   Thread.sleep(100);
//					   processBuilder.command("ssh scp -r -p /home/sonia/eclipse-workspace/SPLITS/", file[i], "sbouden@", machine,":/tmp/sbouden/SPLITS/");
//					   processBuilder.command("ssh", hostname+machine, "cat /tmp/sbouden/SPLITS/", file[i]);
//					   i=i+1; 		
//					   								}
//					   							
//					   Process process = processBuilder.start();
//					   BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
//
//					   String linecmd;
//	          
//					   while ((linecmd = reader.readLine()) != null) {
//						   System.out.println(linecmd);
//	            	
//	            											  		  }    
//				   									
//				   								  
//
//			 						} 
			 String indice = "0";
			 for(String line: lines) {
				 String[] machines = line.split("/n");
				 for (String machine: machines) {
					   System.out.println("Machine: " + machine);		
					   processBuilder.command("ssh scp -r -p /home/sonia/eclipse-workspace/SLAVE/SLAVE.jar sbouden@", machine,":/tmp/sbouden/SLAVE/");
					   processBuilder.command("ssh", hostname+machine, "java", "-jar", "SLAVE.jar ", indice, "/tmp/sbouden/SLAVE.jar");
					   indice=indice+1;
			 }
				 
			 
			 
	}
			 System.out.println("Map finished");
}
}

