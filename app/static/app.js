"use strict";

const PAGE_SIZE = 10;
const state = { meta: null, q: "", category: "", docType: "", offset: 0, total: 0, current: null, editing: null, suggestion: null };

const $ = (id) => document.getElementById(id);

/* ---------- helpers ---------- */

// Build DOM nodes without innerHTML: user content is only ever inserted as text.
function h(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (key === "class") node.className = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (value !== null && value !== undefined && value !== false) node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children.flat()) {
    if (child !== null && child !== undefined && child !== false) node.append(child);
  }
  return node;
}

const dateFormat = new Intl.DateTimeFormat("de-AT", { dateStyle: "medium", timeStyle: "short" });
const formatDate = (iso) => dateFormat.format(new Date(iso));

let toastTimer;
function toast(message, isError = false) {
  const el = $("toast");
  el.textContent = message;
  el.className = "toast" + (isError ? " error" : "");
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, isError ? 6000 : 3000);
}

async function errorMessage(response) {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) {
      return data.detail.map((e) => `${(e.loc || []).slice(1).join(".")}: ${e.msg}`).join("; ");
    }
  } catch { /* not JSON */ }
  return `Fehler ${response.status}`;
}

async function api(path, { method = "GET", body, admin = false, raw = false } = {}) {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (admin) headers["X-Admin-Token"] = sessionStorage.getItem("adminToken") || "";
  const response = await fetch(path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  if (!response.ok) throw new Error(await errorMessage(response));
  if (raw) return response;
  return response.status === 204 ? null : response.json();
}

function debounce(fn, ms) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}

/* ---------- dashboard ---------- */

async function loadStats() {
  const stats = await api("/api/stats");
  const dashboard = $("dashboard");
  dashboard.replaceChildren(
    h("div", { class: "stat" }, h("strong", {}, String(stats.total)), h("span", {}, "Einträge")),
    h("div", { class: "stat" }, h("strong", {}, String(stats.auto_classified)), h("span", {}, "automatisch klassifiziert")),
    ...stats.categories.map((c) =>
      h("button", {
        type: "button",
        class: "chip" + (state.category === c.name ? " active" : ""),
        onclick: () => setCategory(state.category === c.name ? "" : c.name),
      }, c.name, h("b", {}, String(c.count)))
    ),
  );
}

function setCategory(category) {
  state.category = category;
  $("filter-category").value = category;
  state.offset = 0;
  loadStats();
  loadResults();
}

/* ---------- search ---------- */

async function loadResults() {
  const params = new URLSearchParams({ limit: PAGE_SIZE, offset: state.offset });
  if (state.q) params.set("q", state.q);
  if (state.category) params.set("category", state.category);
  if (state.docType) params.set("doc_type", state.docType);

  try {
    const data = await api(`/api/documents?${params}`);
    state.total = data.total;
    renderResults(data.items);
  } catch (err) {
    toast(err.message, true);
  }
}

function snippet(text, length = 180) {
  const flat = text.replace(/\s+/g, " ").trim();
  return flat.length > length ? flat.slice(0, length).trimEnd() + "…" : flat;
}

function badges(doc) {
  return h("div", { class: "badges" },
    h("span", { class: "badge" }, doc.category),
    h("span", { class: "badge plain" }, doc.doc_type),
    doc.auto_classified ? h("span", { class: "badge plain", title: "Kategorie wurde automatisch vorgeschlagen" }, "auto") : null,
  );
}

function tags(doc) {
  return doc.keywords.length ? h("div", { class: "tags" }, doc.keywords.map((k) => h("span", { class: "tag" }, k))) : null;
}

function renderResults(items) {
  const box = $("results");
  const from = state.total === 0 ? 0 : state.offset + 1;
  const to = state.offset + items.length;
  $("result-info").textContent = state.total === 0 ? "" : `${from}–${to} von ${state.total} Einträgen`;
  $("btn-prev").disabled = state.offset === 0;
  $("btn-next").disabled = state.offset + PAGE_SIZE >= state.total;

  if (items.length === 0) {
    box.replaceChildren(h("div", { class: "empty" }, "Keine Einträge gefunden."));
    return;
  }
  box.replaceChildren(...items.map((doc) =>
    h("article", {
      class: "item", tabindex: "0", role: "button",
      onclick: () => openDetail(doc),
      onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDetail(doc); } },
    },
      h("h3", {}, doc.title),
      badges(doc),
      h("p", {}, snippet(doc.content)),
      tags(doc),
    )
  ));
}

/* ---------- detail ---------- */

function openDetail(doc) {
  state.current = doc;
  $("detail-body").replaceChildren(
    h("h2", {}, doc.title),
    badges(doc),
    h("p", { class: "detail-text" }, doc.content),
    tags(doc),
    h("p", { class: "detail-meta" },
      `Erstellt: ${formatDate(doc.created_at)} · Zuletzt geändert: ${formatDate(doc.updated_at)}` +
      (doc.source ? ` · Quelle: ${doc.source}` : "")),
  );
  $("detail-dialog").showModal();
}

async function deleteCurrent() {
  const doc = state.current;
  if (!doc || !confirm(`„${doc.title}“ wirklich löschen?`)) return;
  try {
    await api(`/api/documents/${doc.id}`, { method: "DELETE" });
    $("detail-dialog").close();
    toast("Eintrag gelöscht.");
    await refresh();
  } catch (err) {
    toast(err.message, true);
  }
}

/* ---------- editor ---------- */

function fillSelect(select, options, firstLabel) {
  select.replaceChildren(
    ...(firstLabel ? [h("option", { value: "" }, firstLabel)] : []),
    ...options.map((o) => h("option", { value: o }, o)),
  );
}

function openEditor(doc = null) {
  state.editing = doc;
  state.suggestion = null;
  $("editor-title").textContent = doc ? "Eintrag bearbeiten" : "Neuer Eintrag";
  $("f-title").value = doc?.title ?? "";
  $("f-type").value = doc?.doc_type ?? state.meta.doc_types[0];
  $("f-category").value = doc && !doc.auto_classified ? doc.category : "";
  $("f-content").value = doc?.content ?? "";
  $("f-keywords").value = doc ? doc.keywords.join(", ") : "";
  $("f-source").value = doc?.source ?? "";
  $("suggestion").hidden = true;
  $("editor-error").hidden = true;
  $("detail-dialog").close();
  $("editor-dialog").showModal();
}

const parseKeywords = () => $("f-keywords").value.split(",").map((k) => k.trim()).filter(Boolean);

async function computeSuggestion() {
  const title = $("f-title").value.trim();
  const content = $("f-content").value.trim();
  if (!title || !content) { toast("Bitte zuerst Titel und Inhalt eingeben.", true); return; }
  try {
    const result = await api("/api/classify", { method: "POST", body: { title, content } });
    state.suggestion = result;
    const topScores = Object.entries(result.scores).slice(0, 3).map(([c, s]) => `${c} ${s}`).join(" · ");
    const box = $("suggestion");
    box.replaceChildren(
      result.fallback
        ? h("div", {}, "Keine eindeutige Zuordnung – Standardkategorie: ", h("b", {}, result.category))
        : h("div", {}, "Vorgeschlagene Kategorie: ", h("b", {}, result.category), ` (Sicherheit ${Math.round(result.confidence * 100)} %)`),
      topScores ? h("div", { class: "muted" }, `Punkte: ${topScores}`) : null,
      h("div", {}, "Schlagwörter: ", result.keywords.length ? result.keywords.join(", ") : "–"),
      h("button", { type: "button", onclick: applySuggestion }, "Übernehmen"),
    );
    box.hidden = false;
  } catch (err) {
    toast(err.message, true);
  }
}

function applySuggestion() {
  if (!state.suggestion) return;
  $("f-category").value = state.suggestion.category;
  $("f-keywords").value = state.suggestion.keywords.join(", ");
}

async function saveEditor(event) {
  event.preventDefault();
  const category = $("f-category").value;
  const base = {
    title: $("f-title").value,
    content: $("f-content").value,
    doc_type: $("f-type").value,
    keywords: parseKeywords(),
    source: $("f-source").value.trim() || null,
  };
  try {
    if (state.editing) {
      const body = category ? { ...base, category } : { ...base, reclassify: true };
      await api(`/api/documents/${state.editing.id}`, { method: "PATCH", body });
    } else {
      await api("/api/documents", { method: "POST", body: category ? { ...base, category } : base });
    }
    $("editor-dialog").close();
    toast("Gespeichert.");
    await refresh();
  } catch (err) {
    const box = $("editor-error");
    box.textContent = err.message;
    box.hidden = false;
  }
}

/* ---------- admin / archive ---------- */

const ACTION_LABELS = {
  create: "Erstellt", update: "Geändert", delete: "Gelöscht",
  archive_create: "Archiv erstellt", archive_restore: "Archiv wiederhergestellt",
};

function table(headers, rows) {
  return h("table", {},
    h("thead", {}, h("tr", {}, headers.map((t) => h("th", {}, t)))),
    h("tbody", {}, rows),
  );
}

async function loadAdmin() {
  const [archives, audit] = await Promise.all([
    api("/api/archives", { admin: true }),
    api("/api/audit?limit=50", { admin: true }),
  ]);
  $("admin-area").hidden = false;

  $("archive-list").replaceChildren(
    archives.length === 0
      ? h("p", { class: "muted" }, "Noch keine Archive vorhanden.")
      : table(["Datei", "Erstellt", "Einträge", "Größe", ""], archives.map((a) =>
          h("tr", {},
            h("td", {}, a.name),
            h("td", {}, formatDate(a.created_at)),
            h("td", {}, String(a.document_count)),
            h("td", {}, `${(a.size_bytes / 1024).toFixed(1)} KB`),
            h("td", { class: "actions" },
              h("button", { type: "button", onclick: () => downloadArchive(a.name) }, "Download"), " ",
              h("button", { type: "button", class: "danger", onclick: () => restoreArchive(a) }, "Wiederherstellen"),
            ),
          ))),
  );

  $("audit-list").replaceChildren(
    audit.length === 0
      ? h("p", { class: "muted" }, "Noch keine Einträge.")
      : table(["Zeit", "Aktion", "Details"], audit.map((e) =>
          h("tr", {}, h("td", {}, formatDate(e.timestamp)), h("td", {}, ACTION_LABELS[e.action] ?? e.action), h("td", {}, e.detail)))),
  );
}

async function loginAdmin() {
  const token = $("admin-token").value.trim();
  if (!token) return;
  sessionStorage.setItem("adminToken", token);
  try {
    await loadAdmin();
    toast("Angemeldet.");
  } catch (err) {
    sessionStorage.removeItem("adminToken");
    $("admin-area").hidden = true;
    toast(err.message, true);
  }
}

async function createArchive() {
  try {
    const info = await api("/api/archives", { method: "POST", admin: true });
    toast(`Archiv ${info.name} erstellt (${info.document_count} Einträge).`);
    await loadAdmin();
  } catch (err) {
    toast(err.message, true);
  }
}

async function downloadArchive(name) {
  try {
    const response = await api(`/api/archives/${encodeURIComponent(name)}`, { admin: true, raw: true });
    const url = URL.createObjectURL(await response.blob());
    const link = h("a", { href: url, download: name });
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch (err) {
    toast(err.message, true);
  }
}

async function restoreArchive(archive) {
  const ok = confirm(
    `Alle aktuellen Einträge werden durch die ${archive.document_count} Einträge aus ${archive.name} ersetzt.\n` +
    "Vorher wird automatisch ein Backup des aktuellen Stands angelegt. Fortfahren?");
  if (!ok) return;
  try {
    const result = await api(`/api/archives/${encodeURIComponent(archive.name)}/restore`, { method: "POST", admin: true });
    toast(`${result.restored} Einträge wiederhergestellt. Backup: ${result.backup.name}`);
    await Promise.all([loadAdmin(), refresh()]);
  } catch (err) {
    toast(err.message, true);
  }
}

/* ---------- wiring ---------- */

async function refresh() {
  await Promise.all([loadStats(), loadResults()]);
}

function showTab(name) {
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === name));
  $("tab-kb").hidden = name !== "kb";
  $("tab-admin").hidden = name !== "admin";
  if (name === "admin" && sessionStorage.getItem("adminToken") && $("admin-area").hidden) {
    loadAdmin().catch(() => sessionStorage.removeItem("adminToken"));
  }
}

async function init() {
  try {
    state.meta = await api("/api/meta");
  } catch (err) {
    toast("Server nicht erreichbar: " + err.message, true);
    return;
  }
  fillSelect($("filter-category"), state.meta.categories, "Alle Kategorien");
  fillSelect($("filter-type"), state.meta.doc_types, "Alle Typen");
  fillSelect($("f-category"), state.meta.categories, "Automatisch (Vorschlag)");
  fillSelect($("f-type"), state.meta.doc_types);

  const search = debounce(() => { state.offset = 0; loadResults(); }, 250);
  $("q").addEventListener("input", (e) => { state.q = e.target.value.trim(); search(); });
  $("search-form").addEventListener("submit", (e) => e.preventDefault());
  $("filter-category").addEventListener("change", (e) => setCategory(e.target.value));
  $("filter-type").addEventListener("change", (e) => { state.docType = e.target.value; state.offset = 0; loadResults(); });
  $("btn-prev").addEventListener("click", () => { state.offset = Math.max(0, state.offset - PAGE_SIZE); loadResults(); });
  $("btn-next").addEventListener("click", () => { state.offset += PAGE_SIZE; loadResults(); });
  $("btn-new").addEventListener("click", () => openEditor());

  $("detail-close").addEventListener("click", () => $("detail-dialog").close());
  $("detail-edit").addEventListener("click", () => openEditor(state.current));
  $("detail-delete").addEventListener("click", deleteCurrent);

  $("editor-form").addEventListener("submit", saveEditor);
  $("editor-cancel").addEventListener("click", () => $("editor-dialog").close());
  $("btn-suggest").addEventListener("click", computeSuggestion);

  document.querySelectorAll(".tab").forEach((t) => t.addEventListener("click", () => showTab(t.dataset.tab)));
  $("btn-token").addEventListener("click", loginAdmin);
  $("admin-token").addEventListener("keydown", (e) => { if (e.key === "Enter") loginAdmin(); });
  $("btn-archive").addEventListener("click", createArchive);

  await refresh();
}

init();
