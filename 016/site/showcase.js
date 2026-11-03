"use strict";

const searchInput = document.querySelector("#search");
const topicSelect = document.querySelector("#topic");
const clearButton = document.querySelector("#clear");
const projectList = document.querySelector("#project-list");
const statusNode = document.querySelector("#status");

function validateProjects(documentData) {
  if (!documentData || !Array.isArray(documentData.projects)) {
    throw new Error("Project manifest must contain a projects list.");
  }
  const seen = new Set();
  for (const project of documentData.projects) {
    if (!project || !/^\d{3}$/.test(project.number) || seen.has(project.number)) {
      throw new Error("Project numbers must be unique, zero-padded values.");
    }
    seen.add(project.number);
    for (const field of ["title", "topic", "description"]) {
      if (typeof project[field] !== "string" || !project[field].trim()) {
        throw new Error(`Project ${project.number} is missing ${field}.`);
      }
    }
    if (typeof project.readme !== "string" || !/^\.\.\/\.\.\/\d{3}\/README\.md$/.test(project.readme)) {
      throw new Error(`Project ${project.number} has an invalid local README path.`);
    }
  }
  return documentData.projects;
}

function makeCard(project) {
  const card = document.createElement("article");
  card.className = "project-card";
  const topline = document.createElement("div");
  topline.className = "project-topline";
  const number = document.createElement("span");
  number.className = "project-number";
  number.textContent = project.number;
  const topic = document.createElement("span");
  topic.className = "topic-tag";
  topic.textContent = project.topic;
  topline.append(number, topic);

  const heading = document.createElement("h2");
  heading.textContent = project.title;
  const description = document.createElement("p");
  description.textContent = project.description;
  const link = document.createElement("a");
  link.className = "project-link";
  link.href = project.readme;
  link.textContent = "Read the project guide";
  card.append(topline, heading, description, link);
  return card;
}

function render(projects) {
  const query = searchInput.value.trim().toLowerCase();
  const selectedTopic = topicSelect.value;
  const filtered = projects.filter((project) => {
    const matchesText = `${project.number} ${project.title} ${project.topic} ${project.description}`.toLowerCase().includes(query);
    return matchesText && (!selectedTopic || project.topic === selectedTopic);
  });
  projectList.replaceChildren();
  if (filtered.length === 0) {
    const message = document.createElement("p");
    message.className = "empty";
    message.textContent = "No projects match those filters. Try a different search or topic.";
    projectList.append(message);
  } else {
    projectList.append(...filtered.map(makeCard));
  }
  statusNode.textContent = `Showing ${filtered.length} of ${projects.length} projects.`;
}

async function loadShowcase() {
  try {
    const response = await fetch("projects.json");
    if (!response.ok) throw new Error(`Could not load projects.json (HTTP ${response.status}).`);
    const projects = validateProjects(await response.json());
    const topics = [...new Set(projects.map((project) => project.topic))].sort();
    for (const name of topics) {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      topicSelect.append(option);
    }
    searchInput.addEventListener("input", () => render(projects));
    topicSelect.addEventListener("change", () => render(projects));
    clearButton.addEventListener("click", () => {
      searchInput.value = "";
      topicSelect.value = "";
      render(projects);
      searchInput.focus();
    });
    render(projects);
  } catch (error) {
    statusNode.textContent = `Showcase could not be loaded: ${error.message}`;
  }
}

loadShowcase();
