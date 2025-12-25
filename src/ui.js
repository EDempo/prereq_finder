import { dfs, bfs } from "./graph.js"

async function loadGraph() {
const response = await fetch("/data/courses.json");
const graph = await response.json();
return graph;
}
document.addEventListener("DOMContentLoaded", () => {
  console.log("UI Loaded");
  const input = document.getElementById("input");
  const button = document.getElementById("button");
  const resDiv = document.getElementById("res_div");

  function displayResults(results) {
      resDiv.innerText = results.join("->");
} 

    
    function validateID(courseID) {
      if(courseID.length > 9 || courseID.length < 6) {
        resDiv.innerText = "ERROR: Invalid Course ID.";
        return false;
      }
      return true;
      
    }

    function getPrereqs(courseID, courseGraph) {
       return dfs(courseID, courseGraph, "prereqs");
    }

  loadGraph().then(courseGraph => {
  button.addEventListener("click", () => {
    const courseID = input.value;
    if(validateID(courseID)) {
      const results = getPrereqs(courseID, courseGraph);
      displayResults(results);
    } 
  });
  });
});
