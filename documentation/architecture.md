```mermaid   
 classDiagram
	class User {
	    String username
	    String password
	    list graphs
		}
	class Graph {
	    string name
		}
		
    User "1" -- "*" Graph
```
