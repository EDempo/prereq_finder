// src/main.js
import fs from "fs";
import {dfs} from "./graph.js";
import {bfs} from "./graph.js";
const graph = JSON.parse(
    fs.readFileSync("./data/courses.json", "utf8")  
);


const start = "CMSC131";

console.log('DFS (courses unlocked after):');
for(const c of dfs(start, graph, "reverse_prereqs")) {
  console.log(" ", c);
}

console.log("\nBFS (courses unlocked after):");
for(const c of bfs(start, graph, "reverse_prereqs")) {
  console.log(" ", c);
}

console.log("\nRequired Pre-requisites:");
for(const c of dfs(start, graph, "prereqs")) {
  console.log(" ", c);
}

