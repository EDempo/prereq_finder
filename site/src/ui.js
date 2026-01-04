import { dfs } from "./graph.js";

async function loadGraph() {
  const response = await fetch("/data/courses.json");
  const graph = await response.json();
  return graph;
}
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("course-input");
  const button = document.getElementById("search-button");
  const collapse_button = document.getElementById("collapsible-button");
  const ul_prereqs = document.getElementById("prereqs-list");
  const ul_coreqs = document.getElementById("coreqs-list");
  const ul_reverse = document.getElementById("reverse-list");
  const prereq_count = document.getElementById("prereq-count");
  const coreq_count = document.getElementById("coreq-count");
  const reverse_count = document.getElementById("reverse-count");
  let prereqs = [];
  let coreqs = [];
  let reverses = [];

  function render(ul, list) {
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
  }

  function validateID(courseID, courseGraph) {
    const error = document.getElementById("error");
    if (!courseGraph[courseID]) {
      error.textContent = "ERROR: Invalid Course ID.";
      return false;
    }
    error.textContent = "";
    return true;
  }

  function getEdgesBFS(courseID, courseGraph, edgeKey) {
    return dfs(courseID, courseGraph, edgeKey);
  }

  function getEdgesDFS(courseID, courseGraph, edgeKey) {
    return dfs(courseID, courseGraph, edgeKey);
  }

  let state = "hidden";

  collapse_button.textContent = "Show";
  collapse_button.addEventListener("click", () => {
    reverse_count.textContent = "";
    ul_reverse.textContent = "";
    if (state === "hidden") {
      state = "expanded";
      collapse_button.textContent = "Hide";
      reverse_count.textContent = `Showing ${reverses.length} out of ${reverses.length} reverse perequisites.`;
    } else {
      state = "hidden";
      collapse_button.textContent = "Show";
      reverse_count.textContent = `Showing 8 out of ${reverses.length} reverse perequisites.`;
    }

    const visible = state === "expanded" ? reverses : reverses.slice(0, 8);
    render(ul_reverse, visible);
  });

  const reverseSearch = document.getElementById("reverse-search");

  loadGraph().then((courseGraph) => {
    button.addEventListener("click", () => {
      const courseID = input.value.toUpperCase();
      if (validateID(courseID, courseGraph)) {
        state = "hidden";
        collapse_button.textContent = "Show";
        reverseSearch.value = "";
        prereqs = getEdgesDFS(courseID, courseGraph, "prereqs");
        if (prereqs.length == 0) {
          prereqs.push("No prerequisites for this course.");
        }

        coreqs = getEdgesBFS(courseID, courseGraph, "coreqs");
        if (coreqs.length == 0) {
          coreqs.push("No corequisites for this course.");
        }
        reverses = getEdgesDFS(courseID, courseGraph, "reverse_prereqs").sort();
        if (reverses.length == 0) {
          reverses.push("None");
        }

        ul_prereqs.textContent = "";
        ul_coreqs.textContent = "";
        ul_reverse.textContent = "";
        if (prereqs[0] !== "No prerequisites for this course.") {
          render(ul_prereqs, prereqs);
          prereq_count.textContent = `${prereqs.length} prerequisites found.`;
        } else {
          prereq_count.textContent = `No prerequisites found.`;
        }
        if (coreqs[0] !== "No corequisites for this course.") {
          render(ul_coreqs, coreqs);
          coreq_count.textContent = `${coreqs.length} corequisites found.`;
        } else {
          coreq_count.textContent = `No corequisites found.`;
        }
        if (reverses[0] !== "None") {
          const visible =
            state === "expanded" ? reverses : reverses.slice(0, 8);
          if (reverses.length < 8) {
            reverse_count.textContent = `${reverses.length} reverse prerequisites found.`;
          } else {
            reverse_count.textContent =
              state === "hidden"
                ? `Showing 8 out of ${reverses.length} subsequent courses.`
                : `Showing ${reverses.length} out of ${reverses.length} subsequent courses.`;
          }
          render(ul_reverse, visible);
          reverseSearch.addEventListener("input", () => {
            const query = reverseSearch.value.toUpperCase();

            const filtered = reverses.filter((c) =>
              c.toUpperCase().includes(query),
            );

            ul_reverse.textContent = "";
            render(ul_reverse, filtered);
            reverse_count.textContent = `Showing ${filtered.length} of ${reverses.length} subsequent courses`;
          });
        } else {
          reverse_count.textContent = `No subsequent courses found.`;
        }
      }
    });
  });
});
