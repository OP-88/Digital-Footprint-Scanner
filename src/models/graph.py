import networkx as nx
import matplotlib.pyplot as plt

class IdentityGraph:
    def __init__(self):
        self.nodes = {} # Dictionary of nodes
        self.root = None
        self.edges = [] # List of tuples (node_a, node_b, relationship)

    def set_root(self, node):
        self.root = node
        self.add_node(node)

    def add_node(self, node):
        # We use a unique ID (like the URL or username) to prevent duplicates
        node_id = node.id
        if node_id not in self.nodes:
            self.nodes[node_id] = node

    def add_edge(self, node_a, node_b, relationship="connected_to"):
        # Store the relationship for the visualizer
        self.edges.append((node_a, node_b, relationship))
        
        # Ensure both nodes are in our registry
        self.add_node(node_a)
        self.add_node(node_b)

    def bfs_traversal(self):
        # Your existing print logic (keep this)
        if not self.root:
            return
        
        queue = [(self.root, 0)]
        visited = set()
        visited.add(self.root.id)

        print(f"[+] Starting Graph Traversal from: {self.root.label}")
        
        while queue:
            current_node, level = queue.pop(0)
            prefix = "  " * level + "└── "
            print(f"{prefix}[{current_node.type}] {current_node.label}")

            # Find neighbors based on edges
            for u, v, rel in self.edges:
                neighbor = None
                if u.id == current_node.id: neighbor = v
                elif v.id == current_node.id: neighbor = u
                
                if neighbor and neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append((neighbor, level + 1))

    # --- NEW VISUALIZATION ENGINE ---
    def visualize(self, filename="footprint_map.png"):
        """
        Generates a PNG image of the attack surface using NetworkX.
        """
        G = nx.Graph()
        color_map = []
        labels = {}

        # 1. Add Nodes
        for node_id, node in self.nodes.items():
            G.add_node(node_id)
            labels[node_id] = node.label
            
            # Color Coding based on Node Type
            if node.type == "Person":
                color_map.append('#ff4d4d') # Red (Target)
            elif node.type == "Email":
                color_map.append('#ffcc00') # Yellow (High Value)
            else:
                color_map.append('#4d94ff') # Blue (Accounts)

        # 2. Add Edges
        for u, v, rel in self.edges:
            G.add_edge(u.id, v.id)

        # 3. Draw
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42) # Spring layout for "spiderweb" look
        
        nx.draw(G, pos, 
                node_color=color_map, 
                with_labels=True, 
                labels=labels,
                node_size=3000, 
                font_size=10,
                font_weight='bold',
                edge_color='gray')
        
        plt.title(f"Digital Footprint Map: {self.root.label}", fontsize=15)
        plt.savefig(filename)
        print(f"\n[+] Visualization saved to: {filename}")
        plt.close()
