"use strict";

const statusNode = document.querySelector("#status");
const projectList = document.querySelector("#project-list");

function isPublicHttpsUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && Boolean(url.hostname) && !url.username && !url.password;
  } catch {
    return false;
  }
}

function renderProject(project) {
  const requiredText = ["title", "summary", "data_source", "data_rights", "limitations"];
  if (!project || typeof project !== "object" || requiredText.some((key) => typeof project[key] !== "string" || !project[key].trim())) {
    throw new Error("An entry is missing required project or disclosure text.");
  }
  if (!isPublicHttpsUrl(project.repository_url) || project.reviewed_for_publication !== true) {
    throw new Error("Every entry needs an HTTPS repository link and publication review.");
  }

  const article = document.createElement("article");
  article.className = "project-card";
  const title = document.createElement("h3");
  const link = document.createElement("a");
  link.href = project.repository_url;
  link.textContent = project.title;
  title.append(link);
  article.append(title);

  for (const [label, value] of [
    ["Summary", project.summary],
    ["Data source", project.data_source],
    ["Rights", project.data_rights],
    ["Limitations", project.limitations],
  ]) {
    const paragraph = document.createElement("p");
    paragraph.className = "meta";
    const strong = document.createElement("strong");
    strong.textContent = `${label}: `;
    paragraph.append(strong, document.createTextNode(value));
    article.append(paragraph);
  }
  return article;
}

async function loadPortfolio() {
  try {
    const response = await fetch("projects.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load projects.json (HTTP ${response.status}).`);
    const portfolio = await response.json();
    if (!portfolio || !Array.isArray(portfolio.projects)) throw new Error("projects.json must contain a projects array.");
    if (portfolio.projects.length === 0) {
      statusNode.textContent = "No case studies are published yet. Add a real project after checking its sources and sharing rights.";
      return;
    }
    const cards = portfolio.projects.map(renderProject);
    projectList.replaceChildren(...cards);
    statusNode.textContent = `${cards.length} reviewed case study${cards.length === 1 ? "" : "ies"}.`;
  } catch (error) {
    statusNode.textContent = `Portfolio entries could not be displayed: ${error.message}`;
  }
}

loadPortfolio();
