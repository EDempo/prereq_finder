//Prereq Graph & Simple traversal Algorithm

/* Graph representation:
 * "CMSC131": {
 *    prereqs: [],
 *    coreqs: [],
 *    reverse_prereqs: ["CMSC132"],
 *    reverse_coreqs: [],
 */

export function dfs(start, graph, edgeKey) {
    const visited  = new Set();

    function visit(course) {
    if(visited.has(course)) return;
    visited.add(course);

    const edges = graph[course]?.[edgeKey] ?? [];
    for(const node of edges) {
        visit(node);
    }
  }

  visit(start);
  return visited;

}

export function bfs(start, graph, edgeKey) {
    const visited = new Set([start]);
    const queue = [start];
    
    while(queue.length > 0) {
      const node = queue.shift();
      const edges = graph[node]?.[edgeKey] ?? [];
      for(const node of edges) {
        if(!visited.has(node)) {
            visited.add(node);
            queue.push(node);
        }
      }
    }
    return visited;
}
