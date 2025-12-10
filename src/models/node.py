import json
from datetime import datetime

class OSINTNode:
    """
    Base class for all nodes in the Identity Graph.
    Implements a Directed Graph structure.
    """
    def __init__(self, value, source="Unknown"):
        self.id = value  # Unique identifier (e.g., username, email)
        self.source = source  # Where we found this info
        self.timestamp = datetime.now().isoformat()
        self.edges = set()  # Adjacency List: Stores connected nodes
        self.properties = {} # Extra data (bio, followers, etc.)
        
        # --- VISUALIZATION ATTRIBUTES ---
        # These are required by graph.py to draw the node correctly
        self.label = value 
        self.type = "Node" 

    def connect(self, node, relation):
        """
        Creates a directed edge to another node.
        Example: connect(email_node, "registered_with")
        """
        # We store the edge as a tuple: (TargetNode, "Relationship Label")
        self.edges.add((node, relation))

    def to_dict(self):
        """Serialization for JSON export"""
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "source": self.source,
            "label": self.label,
            "edges": [(n.id, rel) for n, rel in self.edges]
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"


# --- Polymorphism: Specialized Node Types ---

class PersonNode(OSINTNode):
    """Represents the real human target."""
    def __init__(self, name, source="Input"):
        super().__init__(name, source)
        self.risk_score = 0
        
        # Specifics for Visualization
        self.type = "Person"
        self.label = name  # Display name in the red bubble

class AccountNode(OSINTNode):
    """Represents an account on a specific platform."""
    def __init__(self, username, platform, url, source):
        # Create a unique ID so it doesn't clash with the PersonNode
        unique_id = f"{platform}:{username}"
        
        super().__init__(unique_id, source)
        self.platform = platform
        self.url = url
        self.properties["url"] = url
        
        # Specifics for Visualization
        self.type = "Account"
        self.label = f"{platform}:{username}"  # Display name in the blue bubble

class EmailNode(OSINTNode):
    """Represents an email address."""
    def __init__(self, email, source):
        super().__init__(email, source)
        self.leaked = False  # Placeholder for Breach Check logic
        
        # Specifics for Visualization
        self.type = "Email"
        self.label = email  # Display name in the yellow bubble
