/* =====================================================================
   Legal Intelligence Briefing — universal monitor renderer
   Expects two files alongside the page: monitor.json + items.json
   ===================================================================== */
(function () {
  const THEMES = [
    { id: "light",     label: "Light",     hint: "Cream Prosus brand"          },
    { id: "dark",      label: "Dark",      hint: "Deep violet for night reads" },
    { id: "colourful", label: "Colourful", hint: "Saturated Prosus gradients"  },
    { id: "clean",     label: "Clean",     hint: "Minimal, lots of white"      }
  ];
  const STORAGE_KEY = "lib-theme";

  function applyTheme(id) {
    document.documentElement.setAttribute("data-theme", id);
    try { localStorage.setItem(STORAGE_KEY, id); } catch (e) {}
  }
  function initTheme() {
    let saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    applyTheme(saved && THEMES.some(t => t.id === saved) ? saved : "light");
  }
  initTheme();

  const $  = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  const esc = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

  function hexToRgba(hex, a) {
    const h = hex.replace("#", "");
    const n = h.length === 3
      ? h.split("").map(c => parseInt(c + c, 16))
      : [parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16)];
    return "rgba(" + n[0] + "," + n[1] + "," + n[2] + "," + a + ")";
  }

  const state = { monitor: null, items: [], view: "all", q: "" };

  function renderChrome(m) {
    document.title = m.code + " · " + m.name + " · Legal Intelligence Briefing";
    $("#brand-product").innerHTML = "<b>" + esc(m.code) + "</b> — " + esc(m.name);

    const pill = $("#live-pill");
    pill.className = "live-pill " + (m.status || "live");
    $("#live-pill-label").textContent = m.status_label || (m.week_iso || "Live");

    const tabs = $("#tabs");
    tabs.innerHTML = "";
    tabs.appendChild(makeTab("all", "All items", state.items.length));
    (m.topics || []).forEach(t => {
      tabs.appendChild(makeTab(t.id, t.label, countByTopic(t.id), t.color));
    });

    $("#summary-week").textContent = m.week_label || "";
    const pulseStatus = (m.status === "calibrating") ? "calibrating"
                     : (m.status === "pending")     ? "awaiting sign-off"
                     : (m.status === "dormant")     ? "dormant"
                     : "live";
    $("#summary-pulse").innerHTML = "Pulse: <b>" + esc(pulseStatus) + "</b>";

    const chipsRow = $("#summary-chips");
    chipsRow.innerHTML = "";
    (m.chips || []).forEach(c => {
      const el = document.createElement("span");
      el.className = "chip";
      el.innerHTML = c.replace(/<\/?b>/g, (t) => t);
      chipsRow.appendChild(el);
    });
    if (m.footer_note) {
      const note = document.createElement("span");
      note.className = "chip notice";
      note.textContent = m.footer_note;
      chipsRow.appendChild(note);
    }

    const high = state.items.filter(i => i.risk === "high").length;
    const med  = state.items.filter(i => i.risk === "med").length;
    $("#ct-total").textContent = state.items.length;
    $("#ct-high").textContent  = high;
    $("#ct-med").textContent   = med;
    $("#search-input").placeholder = "Search across " + state.items.length + " items…";

    $("#footer-meta").textContent =
      (m.privilege_note || "Privileged · Prosus internal + named external counsel") +
      " · " + (m.week_label || "");
    $("#footer-gen").textContent =
      "Generated " + (m.generated_at || "—") + " · v" + (m.version || "0.1");
  }

  function makeTab(id, label, count, color) {
    const btn = document.createElement("button");
    btn.className = "tab" + (state.view === id ? " active" : "");
    btn.dataset.view = id;
    if (color) btn.style.setProperty("--topic-color", color);
    btn.innerHTML = esc(label) + ' <span class="tab-ct">' + count + "</span>";
    btn.addEventListener("click", () => {
      state.view = id;
      $$(".tab").forEach(t => t.classList.toggle("active", t === btn));
      renderItems();
    });
    return btn;
  }

  function countByTopic(topicId) {
    return state.items.filter(i => i.theme === topicId).length;
  }

  function topicLookup() {
    const map = {};
    (state.monitor.topics || []).forEach(t => { map[t.id] = t; });
    return map;
  }

  function matches(it) {
    if (state.view !== "all" && it.theme !== state.view) return false;
    if (state.q) {
      const hay = [it.title, it.body, it.why, it.co, it.countryLabel, it.catLabel]
        .filter(Boolean).join(" ").toLowerCase();
      if (hay.indexOf(state.q.toLowerCase()) === -1) return false;
    }
    return true;
  }

  function renderItems() {
    const topics = topicLookup();
    const grid = $("#item-grid");
    const list = state.items.filter(matches);

    if (!list.length) {
      grid.innerHTML =
        '<div class="empty"><h3>No items match these filters</h3>' +
        "<p>Clear the search or pick another tab.</p></div>";
      return;
    }

    grid.innerHTML = list.map(it => {
      const topic = topics[it.theme] || {};
      const color = topic.color || "#571580";
      const domain = topic.label || it.theme;
      const r = it.risk === "high" ? "r-high" : it.risk === "med" ? "r-med" : "r-low";
      const rl = it.risk === "high" ? "HIGH" : it.risk === "med" ? "MED" : "LOW";
      const ruleChip = it.rule ? '<span class="ctag ctag-rule">' + esc(it.rule) + "</span>" : "";
      const styleVars =
        "--topic-fg:" + color + ";" +
        "--topic-tint:" + hexToRgba(color, 0.10) + ";" +
        "--topic-border:" + hexToRgba(color, 0.28);
      return '<article class="card">' +
        '<header class="card-head">' +
          '<span class="ctag ctag-domain" data-topic-color style="' + styleVars + '">' + esc(domain) + "</span>" +
          (it.catLabel ? '<span class="ctag">' + esc(it.catLabel) + "</span>" : "") +
          (it.countryLabel ? '<span class="ctag ctag-loc">' + esc(it.countryLabel) + "</span>" : "") +
          (it.dateLabel ? '<span class="ctag ctag-date">' + esc(it.dateLabel) + "</span>" : "") +
          ruleChip +
          (it.source ? '<a class="ctag ctag-source" href="' + esc(it.url || "#") +
            '" target="_blank" rel="noopener">' + esc(it.source) + " ↗</a>" : "") +
          '<span class="risk-pill ' + r + '">' + rl + "</span>" +
        "</header>" +
        '<h3 class="card-title">' + esc(it.title) + "</h3>" +
        (it.body ? '<p class="card-body">' + esc(it.body) + "</p>" : "") +
        (it.why ? '<div class="card-why"><b>Why it matters →</b> ' + esc(it.why) + "</div>" : "") +
        '<footer class="card-foot">' +
          (it.co ? '<span class="opc">OpCos: <b>' + esc(it.co) + "</b></span>" : "") +
          (it.owner ? '<span class="owner">' + esc(it.owner) +
            (it.ownerTeam ? " · " + esc(it.ownerTeam) : "") + "</span>" : "") +
        "</footer>" +
      "</article>";
    }).join("");

    $$(".tab").forEach(t => {
      const v = t.dataset.view;
      const ct = v === "all" ? state.items.length : countByTopic(v);
      const span = t.querySelector(".tab-ct");
      if (span) span.textContent = ct;
    });
  }

  function mountThemePicker() {
    const btn = $("#theme-toggle");
    const menu = $("#theme-menu");
    menu.innerHTML = THEMES.map(t => {
      const active = document.documentElement.getAttribute("data-theme") === t.id;
      return '<button data-theme="' + t.id + '" class="' + (active ? "active" : "") + '" title="' + esc(t.hint) + '">' +
        '<span class="swatch ' + t.id + '" aria-hidden="true"></span>' +
        '<span>' + esc(t.label) + "</span>" +
      "</button>";
    }).join("");
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = menu.hasAttribute("open");
      if (open) menu.removeAttribute("open"); else menu.setAttribute("open", "");
    });
    menu.addEventListener("click", (e) => {
      const target = e.target.closest("button[data-theme]");
      if (!target) return;
      applyTheme(target.dataset.theme);
      $$("#theme-menu button").forEach(b => b.classList.toggle("active", b === target));
      menu.removeAttribute("open");
    });
    document.addEventListener("click", (e) => {
      if (!menu.contains(e.target) && e.target !== btn) menu.removeAttribute("open");
    });
  }

  function mountSearch() {
    $("#search-input").addEventListener("input", (e) => {
      state.q = e.target.value.trim();
      renderItems();
    });
  }

  async function boot() {
    mountThemePicker();
    mountSearch();
    // Prefer inline data (works over file:// and CDN both); fall back to fetch
    let m = null, items = null;
    try {
      if (window.MONITOR_DATA && window.ITEMS_DATA) {
        m = window.MONITOR_DATA;
        items = window.ITEMS_DATA;
      } else {
        const r = await Promise.all([
          fetch("./monitor.json", { cache: "no-store" }).then(r => r.json()),
          fetch("./items.json",   { cache: "no-store" }).then(r => r.json())
        ]);
        m = r[0]; items = r[1];
      }
      state.monitor = m;
      state.items = Array.isArray(items) ? items : (items.items || []);
      renderChrome(m);
      renderItems();
    } catch (err) {
      console.error("Monitor failed to load", err);
      const grid = $("#item-grid");
      if (grid) grid.innerHTML =
        '<div class="empty"><h3>Monitor data didn\'t load</h3>' +
        "<p>Check that <code>monitor.json</code> and <code>items.json</code> sit next to this page, or open via the Netlify URL.</p></div>";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
