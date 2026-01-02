import { dfs, bfs } from "./graph.js";

async function loadGraph() {
  const response = await fetch("/data/courses.json");
  const graph = await response.json();
  return graph;
}
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("course-input");
  const button = document.getElementById("search-button");
  const collapse_button = document.getElementById("collapsible-button");

  function render(ul, list, limit) {
    let count = 0;
    if (limit == -1) {
      for (const c of list) {
        const li = document.createElement("li");
        if (
          c != "None" &&
          c != "No prerequisites for this course." &&
          c != "No corequisites for this course."
        ) {
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
        ul.appendChild(li);
      }
    } else {
      while (count != limit && count != list.length) {
        const li = document.createElement("li");
        //Making sure there's no link attached if there are no courses in the list
        if (
          list[count] == "No prerequisites for this course." ||
          list[count] == "No corequisites for this course." ||
          list[count] == "None"
        ) {
          li.appendChild(list[count]);
          ul.appendChild(li);
        } else {
          const link = document.createElement("a");
          link.href = "#";
          link.textContent = list[count];
          link.addEventListener("click", (e) => {
            //Click logic for if the user clicks a link attached to any of the courses
            e.preventDefault();
            input.value = list[count];
            button.click();
          });
          li.appendChild(link);
          ul.appendChild(li);
        }
        count++;
      }
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

  let limit = 8;
  collapse_button.textContent = "Show";
  collapse_button.addEventListener("click", () => {
    reverse_count.textContent = "";
    ul_reverse.textContent = "";
    if (limit == 8) {
      limit = -1;
      collapse_button.textContent = "Hide";
      reverse_count.textContent = `Showing ${reverse_prereqs.length} out of ${reverse_prereqs.length} reverse perequisites.`;
    } else {
      limit = 8;
      collapse_button.textContent = "Show";
      reverse_count.textContent = `Showing 8 out of ${reverse_prereqs.length} reverse perequisites.`;
    }
    render(ul_reverse, reverse_prereqs, limit, state);
  });
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

        const ul_prereqs = document.getElementById("prereqs-list");
        const ul_coreqs = document.getElementById("coreqs-list");
        const ul_reverse = document.getElementById("reverse-list");
        const prereq_count = document.getElementById("prereq-count");
        const coreq_count = document.getElementById("coreq-count");
        const reverse_count = document.getElementById("reverse-count");
        ul_prereqs.textContent = "";
        ul_coreqs.textContent = "";
        ul_reverse.textContent = "";
        render(ul_prereqs, prereqs, -1);
        render(ul_coreqs, coreqs, -1);
        render(ul_reverse, reverse_prereqs, limit);
        prereq_count.textContent = `${prereqs.length} prerequisites found.`;
        coreq_count.textContent = `${coreqs.length} corequisites found.`;
        if (reverse_prereqs.length < 8) {
          reverse_count.textContent = `${reverse_prereqs.length} reverse prerequisites found.`;
        } else {
          reverse_count.textContent =
            limit == 8
              ? `Showing 8 out of ${reverse_prereqs.length} reverse perequisites.`
              : `Showing ${reverse_prereqs.length} out of ${reverse_prereqs.length} reverse perequisites.`;
        }
      }
    });
  });
});
