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

  function displayResults({prereqs, coreqs}) {
      resDiv.innerHTML = `
        <strong>Prerequisites:</strong> ${prereqs.join("->")}<br>
        <strong>Corequisites:</strong> ${coreqs.join(" , ")}
      `
} 

    
    function validateID(courseID, courseGraph) {
      if(!courseGraph[courseID]) {
        resDiv.innerText = "ERROR: Invalid Course ID.";
        return false;
      }
      return true;
      
    }

    function getEdges(courseID, courseGraph, edgeKey) {
       return dfs(courseID, courseGraph, edgeKey);
    }

  loadGraph().then(courseGraph => {
  button.addEventListener("click", () => {
    const courseID = input.value;
    if(validateID(courseID, courseGraph)) {
      const prereqs = getEdges(courseID, courseGraph, "prereqs");
      if(prereqs.length == 0) {
        prereqs.push("No prerequisites for this course.")
      }
      const coreqs  = getEdges(courseID, courseGraph, "coreqs");
      if(coreqs.length == 0) {
        coreqs.push("No corequisites for this course.")
      }
      displayResults({prereqs, coreqs});
    } 
  });
  });
});
