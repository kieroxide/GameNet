def convert_game_data_to_graph(data):
    nodes = {} 
    edges = [] 

    for game, attrs in data.items():
        # Add the game node
        nodes[game] = {"type": "Game"}
        if "releaseDate" in attrs:
            nodes[game]["releaseDate"] = attrs["releaseDate"]

        # Handle relationships
        for col in ["developers", "platforms", "genres"]:
            if col in attrs:
                for value in attrs[col]:
                    # Add the related node if not already there
                    if value not in nodes:
                        nodes[value] = {"type": col[:-1].capitalize()}  # [:-1] strips the s

                    # Add the edge
                    edges.append({
                        "source": game,
                        "target": value,
                        "type": col[:-1]  # strips s
                    })

    return {"nodes": nodes, "edges": edges}