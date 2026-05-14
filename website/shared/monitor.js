/* =====================================================================
   Legal Intelligence Briefing — universal monitor renderer
   Expects two files alongside the page: monitor.json + items.json
   (or inline window.MONITOR_DATA / window.ITEMS_DATA for file:// use).

   v0.3 — adds the per-article feedback widget + export-to-markdown loop.
   See system/skills/feedback-integration.md for how the system consumes
   the batches this widget produces.
   ===================================================================== */
(function () {
  const THEMES = [
    { id: "light",     label: "Light",     hint: "Cream Prosus brand"          },
    { id: "dark",      label: "Dark",      hint: "Deep violet for night reads" },
    { id: "colourful", label: "Colourful", hint: "Saturated Prosus gradients"  },
    { id: "clean",     label: "Clean",     hint: "Minimal, lots of white"      }
  ];
  const STORAGE_KEY = "lib-theme";
  const FEEDBACK_KEY = "lib-feedback-v1";
  const FEEDBACK_WIDGET_VERSION = "0.3";

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

  /* =====================================================================
     FEEDBACK — localStorage-backed thumbs widget + export-to-markdown.
     One vote per (monitor_id, article_id). Re-voting overwrites the
     previous vote and resets its exported_at flag so the new opinion
     reaches the next batch.
     ===================================================================== */
  function loadFeedback() {
    try {
      const raw = localStorage.getItem(FEEDBACK_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) { return []; }
  }
  function saveFeedback(arr) {
    try { localStorage.setItem(FEEDBACK_KEY, JSON.stringify(arr)); } catch (e) {}
  }
  function findVote(arr, monitorId, articleId) {
    return arr.findIndex(v => v.monitor_id === monitorId && v.article_id === articleId);
  }
  function recordVote(item, vote, reason) {
    const arr = loadFeedback();
    const monitorId = state.monitor && state.monitor.id || "unknown";
    const monitorCode = state.monitor && state.monitor.code || "—";
    const idx = findVote(arr, monitorId, item.id);
    const entry = {
      monitor_id: monitorId,
      monitor_code: monitorCode,
      article_id: item.id,
      title: item.title || "",
      theme: item.theme || "",
      catLabel: item.catLabel || "",
      country: item.country || "",
      url: item.url || "",
      vote: vote,
      reason: (reason || "").trim(),
      voted_at: new Date().toISOString(),
      exported_at: null,
      widget_version: FEEDBACK_WIDGET_VERSION
    };
    if (idx >= 0) arr[idx] = entry; else arr.push(entry);
    saveFeedback(arr);
    updateFeedbackBadge();
    return entry;
  }
  function unexportedCount() {
    return loadFeedback().filter(v => !v.exported_at).length;
  }
  function totalVoteCount() {
    return loadFeedback().length;
  }

  function paintCardFeedback(cardEl, item) {
    if (!cardEl) return;
    const arr = loadFeedback();
    const monitorId = state.monitor && state.monitor.id || "unknown";
    const existing = arr[findVote(arr, monitorId, item.id)] || null;
    const up = cardEl.querySelector(".fb-up");
    const down = cardEl.querySelector(".fb-down");
    const status = cardEl.querySelector(".fb-status");
    const reasonRow = cardEl.querySelector(".fb-reason");
    if (up && down) {
      up.classList.toggle("voted", !!existing && existing.vote === "up");
      down.classList.toggle("voted", !!existing && existing.vote === "down");
    }
    if (status) {
      if (existing) {
        const icon = existing.vote === "up" ? "👍" : "👎";
        const exported = existing.exported_at ? " · exported" : "";
        const reason = existing.reason ? ' · "' + existing.reason + '"' : "";
        status.hidden = false;
        status.textContent = "Your vote: " + icon + reason + exported;
      } else {
        status.hidden = true;
        status.textContent = "";
      }
    }
    if (reasonRow) reasonRow.hidden = true;
  }

  function feedbackWidgetHTML() {
    return (
      '<div class="fb" role="group" aria-label="Feedback on this article">' +
        '<button type="button" class="fb-btn fb-up"   aria-label="Helpful — keep this kind of item">' +
          '<span class="fb-icon" aria-hidden="true">👍</span> Helpful' +
        '</button>' +
        '<button type="button" class="fb-btn fb-down" aria-label="Not helpful — less of this">' +
          '<span class="fb-icon" aria-hidden="true">👎</span> Not for me' +
        '</button>' +
        '<span class="fb-status" hidden></span>' +
        '<div class="fb-reason" hidden>' +
          '<input type="text" class="fb-reason-input" maxlength="240"' +
            ' placeholder="Optional — why? (e.g. &quot;too narrow&quot;, &quot;wrong jurisdiction&quot;, &quot;exactly what I needed&quot;)">' +
          '<button type="button" class="fb-save">Save</button>' +
          '<button type="button" class="fb-skip">Skip</button>' +
        '</div>' +
      '</div>'
    );
  }

  function wireCardFeedback(cardEl, item) {
    if (!cardEl) return;
    const up = cardEl.querySelector(".fb-up");
    const down = cardEl.querySelector(".fb-down");
    const reasonRow = cardEl.querySelector(".fb-reason");
    const reasonInput = cardEl.querySelector(".fb-reason-input");
    const saveBtn = cardEl.querySelector(".fb-save");
    const skipBtn = cardEl.querySelector(".fb-skip");
    let pendingVote = null;

    function openReason(vote) {
      pendingVote = vote;
      if (!reasonRow) return;
      reasonRow.hidden = false;
      // Pre-fill with prior reason if re-voting the same way
      const arr = loadFeedback();
      const monitorId = state.monitor && state.monitor.id || "unknown";
      const existing = arr[findVote(arr, monitorId, item.id)];
      reasonInput.value = (existing && existing.vote === vote && existing.reason) ? existing.reason : "";
      reasonInput.focus();
    }
    function commit(reason) {
      if (!pendingVote) return;
      recordVote(item, pendingVote, reason || "");
      pendingVote = null;
      if (reasonRow) reasonRow.hidden = true;
      paintCardFeedback(cardEl, item);
    }

    if (up)   up.addEventListener("click", () => openReason("up"));
    if (down) down.addEventListener("click", () => openReason("down"));
    if (saveBtn) saveBtn.addEventListener("click", () => commit(reasonInput.value));
    if (skipBtn) skipBtn.addEventListener("click", () => commit(""));
    if (reasonInput) {
      reasonInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") { e.preventDefault(); commit(reasonInput.value); }
        if (e.key === "Escape") { e.preventDefault(); if (reasonRow) reasonRow.hidden = true; pendingVote = null; }
      });
    }
    paintCardFeedback(cardEl, item);
  }

  function buildBatchMarkdown(allVotes, unexported) {
    const now = new Date();
    const yyyy = now.getUTCFullYear();
    const mm = String(now.getUTCMonth() + 1).padStart(2, "0");
    const dd = String(now.getUTCDate()).padStart(2, "0");
    const hh = String(now.getUTCHours()).padStart(2, "0");
    const mi = String(now.getUTCMinutes()).padStart(2, "0");
    const batchId = "fb-" + yyyy + "-" + mm + "-" + dd + "-" + hh + mi;
    const isoNow = now.toISOString();

    // Group counts by monitor for the summary section
    const byMonitor = {};
    unexported.forEach(v => {
      const k = v.monitor_code || "—";
      if (!byMonitor[k]) byMonitor[k] = { up: 0, down: 0 };
      if (v.vote === "up") byMonitor[k].up++; else byMonitor[k].down++;
    });
    const summaryLines = Object.keys(byMonitor).sort().map(k => {
      const c = byMonitor[k];
      const total = c.up + c.down;
      return "- " + k + " · " + total + " " + (total === 1 ? "vote" : "votes") +
             " (" + c.up + " up · " + c.down + " down)";
    });

    const head =
      "---\n" +
      "batch-id: " + batchId + "\n" +
      "generated-at: " + isoNow + "\n" +
      "generated-by: website-feedback-widget v" + FEEDBACK_WIDGET_VERSION + "\n" +
      "votes: " + unexported.length + "\n" +
      "votes-up: " + unexported.filter(v => v.vote === "up").length + "\n" +
      "votes-down: " + unexported.filter(v => v.vote === "down").length + "\n" +
      "status: ready-for-feedback-integration\n" +
      "---\n\n" +
      "# Feedback batch — " + yyyy + "-" + mm + "-" + dd + " · " + unexported.length +
      " new " + (unexported.length === 1 ? "vote" : "votes") + "\n\n" +
      "## Summary by monitor\n\n" + (summaryLines.length ? summaryLines.join("\n") : "_(no votes in this batch)_") + "\n\n" +
      "## Votes\n\n";

    const body = unexported.map(v => {
      const icon = v.vote === "up" ? "👍 helpful" : "👎 not for me";
      const reason = v.reason ? '> ' + v.reason.replace(/\n/g, " ") + "\n\n" : "";
      return (
        "### " + (v.monitor_code || "—") + " · " + (v.theme || "—") + " · " + (v.title || "(untitled)") + "\n\n" +
        "- **Vote:** " + icon + "\n" +
        "- **Article ID:** `" + (v.article_id || "—") + "`\n" +
        "- **Monitor:** " + (v.monitor_code || "—") + " (`" + (v.monitor_id || "—") + "`)\n" +
        "- **Topic / Category:** " + (v.theme || "—") + (v.catLabel ? " (" + v.catLabel + ")" : "") + "\n" +
        (v.country ? "- **Country:** " + v.country + "\n" : "") +
        (v.url ? "- **URL:** " + v.url + "\n" : "") +
        "- **Voted at:** " + v.voted_at + "\n\n" +
        reason
      );
    }).join("");

    const tail =
      "## What the Orchestrator should do with this\n\n" +
      "1. Re-thread these articles against the dimensions in `system/skills/feedback-integration.md` — keywords, source tiers, ranking rules, theory-of-harm tags.\n" +
      "2. Watch for clusters (≥3 down-votes on the same theme / source / jurisdiction) before changing weights — per CLAUDE.md Rule 6, one 👎 is a signal, not a verdict.\n" +
      "3. Output a delta report to `generated/reports/" + yyyy + "-" + mm + "-" + dd + "-feedback-delta.md`. Never edit prior findings or briefs.\n" +
      "4. Archive this batch to `queue/feedback/_processed/" + yyyy + "-" + mm + "-" + dd + "/` once the delta report is written.\n";

    return { filename: batchId + ".md", markdown: head + body + tail };
  }

  function exportFeedback() {
    const all = loadFeedback();
    const unexported = all.filter(v => !v.exported_at);
    if (!unexported.length) {
      alert("No new feedback to export. (Total stored: " + all.length + ")");
      return;
    }
    const { filename, markdown } = buildBatchMarkdown(all, unexported);
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename; document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 800);

    // Mark exported
    const stamp = new Date().toISOString();
    const next = all.map(v => v.exported_at ? v : Object.assign({}, v, { exported_at: stamp }));
    saveFeedback(next);
    updateFeedbackBadge();
    // Repaint visible cards so the "exported" hint appears
    state.items.forEach(it => {
      const card = document.querySelector('[data-card-id="' + cssEscape(it.id) + '"]');
      if (card) paintCardFeedback(card, it);
    });
  }
  function clearFeedback() {
    if (!loadFeedback().length) { alert("Nothing to clear."); return; }
    const ok = confirm("Clear ALL stored feedback from this browser? This cannot be undone. (Already-exported batches in your repo are not affected.)");
    if (!ok) return;
    saveFeedback([]);
    updateFeedbackBadge();
    state.items.forEach(it => {
      const card = document.querySelector('[data-card-id="' + cssEscape(it.id) + '"]');
      if (card) paintCardFeedback(card, it);
    });
  }
  function cssEscape(s) {
    // Minimal CSS attribute selector escape — good enough for ids like "samr-tencent"
    return String(s).replace(/(["\\])/g, "\\$1");
  }

  function updateFeedbackBadge() {
    const badge = $("#fb-badge");
    if (!badge) return;
    const n = unexportedCount();
    badge.textContent = n;
    badge.classList.toggle("has", n > 0);
    const total = $("#fb-panel-total");
    const newCt = $("#fb-panel-new");
    if (total) total.textContent = totalVoteCount();
    if (newCt) newCt.textContent = n;
  }

  /* =====================================================================
     RENDERERS
     ===================================================================== */
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
      return '<article class="card" data-card-id="' + esc(it.id) + '">' +
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
        feedbackWidgetHTML() +
      "</article>";
    }).join("");

    // Wire up the feedback widget on each freshly-rendered card.
    $$(".card").forEach((card, idx) => {
      const it = list[idx];
      if (it) wireCardFeedback(card, it);
    });

    $$(".tab").forEach(t => {
      const v = t.dataset.view;
      const ct = v === "all" ? state.items.length : countByTopic(v);
      const span = t.querySelector(".tab-ct");
      if (span) span.textContent = ct;
    });
  }

  /* =====================================================================
     CHROME MOUNTERS
     ===================================================================== */
  function mountThemePicker() {
    const btn = $("#theme-toggle");
    const menu = $("#theme-menu");
    if (!btn || !menu) return;
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
    const input = $("#search-input");
    if (!input) return;
    input.addEventListener("input", (e) => {
      state.q = e.target.value.trim();
      renderItems();
    });
  }

  function mountFeedbackPanel() {
    // The button + dropdown is injected next to the theme toggle, so any
    // existing monitor page that has the standard topbar gets the widget
    // automatically (no per-page markup changes required).
    const themeContainer = $("#theme-toggle") && $("#theme-toggle").parentElement;
    if (!themeContainer) return;

    const wrap = document.createElement("div");
    wrap.style.position = "relative";
    wrap.style.marginRight = "8px";
    wrap.innerHTML =
      '<button class="theme-toggle fb-toggle" id="fb-toggle" aria-haspopup="true" aria-expanded="false" title="Your feedback on this monitor">' +
        'Feedback <span class="fb-badge" id="fb-badge">0</span>' +
      '</button>' +
      '<div class="theme-menu fb-panel" id="fb-panel" role="menu">' +
        '<div class="fb-panel-head">Your feedback (local to this browser)</div>' +
        '<div class="fb-panel-stat"><b id="fb-panel-new">0</b> new since last export</div>' +
        '<div class="fb-panel-stat fb-panel-stat-soft"><b id="fb-panel-total">0</b> total votes stored</div>' +
        '<button class="fb-panel-btn fb-panel-export" id="fb-export">Export new votes as Markdown…</button>' +
        '<button class="fb-panel-btn fb-panel-clear" id="fb-clear">Clear local feedback…</button>' +
        '<div class="fb-panel-help">' +
          'Export saves a <code>fb-YYYY-MM-DD-HHMM.md</code> file. Drop it into ' +
          '<code>queue/feedback/inbox/</code> in your repo. ' +
          'See <code>system/skills/feedback-integration.md</code> for what happens next.' +
        '</div>' +
      '</div>';
    themeContainer.parentNode.insertBefore(wrap, themeContainer);

    const btn = $("#fb-toggle");
    const panel = $("#fb-panel");
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = panel.hasAttribute("open");
      if (open) panel.removeAttribute("open"); else panel.setAttribute("open", "");
    });
    document.addEventListener("click", (e) => {
      if (!panel.contains(e.target) && e.target !== btn) panel.removeAttribute("open");
    });
    $("#fb-export").addEventListener("click", () => { exportFeedback(); panel.removeAttribute("open"); });
    $("#fb-clear").addEventListener("click", () => { clearFeedback(); panel.removeAttribute("open"); });
    updateFeedbackBadge();
  }

  async function boot() {
    mountThemePicker();
    mountSearch();
    mountFeedbackPanel();
    // Prefer inline data (works over file:// and CDN both); fall back to fetch.
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
      updateFeedbackBadge();
    } catch (err) {
      console.error("Monitor failed to load", err);
      const grid = $("#item-grid");
      if (grid) grid.innerHTML =
        '<div class="empty"><h3>Monitor data didn\'t load</h3>' +
        '<p>Check that <code>monitor.json</code> and <code>items.json</code> exist next to this page, ' +
        'or that the inline <code>MONITOR_DATA</code> / <code>ITEMS_DATA</code> blocks are present.</p></div>';
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
