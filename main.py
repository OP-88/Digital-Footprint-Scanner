#!/usr/bin/env python3
import sys
from src.models.node import PersonNode
from src.models.graph import IdentityGraph
from src.core.scanner import Scanner
from src.core.reporter import Reporter

def main():
    print("========================================")
    print("   DIGITAL FOOTPRINT MAPPER (v1.0)      ")
    print("   OpSec Analysis Tool                  ")
    print("========================================")

    # 1. Setup the Target (Input)
    try:
        target_username = input("Enter target username (e.g., joe_doe): ").strip()
        if not target_username:
            print("[-] Error: Username cannot be empty.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] User aborted.")
        sys.exit(0)
    
    # 2. Initialize the Graph (The Data Structure)
    graph = IdentityGraph()
    
    # 3. Create the Root Node (The Person)
    me = PersonNode(target_username, source="User Input")
    graph.set_root(me)

    # 4. Initialize the Engine
    scanner = Scanner()
    
    # 5. Run the Scan (The Algorithm)
    scanner.scan_target(target_username, graph, me)

    # 6. Visualize the Results
    print("\n" + "="*40)
    print("FINAL IDENTITY GRAPH STRUCTURE")
    print("="*40)
    
    if len(graph.nodes) > 1:
        # A. Print the Text Tree to Terminal
        graph.bfs_traversal()
        
        # B. Generate the Visual PNG Image
        output_filename = f"scan_{target_username}.png"
        try:
            graph.visualize(filename=output_filename)
        except AttributeError:
            print("[!] Warning: visualize() method not found in IdentityGraph.")
        except Exception as e:
            print(f"[!] Warning: Could not generate image. Error: {e}")
            
        # C. Generate the HTML Report
        print("\n[*] Generating Intelligence Report...")
        try:
            reporter = Reporter(target_username, graph)
            reporter.generate_html()
        except Exception as e:
            print(f"[!] Error generating report: {e}")

        print("\n[+] Scan Complete. Target mapped.")
    else:
        print("[-] No footprint found. Target has excellent OpSec or does not exist.")

if __name__ == "__main__":
    main()
