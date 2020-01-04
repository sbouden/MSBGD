import java.awt.List;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

public static boolean sequentialProcessLauncher(String command) {
​
		ProcessBuilder builder = new ProcessBuilder(command.split(" "));
		builder.redirectErrorStream(true);
		Process process = null;
		try {
			process = builder.start();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
​
		BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
​
		boolean running = true;
		boolean tooLong = false;
		while (running) {
			try {
				// Wait For retourne vrai si le programme est arrete
				boolean stillRunning = !process.waitFor(5, TimeUnit.SECONDS);
​
				// On lit la sortie standard. Si on a eu quelque chose, on continue
​
				if (reader.ready()) {
					// On a du monde dans le buffer. On les recupere.
					// Si on ne veut pas les récuperer, on peut faire un "reset"
					// reader.reset();
					while (reader.ready()) {
						int c = reader.read();
						System.out.print((char) c);
					}
​
				} else if(stillRunning) {
					// Le process n'a rien écris pendant les 5 secondes. On le tue
					tooLong = true;
					process.destroy();
				}
				running = stillRunning && !tooLong;
			} catch (IOException | InterruptedException e) {
				e.printStackTrace();
			}
		}
​
		return !tooLong;
​
	}
​
	static class MonRunnable implements Runnable {
		
		int position;
		boolean values[];
		String command;
		
		public MonRunnable(String command, boolean values[], int pos) {
			position = pos;
			this.values = values;
			this.command = command;
		}
		
		@Override
		public void run() {
			boolean b = sequentialProcessLauncher(command);
			values[position] = b;
			System.out.println("Valeur du retour: " + b);
		}
​
	}
​
	public static void main(String[] args) throws IOException, InterruptedException {
​
		// Deploy the
​
		String pc[] = new String[] { "c130-10", "c130-11" };
​
		// Une facon de lancer les threads, sans attendre de retour de leur part:
		Arrays.asList(pc).parallelStream().forEach(l-> sequentialProcessLauncher("ssh login@"+l +" ls"));
		
		// Une autre, et on fait une liste avec les valeurs de retour.
		List<Boolean> returnValue = Arrays.asList(pc).parallelStream().map(l->sequentialProcessLauncher).collect(Collectors.toCollection(ArrayList::new));
		
		System.out.println(returnValue);
		
		
		Thread threads[] = new Thread[pc.length];
		boolean[] returnVal = new boolean[pc.length];
		
		for (int i = 0; i < pc.length; i++) {
			Thread tread = new Thread(new MonRunnable(pc[i],returnVal, i)); 
			
			tread.start();
			threads[i] = tread;
		}
​
		/// Do some code
​
		for(Thread th : threads)
			th.join();
		
		
		for(boolean b: returnVal)
			System.out.print(b + " ");
}

