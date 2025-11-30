def detect_cycles(tasks):
    """Simple DFS-based cycle detection using task titles as nodes."""
    graph = {t["title"]: t.get("dependencies", []) for t in tasks}
    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            if dep in graph and dfs(dep):
                return True

        stack.remove(node)
        return False

    for node in graph:
        if dfs(node):
            return True
    return False