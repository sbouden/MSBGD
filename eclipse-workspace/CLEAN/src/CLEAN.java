import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class CLEAN {

	public static void main(String[] args) throws IOException, InterruptedException {
		 List<String> lines = Files.readAllLines(Paths.get("machine"));
		 String hostname = "sbouden@";
		 ProcessBuilder processBuilder = new ProcessBuilder();
		 
		 try {
		 
		   for(String line: lines) {
		   String[] machines = line.split("/n");
		  
		   for (String machine: machines) {
			   System.out.println("Machine: " + machine);
			   
			   Process process = processBuilder.start();
			   processBuilder.command("ssh", hostname+machine, "rm -rf SLAVE/");
			   //process.waitFor();Thread.sleep(10000);
           	   processBuilder.command("exit");

			   BufferedReader reader =
	                    new BufferedReader(new InputStreamReader(process.getErrorStream()));

	            String linecmd;
	            while ((linecmd = reader.readLine()) != null) {
	            	System.out.println(linecmd);
	            }
		   }
}
	 } catch (IOException e) {
        e.printStackTrace();
    }
}

}
