// src/main.js
import {dfs} from "./graph.js";

const graph = {
  "CMSC131": {
    prereqs: [],
    coreqs: [],
    reverse_prereqs: ["CMSC132"],
    reverse_coreqs: []
  },
  "CMSC132": {
    prereqs: ["CMSC131"],
    coreqs: [],
    reverse_prereqs: ["CMSC216"],
    reverse_coreqs: []
  },
  "CMSC216": {
    prereqs: ["CMSC132"],
    coreqs: [],
    reverse_prereqs: [],
    reverse_coreqs: []
  }
};

const start = "CMSC131";
const reachable = dfs(start, graph);

console.log('Courses reachable from ${start}:');

for(const c of reachable) {
    console.log(" ", c);
}

