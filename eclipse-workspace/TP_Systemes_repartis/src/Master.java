import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;

public class Master {

    public static void main(String[] args) {

        ProcessBuilder processBuilder = new ProcessBuilder("java", "-jar", "/home/sonia/eclipse-workspace/SLAVE/SLAVE.jar");

      
        try {
        	processBuilder.inheritIO();
            Process process = processBuilder.start();
            
        	//Process process = processBuilder.inheritIO().start();
            
             
            BufferedReader reader =
                    new BufferedReader(new InputStreamReader(process.getErrorStream()));

            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            
           // int exitCode = process.waitFor();
            boolean b = process.waitFor(2, TimeUnit.SECONDS); 
           // Thread.sleep(15000);
            System.out.println("\nExited with error code : " + b);
            //System.out.printf("Program ended with exitCode %d", exitCode);
            

        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

}