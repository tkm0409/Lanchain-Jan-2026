import os
import networkx as nx
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONCEPT: Simple GraphRAG (Knowledge Graph)
# Instead of chunking text blindly, we extract entities
# and build a NetworkX graph to find "Multi-hop" connections.
# ==========================================

print("--- Lesson 2: Local Knowledge Graph (NetworkX) ---")

# 1. The Knowledge Base
text_data = [
    ("Elon Musk", "founded", "SpaceX"),
    ("SpaceX", "created", "Starship"),
    ("Starship", "destined_for", "Mars"),
    ("Mars", "is_a", "Planet")
]

# 2. Build Graph
G = nx.DiGraph()

for subject, relation, object_ in text_data:
    G.add_edge(subject, object_, relation=relation)

# 3. Visualize Logic
print(f"Nodes: {G.nodes()}")
print(f"Edges: {G.edges(data=True)}")

# 4. Multi-Hop Retrieval Function
def graph_search(start_entity: str, max_depth=2):
    print(f"\nSearching Knowledge Graph starting from: '{start_entity}'...")
    
    if start_entity not in G:
        return "Entity not found in Knowledge Graph."
    
    # Traverse using BFS (Breadth-First Search)
    visited = set()
    queue = [(start_entity, 0)]
    facts = []

    while queue:
        node, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        
        if node not in visited:
            visited.add(node)
            # Get neighbors
            neighbors = G[node]
            for neighbor, attr in neighbors.items():
                relation = attr['relation']
                fact = f"{node} -> [{relation}] -> {neighbor}"
                facts.append(fact)
                queue.append((neighbor, depth + 1))
    
    return facts

# 5. Ask Questions
# UserQ: "What is Elon Musk connected to Mars?"
# Vector DB would fail unless one chunk has "Elon" and "Mars".
# Graph DB hops: Elon -> SpaceX -> Starship -> Mars.

results = graph_search("Elon Musk", max_depth=3)
print("\nRetrieved Facts from Graph:")
for r in results:
    print(r)

# 6. Conclusion
print("\n[System] In production, use Neo4j + LangChain's GraphCypherQAChain for this.")
