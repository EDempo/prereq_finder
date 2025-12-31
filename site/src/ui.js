import { dfs, bfs } from "./graph.js";

async function loadGraph() {
  const response = await fetch("/data/courses.json");
  const graph = await response.json();
  return graph;
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("course-input");
  const button = document.getElementById("search-button");

  function displayResults({ prereqs, coreqs, reverse_prereqs }) {
    const ul_prereqs = document.getElementById("prereqs-list");
    const ul_coreqs  =  document.getElementById("coreqs-list");
    const ul_reverse =  document.getElementById("reverse-list");
    ul_prereqs.textContent = "";
    ul_coreqs.textContent = "";
    ul_reverse.textContent = "";

    for (const c of prereqs) {
      const li = document.createElement("li");
      if (c != "No prerequisites for this course.") {
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


    for (const c of coreqs) {
      const li = document.createElement("li");
      if (c != "No corequisites for this course.") {
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


    for (const c of reverse_prereqs) {
      const li = document.createElement("li");
      if (c != "None") {
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

      ul_reverse.appendChild(li);
    }


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
