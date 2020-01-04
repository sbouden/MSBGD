import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class STEP9 {
	
	public static void main(String[] args) throws IOException {
			 List<String> lines = Files.readAllLines(Paths.get("machine"));
			 String hostname = "sbouden@";
			 
			 ProcessBuilder processBuilder = new ProcessBuilder();
			 
			 for(String line: lines) {
				   String[] machines = line.split("/n");
				  
				   for (String machine: machines) {
					   System.out.println("Machine: " + machine);
				   
			 processBuilder.command("ssh", hostname+machine, "rm -rf /tmp/sbouden/SLAVE/");
			 processBuilder.command("ssh", hostname+machine, "mkdir -p /tmp/sbouden/SLAVE");
			 processBuilder.command("ssh scp -r -p /home/sonia/eclipse-workspace/SLAVE/SLAVE.jar sbouden@", machine,":/tmp/sbouden/SLAVE/");
			 processBuilder.command("java", "-jar", "/tmp/sbouden/SLAVE.jar");
			 
     		 Process process = processBuilder.start();
			 BufferedReader reader =
	                    new BufferedReader(new InputStreamReader(process.getInputStream()));

	            String linecmd;
	          
	            while ((linecmd = reader.readLine()) != null) {
	            	System.out.println(linecmd);
	            	
	            }      	
	}

}
}
}