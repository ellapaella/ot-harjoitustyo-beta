```mermaid   
 classDiagram
	class User {
	    String nimi
	    String password
	    list graphs
		}
	class Graph {
	    int nominator
            int denominator
            int repeats
		}
		
    User "1" -- "*" Graph
```
