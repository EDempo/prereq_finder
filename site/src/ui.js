import { dfs, bfs } from "./graph.js";

async function loadGraph() {
  const response = await fetch("/data/courses.json");
  const graph = await response.json();
  console.log("Fetched.");
  console.log(graph);
  return graph;
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("UI Loaded");
  const input = document.getElementById("input");
  const button = document.getElementById("button");
  const resDiv = document.getElementById("res_div");

  function displayResults({ prereqs, coreqs, reverse_prereqs }) {
    resDiv.textContent = "";
    const ul_prereqs = document.createElement("ul_prereqs");
    const ul_coreqs = document.createElement("ul_coreqs");

    const label_prereqs = document.createElement("strong");
    label_prereqs.textContent = "Prerequisites";

    resDiv.appendChild(label_prereqs);
    resDiv.appendChild(document.createElement("br"));
    for (const c of prereqs) {
      const li = document.createElement("li");
      if (c !== "No prerequisites for this course.") {
        const link = document.createElement("a");
        link.href = "#";
        link.textContent = c;
        link.addEventListener("click", (e) => {
          e.preventDefault();
          input.value = c;
          button.click();
        });
        li.appendChild(link);
      } else {
        li.textContent = c;
      }

      ul_prereqs.appendChild(li);
    }

    resDiv.appendChild(ul_prereqs);
    resDiv.appendChild(document.createElement("br"));

    const label_coreqs = document.createElement("strong");
    label_coreqs.textContent = "Corequisites";
    resDiv.appendChild(label_coreqs);
    resDiv.appendChild(document.createElement("br"));

    for (const c of coreqs) {
      const li = document.createElement("li");
      if (c !== "No prerequisites for this course.") {
        const link = document.createElement("a");
        link.href = "#";
        link.textContent = c;
        link.addEventListener("click", (e) => {
          e.preventDefault();
          input.value = c;
          button.click();
        });
        li.appendChild(link);
      } else {
        li.textContent = c;
      }

      ul_coreqs.appendChild(li);
    }

    resDiv.appendChild(ul_coreqs);
    resDiv.appendChild(document.createElement("br"));
  }

  function validateID(courseID, courseGraph) {
    if (!courseGraph[courseID]) {
      resDiv.innerText = "ERROR: Invalid Course ID.";
      return false;
    }
    return true;
  }

  function getEdgesBFS(courseID, courseGraph, edgeKey) {
    return dfs(courseID, courseGraph, edgeKey);
  }

  function getEdgesDFS(courseID, courseGraph, edgeKey) {
    return dfs(courseID, courseGraph, edgeKey);
  }

  loadGraph().then((courseGraph) => {
    button.addEventListener("click", () => {
      const courseID = input.value;
      if (validateID(courseID, courseGraph)) {
        const prereqs = getEdgesBFS(courseID, courseGraph, "prereqs");
        if (prereqs.length == 0) {
          prereqs.push("No prerequisites for this course.");
        }
        const coreqs = getEdgesDFS(courseID, courseGraph, "coreqs");
        console.log(coreqs);
        if (coreqs.length == 0) {
          coreqs.push("No corequisites for this course.");
        }
        const reverse_prereqs = getEdgesDFS(
          courseID,
          courseGraph,
          "reverse_prereqs",
        );
        console.log(reverse_prereqs);
        if (reverse_prereqs.length == 0) {
          reverse_prereqs.push("None");
        }
        displayResults({ prereqs, coreqs, reverse_prereqs });
      }
    });
  });
});
