```mermaid   
 classDiagram
	class User {
	    String username
	    String password
	    list plots
		}
	class Plot {
	    string name
	    tuple color
		}
		
    User "1" -- "*" Plot
```
