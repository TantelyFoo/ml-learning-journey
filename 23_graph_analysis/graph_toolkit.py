"""
Graph Analysis & Network Science Toolkit
========================================

Core utilities and examples for Week 23: Graph Analysis & Network Science
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

class BasicGraphAnalyzer:
    """Basic graph analysis utilities"""
    
    def __init__(self, graph=None):
        self.graph = graph or nx.Graph()
    
    def create_sample_network(self, n_nodes=20, edge_prob=0.3):
        """Create a sample social network"""
        self.graph = nx.erdos_renyi_graph(n_nodes, edge_prob)
        return self.graph
    
    def basic_metrics(self):
        """Calculate basic graph metrics"""
        if self.graph.number_of_nodes() == 0:
            return {"error": "Empty graph"}
        
        metrics = {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "avg_clustering": nx.average_clustering(self.graph),
            "is_connected": nx.is_connected(self.graph)
        }
        
        if nx.is_connected(self.graph):
            metrics["avg_shortest_path"] = nx.average_shortest_path_length(self.graph)
            metrics["diameter"] = nx.diameter(self.graph)
        
        return metrics
    
    def centrality_analysis(self):
        """Calculate centrality measures"""
        if self.graph.number_of_nodes() == 0:
            return {"error": "Empty graph"}
        
        centralities = {
            "degree": dict(nx.degree_centrality(self.graph)),
            "betweenness": nx.betweenness_centrality(self.graph),
            "closeness": nx.closeness_centrality(self.graph),
            "pagerank": nx.pagerank(self.graph)
        }
        
        return centralities
    
    def visualize(self, layout="spring", node_size=300, with_labels=True):
        """Visualize the graph"""
        plt.figure(figsize=(12, 8))
        
        if layout == "spring":
            pos = nx.spring_layout(self.graph)
        elif layout == "circular":
            pos = nx.circular_layout(self.graph)
        elif layout == "random":
            pos = nx.random_layout(self.graph)
        else:
            pos = nx.spring_layout(self.graph)
        
        nx.draw(self.graph, pos, node_size=node_size, 
                with_labels=with_labels, node_color='lightblue',
                font_size=10, font_weight='bold')
        
        plt.title("Graph Visualization")
        plt.axis('off')
        plt.show()


class GraphNeuralNetwork(torch.nn.Module):
    """Simple Graph Convolutional Network"""
    
    def __init__(self, num_features, hidden_dim=16, num_classes=2):
        super(GraphNeuralNetwork, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, num_classes)
        self.dropout = torch.nn.Dropout(0.5)
    
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        # First GCN layer
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        # Second GCN layer
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)


class InfluenceAnalyzer:
    """Social network influence analysis"""
    
    def __init__(self, graph):
        self.graph = graph
        self.influence_scores = {}
    
    def calculate_influence_metrics(self):
        """Calculate various influence metrics"""
        self.influence_scores = {
            'pagerank': nx.pagerank(self.graph),
            'betweenness': nx.betweenness_centrality(self.graph),
            'closeness': nx.closeness_centrality(self.graph),
            'degree': dict(nx.degree_centrality(self.graph))
        }
        return self.influence_scores
    
    def detect_communities(self):
        """Detect communities using Louvain algorithm"""
        try:
            from community import community_louvain
            communities = community_louvain.best_partition(self.graph)
            return communities
        except ImportError:
            print("Please install python-louvain: pip install python-louvain")
            return {}
    
    def top_influencers(self, metric='pagerank', top_k=10):
        """Get top influencers by specified metric"""
        if not self.influence_scores:
            self.calculate_influence_metrics()
        
        if metric not in self.influence_scores:
            return []
        
        sorted_scores = sorted(self.influence_scores[metric].items(), 
                             key=lambda x: x[1], reverse=True)
        return sorted_scores[:top_k]
    
    def influence_report(self):
        """Generate comprehensive influence analysis report"""
        if not self.influence_scores:
            self.calculate_influence_metrics()
        
        report = {
            "graph_summary": {
                "nodes": self.graph.number_of_nodes(),
                "edges": self.graph.number_of_edges(),
                "density": nx.density(self.graph)
            },
            "top_influencers": {
                "pagerank": self.top_influencers("pagerank", 5),
                "betweenness": self.top_influencers("betweenness", 5),
                "degree": self.top_influencers("degree", 5)
            }
        }
        
        communities = self.detect_communities()
        if communities:
            report["communities"] = {
                "count": len(set(communities.values())),
                "largest_community_size": max([
                    len([n for n, c in communities.items() if c == comm_id])
                    for comm_id in set(communities.values())
                ])
            }
        
        return report


class GraphRecommender:
    """Graph-based recommendation system"""
    
    def __init__(self, user_item_graph):
        self.graph = user_item_graph
        self.user_nodes = set()
        self.item_nodes = set()
        self._identify_node_types()
    
    def _identify_node_types(self):
        """Identify user and item nodes (assuming bipartite graph)"""
        # This is a simplified approach - in practice, you'd have node attributes
        # indicating whether a node is a user or item
        for node in self.graph.nodes():
            if str(node).startswith('user_'):
                self.user_nodes.add(node)
            elif str(node).startswith('item_'):
                self.item_nodes.add(node)
    
    def collaborative_filtering_scores(self, target_user):
        """Calculate collaborative filtering scores"""
        if target_user not in self.user_nodes:
            return {}
        
        # Get items the target user has interacted with
        user_items = set(self.graph.neighbors(target_user))
        
        # Find similar users
        similar_users = {}
        for user in self.user_nodes:
            if user != target_user:
                user_items_other = set(self.graph.neighbors(user))
                # Calculate Jaccard similarity
                intersection = len(user_items.intersection(user_items_other))
                union = len(user_items.union(user_items_other))
                if union > 0:
                    similar_users[user] = intersection / union
        
        # Get recommendations based on similar users
        recommendations = {}
        for similar_user, similarity in similar_users.items():
            similar_user_items = set(self.graph.neighbors(similar_user))
            new_items = similar_user_items - user_items
            for item in new_items:
                if item in recommendations:
                    recommendations[item] += similarity
                else:
                    recommendations[item] = similarity
        
        return recommendations
    
    def recommend_items(self, user_id, top_k=10):
        """Generate top-k recommendations for a user"""
        scores = self.collaborative_filtering_scores(user_id)
        sorted_recommendations = sorted(scores.items(), 
                                      key=lambda x: x[1], reverse=True)
        return sorted_recommendations[:top_k]


def create_sample_social_network():
    """Create a sample social network for testing"""
    G = nx.Graph()
    
    # Add users
    users = [f"user_{i}" for i in range(20)]
    G.add_nodes_from(users)
    
    # Add random connections (friendships)
    import random
    random.seed(42)
    for i, user1 in enumerate(users):
        for user2 in users[i+1:]:
            if random.random() < 0.3:  # 30% chance of connection
                G.add_edge(user1, user2)
    
    return G


def create_sample_recommendation_graph():
    """Create a sample user-item bipartite graph for recommendations"""
    G = nx.Graph()
    
    # Add users and items
    users = [f"user_{i}" for i in range(10)]
    items = [f"item_{i}" for i in range(15)]
    
    G.add_nodes_from(users)
    G.add_nodes_from(items)
    
    # Add user-item interactions
    import random
    random.seed(42)
    for user in users:
        # Each user interacts with 3-7 items
        num_interactions = random.randint(3, 7)
        user_items = random.sample(items, num_interactions)
        for item in user_items:
            G.add_edge(user, item)
    
    return G


# Example usage and testing functions
def run_basic_analysis_example():
    """Example: Basic graph analysis"""
    print("=== Basic Graph Analysis Example ===")
    
    analyzer = BasicGraphAnalyzer()
    graph = analyzer.create_sample_network(n_nodes=15, edge_prob=0.4)
    
    # Basic metrics
    metrics = analyzer.basic_metrics()
    print("Graph Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Centrality analysis
    centralities = analyzer.centrality_analysis()
    print("\nTop 5 nodes by PageRank:")
    pagerank_sorted = sorted(centralities["pagerank"].items(), 
                           key=lambda x: x[1], reverse=True)
    for node, score in pagerank_sorted[:5]:
        print(f"  Node {node}: {score:.3f}")


def run_influence_analysis_example():
    """Example: Social network influence analysis"""
    print("\n=== Influence Analysis Example ===")
    
    # Create social network
    social_graph = create_sample_social_network()
    analyzer = InfluenceAnalyzer(social_graph)
    
    # Generate report
    report = analyzer.influence_report()
    print("Influence Analysis Report:")
    print(f"  Nodes: {report['graph_summary']['nodes']}")
    print(f"  Edges: {report['graph_summary']['edges']}")
    print(f"  Density: {report['graph_summary']['density']:.3f}")
    
    print("\nTop 3 Influencers (PageRank):")
    for node, score in report['top_influencers']['pagerank'][:3]:
        print(f"  {node}: {score:.3f}")


def run_recommendation_example():
    """Example: Graph-based recommendations"""
    print("\n=== Recommendation System Example ===")
    
    # Create recommendation graph
    rec_graph = create_sample_recommendation_graph()
    recommender = GraphRecommender(rec_graph)
    
    # Get recommendations for a user
    target_user = "user_0"
    recommendations = recommender.recommend_items(target_user, top_k=5)
    
    print(f"Recommendations for {target_user}:")
    for item, score in recommendations:
        print(f"  {item}: {score:.3f}")


if __name__ == "__main__":
    # Run all examples
    run_basic_analysis_example()
    run_influence_analysis_example()
    run_recommendation_example()
    
    print("\n=== Graph Analysis Toolkit Ready! ===")
    print("Use the classes above to build your own graph analysis projects.")
