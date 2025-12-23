//Prereq Graph & Simple traversal Algorithm

/* Graph representation:
 * "CMSC131": {
 *    prereqs: [],
 *    coreqs: [],
 *    reverse_prereqs: ["CMSC132"],
 *    reverse_coreqs: [],
 */

export function dfs(start, graph) {
    const visited  = new Set();

    function visit(course) {
    if(visited.has(course)) return;
    visited.add(course);

    const node = graph[course];
    if(!node) return;
    
    for (const next of node.reverse_prereqs) {
      visit(next);
    }
    }
  visit(start);
  return visited;
}
