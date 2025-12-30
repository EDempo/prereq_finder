UMD Course Prereq Finder – Full App Roadmap
Setup & Project Foundation  - DONE
Graph Logic - DONE
Basic UI Integration - DONE
Full Traversal & Coreqs - DONE

Goals: Extend the app to show all course relationships.

Tasks:

Add coreqs using DFS/BFS.

Add reverse_prereqs and reverse_coreqs traversals.

Refactor displayResults() to handle multiple arrays:

displayResults({
  prereqs: [...],
  coreqs: [...],
  reversePrereqs: [...],
  reverseCoreqs: [...]
})

Format the display using HTML lists (<ul> / <li>) and labels.

Optionally make course IDs clickable so users can search them directly.

Outcome: The app now shows a complete set of relationships for any course in a readable format.

Day 5 – UI Polish & Usability

Goals: Make the app more user-friendly and visually clear.

Tasks:

Add CSS for readability (spacing, colors, fonts).

Highlight sections: Prereqs, Coreqs, Reverse Prereqs, Reverse Coreqs.

Sort arrays alphabetically or in traversal order for clarity.

Handle errors gracefully: show messages if course not found.

Optionally add search history, input clearing, or keyboard shortcuts.

Outcome: The app is visually clean, easy to use, and robust for public use.

Day 6 – Optional Features & Deployment

Goals: Make the app dynamic, always up-to-date, and ready for public access.

Tasks:

Implement caching of the course graph to avoid multiple fetches.

Research if UMD provides an API to keep courses always up-to-date.

If no API exists, document how to manually update courses.json.

Deploy to GitHub Pages, Netlify, or another static host.

Test live version for cross-browser compatibility.

Outcome: A fully functional, publicly accessible UMD Prereq Finder app, dynamic and maintainable.
