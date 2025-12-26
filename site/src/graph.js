// Graph representation example:
// "CMSC131": {
//    prereqs: [],
//    coreqs: [],
//    reverse_prereqs: ["CMSC132"],
//    reverse_coreqs: [],
// }

export function dfs(start, graph, edgeKey) {
  const visited = new Set();
  const final = [];

  function visit(course) {
    if (visited.has(course)) return;
    visited.add(course);
    if (course !== start) {
      final.unshift(course);
    }

    const edges = graph[course]?.[edgeKey] ?? [];
    for (const node of edges) {
      visit(node);
    }
  }

  visit(start);
  return final;
}

export function bfs(start, graph, edgeKey) {
  const visited = new Set([start]);
  const final = [];
  const queue = [start];

  while (queue.length > 0) {
    const node = queue.shift();
    const edges = graph[node]?.[edgeKey] ?? [];
    for (const next of edges) {
      if (!visited.has(next)) {
        visited.add(next);
        if (next !== start) {
          final.unshift(next);
        }
        queue.push(next);
      }
    }
  }

  return final;
}
