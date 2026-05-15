/* =====================================================================
   Legal Intelligence Briefing - universal monitor renderer
   Expects two files alongside the page: monitor.json + items.json
   (or inline window.MONITOR_DATA / window.ITEMS_DATA for file:// use).

   v0.3 - per-article feedback widget + export-to-markdown loop.
   v0.4 (2026-05-14) - archive layer (>ARCHIVE_DAYS old items hidden)
                       + topbar Export panel (MD / HTML / Slack / PDF).
   v0.5 (2026-05-15) - Direction B build:
     * Combobox filter bar (Country / Risk / When) above the items list
     * Export moves from dropdown to right-side drawer + backdrop
     * Card risk-class (.risk-high / .risk-med / .risk-low) drives
       the Pattern C left-border accent
   Storage keys preserved: lib-theme, lib-feedback-v1, lib-export-v1.
   monitor.json + items.json schemas unchanged.
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
  const FEEDBACK_WIDGET_VERSION = "0.3.1";
  const EXPORT_STATE_KEY = "lib-export-v1";
  const EXPORT_VERSION = "0.4";
  const ARCHIVE_DAYS = 14;

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

  // v0.5: filters added. countries[], risks[], when ('all' | 'today' | 'last7' | 'last30').
  const state = {
    monitor: null,
    items: [],
    view: "all",
    q: "",
    filters: { countries: [], risks: [], when: "all" }
  };

  /* =====================================================================
     ARCHIVE LAYER - items older than ARCHIVE_DAYS are tagged _archived.
     The main page hides them from tabs, counters, search, and the grid.
     The Export drawer can opt them back in via its "include archive" toggle.
     ===================================================================== */
  function parseDate(dateStr) {
    if (!dateStr) return null;
    const d = new Date(dateStr);
    return isNaN(d.getTime()) ? null : d;
  }
  function daysBetween(a, b) {
    return Math.floor((a.getTime() - b.getTime()) / (1000 * 60 * 60 * 24));
  }
  function tagArchive(items) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return items.map(it => {
      const d = parseDate(it.date);
      const age = d ? daysBetween(today, d) : 0;
      return Object.assign({}, it, {
        _date: d,
        _ageDays: age,
        _archived: age > ARCHIVE_DAYS
      });
    });
  }
  function liveItems() { return state.items.filter(i => !i._archived); }
  function archivedItems() { return state.items.filter(i => i._archived); }


  /* =====================================================================
     FEEDBACK - localStorage-backed thumbs widget + export-to-markdown.
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
    const monitorCode = state.monitor && state.monitor.code || "-";
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
        const verb = existing.vote === "up" ? "Pinned" : "Binned";
        const exported = existing.exported_at ? " - exported" : "";
        const reason = existing.reason ? ' - "' + existing.reason + '"' : "";
        status.hidden = false;
        status.textContent = verb + reason + exported;
      } else {
        status.hidden = true;
        status.textContent = "";
      }
    }
  }

  function feedbackWidgetHTML() {
    return (
      '<div class="fb" role="group" aria-label="Feedback on this article">' +
        '<button type="button" class="fb-btn fb-up"   aria-label="Pin - surface more like this">' +
          'Pin' +
        '</button>' +
        '<button type="button" class="fb-btn fb-down" aria-label="Bin - surface less like this">' +
          'Bin' +
        '</button>' +
        '<span class="fb-status" hidden></span>' +
        '<div class="fb-reason" hidden>' +
          '<input type="text" class="fb-reason-input" maxlength="240"' +
            ' placeholder="Optional - add a note (Enter to save)">' +
          '<button type="button" class="fb-save" title="Save note">Save note</button>' +
          '<button type="button" class="fb-skip" title="Close without a note" aria-label="Close note input">x</button>' +
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

    function existingVote() {
      const arr = loadFeedback();
      const monitorId = state.monitor && state.monitor.id || "unknown";
      return arr[findVote(arr, monitorId, item.id)] || null;
    }

    function castVote(vote) {
      const prior = existingVote();
      const reason = (prior && prior.vote === vote && prior.reason) ? prior.reason : "";
      recordVote(item, vote, reason);
      paintCardFeedback(cardEl, item);
      if (reasonRow) {
        reasonRow.hidden = false;
        reasonInput.value = reason;
        setTimeout(() => reasonInput.focus({ preventScroll: true }), 0);
      }
    }
    function saveNote() {
      const current = existingVote();
      if (!current) { if (reasonRow) reasonRow.hidden = true; return; }
      recordVote(item, current.vote, reasonInput.value);
      if (reasonRow) reasonRow.hidden = true;
      paintCardFeedback(cardEl, item);
    }
    function dismissNote() {
      if (reasonRow) reasonRow.hidden = true;
    }

    if (up)   up.addEventListener("click", () => castVote("up"));
    if (down) down.addEventListener("click", () => castVote("down"));
    if (saveBtn) saveBtn.addEventListener("click", saveNote);
    if (skipBtn) skipBtn.addEventListener("click", dismissNote);
    if (reasonInput) {
      reasonInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter")  { e.preventDefault(); saveNote(); }
        if (e.key === "Escape") { e.preventDefault(); dismissNote(); }
      });
    }
    paintCardFeedback(cardEl, item);
    if (reasonRow) reasonRow.hidden = true;
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

    const byMonitor = {};
    unexported.forEach(v => {
      const k = v.monitor_code || "-";
      if (!byMonitor[k]) byMonitor[k] = { up: 0, down: 0 };
      if (v.vote === "up") byMonitor[k].up++; else byMonitor[k].down++;
    });
    const summaryLines = Object.keys(byMonitor).sort().map(k => {
      const c = byMonitor[k];
      const total = c.up + c.down;
      return "- " + k + " - " + total + " " + (total === 1 ? "vote" : "votes") +
             " (" + c.up + " up - " + c.down + " down)";
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
      "# Feedback batch - " + yyyy + "-" + mm + "-" + dd + " - " + unexported.length +
      " new " + (unexported.length === 1 ? "vote" : "votes") + "\n\n" +
      "## Summary by monitor\n\n" + (summaryLines.length ? summaryLines.join("\n") : "_(no votes in this batch)_") + "\n\n" +
      "## Votes\n\n";

    const body = unexported.map(v => {
      const icon = v.vote === "up" ? "helpful" : "not for me";
      const reason = v.reason ? '> ' + v.reason.replace(/\n/g, " ") + "\n\n" : "";
      return (
        "### " + (v.monitor_code || "-") + " - " + (v.theme || "-") + " - " + (v.title || "(untitled)") + "\n\n" +
        "- **Vote:** " + icon + "\n" +
        "- **Article ID:** `" + (v.article_id || "-") + "`\n" +
        "- **Monitor:** " + (v.monitor_code || "-") + " (`" + (v.monitor_id || "-") + "`)\n" +
        "- **Topic / Category:** " + (v.theme || "-") + (v.catLabel ? " (" + v.catLabel + ")" : "") + "\n" +
        (v.country ? "- **Country:** " + v.country + "\n" : "") +
        (v.url ? "- **URL:** " + v.url + "\n" : "") +
        "- **Voted at:** " + v.voted_at + "\n\n" +
        reason
      );
    }).join("");

    const tail =
      "## What the Orchestrator should do with this\n\n" +
      "1. Re-thread these articles against the dimensions in `system/skills/feedback-integration.md` - keywords, source tiers, ranking rules, theory-of-harm tags.\n" +
      "2. Watch for clusters (>= 3 down-votes on the same theme / source / jurisdiction) before changing weights - per CLAUDE.md Rule 6, one down-vote is a signal, not a verdict.\n" +
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

    const stamp = new Date().toISOString();
    const next = all.map(v => v.exported_at ? v : Object.assign({}, v, { exported_at: stamp }));
    saveFeedback(next);
    updateFeedbackBadge();
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
     EXPORT - filterable weekly-brief export in four formats.
     ===================================================================== */
  const DEFAULT_EXPORT_STATE = {
    dateRange: "last7",
    dateFrom: "",
    dateTo: "",
    countries: [],
    themes: [],
    risks: [],
    includeArchive: false,
    format: "markdown"
  };
  let exportState = Object.assign({}, DEFAULT_EXPORT_STATE);

  function loadExportState() {
    try {
      const raw = localStorage.getItem(EXPORT_STATE_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === "object") {
        exportState = Object.assign({}, DEFAULT_EXPORT_STATE, parsed);
      }
    } catch (e) {}
  }
  function saveExportState() {
    try { localStorage.setItem(EXPORT_STATE_KEY, JSON.stringify(exportState)); } catch (e) {}
  }

  function dateWindow() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (exportState.dateRange === "all") {
      return { from: null, to: null, label: "all dates" };
    }
    if (exportState.dateRange === "custom") {
      const from = exportState.dateFrom ? parseDate(exportState.dateFrom) : null;
      const to   = exportState.dateTo   ? parseDate(exportState.dateTo)   : null;
      return {
        from: from, to: to,
        label: (from ? exportState.dateFrom : "earliest") + " -> " + (to ? exportState.dateTo : "latest")
      };
    }
    const days = exportState.dateRange === "last7" ? 7
              : exportState.dateRange === "last14" ? 14
              : 30;
    const from = new Date(today);
    from.setDate(from.getDate() - (days - 1));
    return { from: from, to: today, label: "last " + days + " days" };
  }

  function applyExportFilters() {
    const win = dateWindow();
    const cs = new Set(exportState.countries);
    const ts = new Set(exportState.themes);
    const rs = new Set(exportState.risks);
    return state.items.filter(it => {
      if (it._archived && !exportState.includeArchive) return false;
      if (win.from && (!it._date || it._date < win.from)) return false;
      if (win.to   && (!it._date || it._date > win.to))   return false;
      if (cs.size && !cs.has(it.country)) return false;
      if (ts.size && !ts.has(it.theme))   return false;
      if (rs.size && !rs.has(it.risk))    return false;
      return true;
    }).sort((a, b) => {
      const ad = a._date ? a._date.getTime() : 0;
      const bd = b._date ? b._date.getTime() : 0;
      if (bd !== ad) return bd - ad;
      const rank = { high: 0, med: 1, low: 2 };
      return (rank[a.risk] != null ? rank[a.risk] : 3) - (rank[b.risk] != null ? rank[b.risk] : 3);
    });
  }

  function exportFilterSummary(items) {
    const win = dateWindow();
    const m = state.monitor || {};
    return {
      monitor_code: m.code || "-",
      monitor_name: m.name || "",
      monitor_id: m.id || "",
      generated_at: new Date().toISOString(),
      date_label: win.label,
      countries: exportState.countries.slice().sort(),
      themes: exportState.themes.slice().sort(),
      risks: exportState.risks.slice().sort(),
      include_archive: exportState.includeArchive,
      count: items.length,
      high: items.filter(i => i.risk === "high").length,
      med:  items.filter(i => i.risk === "med").length,
      low:  items.filter(i => i.risk === "low").length
    };
  }

  function pad2(n) { return String(n).padStart(2, "0"); }
  function isoStamp(d) {
    return d.getUTCFullYear() + "-" + pad2(d.getUTCMonth()+1) + "-" + pad2(d.getUTCDate()) +
           "-" + pad2(d.getUTCHours()) + pad2(d.getUTCMinutes());
  }
  function exportFilenameBase() {
    const m = state.monitor || {};
    const code = (m.code || "monitor").toLowerCase().replace(/[^a-z0-9]+/g, "-");
    return code + "-brief-" + isoStamp(new Date());
  }

  function buildExportMarkdown(items, meta) {
    const head =
      "---\n" +
      "monitor: " + meta.monitor_code + " - " + meta.monitor_name + "\n" +
      "monitor-id: " + meta.monitor_id + "\n" +
      "generated-at: " + meta.generated_at + "\n" +
      "generated-by: website-export v" + EXPORT_VERSION + "\n" +
      "date-window: " + meta.date_label + "\n" +
      (meta.countries.length ? "countries: [" + meta.countries.join(", ") + "]\n" : "countries: all\n") +
      (meta.themes.length    ? "themes: [" + meta.themes.join(", ") + "]\n"       : "themes: all\n") +
      (meta.risks.length     ? "risks: [" + meta.risks.join(", ") + "]\n"         : "risks: all\n") +
      "include-archive: " + (meta.include_archive ? "true" : "false") + "\n" +
      "items: " + meta.count + " (high " + meta.high + " | med " + meta.med + " | low " + meta.low + ")\n" +
      "---\n\n" +
      "# " + meta.monitor_code + " - Regulatory Brief\n" +
      "_" + meta.date_label + " | " + meta.count + " " + (meta.count === 1 ? "item" : "items") + "_\n\n";
    if (!items.length) return head + "_No items match the selected filters._\n";
    const groups = {};
    items.forEach(it => {
      const k = it.catLabel || it.theme || "Other";
      (groups[k] = groups[k] || []).push(it);
    });
    const body = Object.keys(groups).sort().map(k => {
      const block = groups[k];
      const h = "## " + k + " (" + block.length + ")\n\n";
      const lines = block.map(it => {
        const risk = (it.risk || "low").toUpperCase();
        const line1 = "### " + (it.title || "(untitled)") + "\n";
        const meta1 =
          "- **" + risk + "** | " + (it.countryLabel || it.country || "-") +
          " | " + (it.dateLabel || it.date || "-") +
          (it.rule ? " | " + it.rule : "") +
          (it._archived ? " | _archived_" : "") + "\n" +
          (it.source ? "- Source: " + (it.url ? "[" + it.source + "](" + it.url + ")" : it.source) + "\n" : "") +
          (it.co ? "- OpCos: **" + it.co + "**\n" : "") +
          (it.owner ? "- Owner: " + it.owner + (it.ownerTeam ? " | " + it.ownerTeam : "") + "\n" : "");
        const body1 = it.body ? "\n" + it.body + "\n" : "";
        const why1  = it.why  ? "\n> **Why it matters ->** " + it.why + "\n" : "";
        return line1 + meta1 + body1 + why1 + "\n";
      }).join("");
      return h + lines;
    }).join("");
    return head + body;
  }

  function buildExportSlack(items, meta) {
    const head =
      "*" + meta.monitor_code + " - Regulatory Brief* | " + meta.date_label + "\n" +
      "_" + meta.count + " items | " + meta.high + " high | " + meta.med + " med | " + meta.low + " low" +
      (meta.countries.length ? " | " + meta.countries.join("/") : "") +
      "_\n\n";
    if (!items.length) return head + "_No items match the selected filters._";
    const body = items.map(it => {
      const riskTag = it.risk === "high" ? ":red_circle:"
                    : it.risk === "med"  ? ":large_orange_circle:"
                    : ":large_green_circle:";
      const country = it.countryLabel || it.country || "-";
      const date = it.dateLabel || it.date || "-";
      const titleLine = it.url
        ? riskTag + " *<" + it.url + "|" + (it.title || "(untitled)") + ">*"
        : riskTag + " *" + (it.title || "(untitled)") + "*";
      const meta1 = "_" + country + " | " + date +
        (it.catLabel ? " | " + it.catLabel : "") +
        (it.rule ? " | " + it.rule : "") +
        (it.source ? " | " + it.source : "") + "_";
      const why = it.why ? "\n> " + it.why.replace(/\n/g, " ") : "";
      return titleLine + "\n" + meta1 + why;
    }).join("\n\n");
    const footer = "\n\n_Generated by " + meta.monitor_code + " export v" + EXPORT_VERSION + " | " + meta.generated_at.slice(0, 16).replace("T", " ") + " UTC_";
    return head + body + footer;
  }

  function buildExportHTML(items, meta) {
    const css =
      "body{font-family:Verdana,Geneva,Tahoma,sans-serif;color:#1B0838;background:#fff;margin:32px;line-height:1.55;}" +
      "h1{font-size:22px;margin:0 0 4px;color:#370180;}" +
      "h2{font-size:16px;margin:24px 0 8px;color:#5715B0;border-bottom:0.5px solid #ddd;padding-bottom:4px;}" +
      "h3{font-size:14px;margin:14px 0 4px;color:#1B0838;}" +
      ".meta{font-size:11.5px;color:#666;margin-bottom:16px;}" +
      ".item{margin-bottom:14px;padding-bottom:10px;border-bottom:0.5px dashed #eee;page-break-inside:avoid;border-left:3px solid #bbb;padding-left:12px;}" +
      ".item.high{border-left-color:#D90276;}" +
      ".item.med{border-left-color:#FC9628;}" +
      ".item.low{border-left-color:#0DAC8B;}" +
      ".tags{font-size:11px;color:#555;margin:2px 0 6px;}" +
      ".tag{display:inline-block;padding:1px 7px;border-radius:6px;border:0.5px solid #ddd;margin-right:4px;background:#f7f3ea;}" +
      ".tag.high{background:#FBE0EF;color:#AF015F;border-color:#f0c6d8;}" +
      ".tag.med{background:#FFF1DC;color:#A35B00;border-color:#f0d8b0;}" +
      ".tag.low{background:#DDF5EE;color:#00854E;border-color:#bfe4d6;}" +
      ".tag.archived{background:#eee;color:#888;}" +
      ".body{font-size:13px;color:#333;margin:4px 0;}" +
      ".why{border-left:2px solid #D90276;padding:2px 0 2px 10px;font-size:12px;margin:6px 0;}" +
      ".foot{font-size:11px;color:#888;margin-top:32px;border-top:0.5px solid #ddd;padding-top:8px;}" +
      "a{color:#5715B0;}" +
      "@media print { body{margin:14mm;} h2{break-after:avoid;} }";
    const safe = (s) => esc(s == null ? "" : s);
    const itemsHTML = items.length
      ? items.map(it => {
          const riskClass = it.risk || "low";
          const riskLabel = (it.risk || "low").toUpperCase();
          return '<div class="item ' + riskClass + '">' +
            '<h3>' + (it.url ? '<a href="' + safe(it.url) + '" target="_blank" rel="noopener">' + safe(it.title) + " &#8599;</a>" : safe(it.title)) + "</h3>" +
            '<div class="tags">' +
              '<span class="tag ' + riskClass + '">' + riskLabel + "</span>" +
              (it.countryLabel ? '<span class="tag">' + safe(it.countryLabel) + "</span>" : "") +
              (it.catLabel ? '<span class="tag">' + safe(it.catLabel) + "</span>" : "") +
              (it.dateLabel ? '<span class="tag">' + safe(it.dateLabel) + "</span>" : "") +
              (it.rule ? '<span class="tag">' + safe(it.rule) + "</span>" : "") +
              (it.source ? '<span class="tag">' + safe(it.source) + "</span>" : "") +
              (it._archived ? '<span class="tag archived">archived</span>' : "") +
            "</div>" +
            (it.body ? '<div class="body">' + safe(it.body) + "</div>" : "") +
            (it.why ? '<div class="why"><b>Why it matters -&gt;</b> ' + safe(it.why) + "</div>" : "") +
            (it.co || it.owner ?
              '<div class="tags">' +
                (it.co ? '<span class="tag">OpCos: ' + safe(it.co) + "</span>" : "") +
                (it.owner ? '<span class="tag">' + safe(it.owner) + (it.ownerTeam ? " | " + safe(it.ownerTeam) : "") + "</span>" : "") +
              "</div>" : "") +
            "</div>";
        }).join("")
      : '<div class="item"><i>No items match the selected filters.</i></div>';
    const metaLine =
      "Window: " + safe(meta.date_label) +
      " | " + meta.count + " items (" + meta.high + " high | " + meta.med + " med | " + meta.low + " low)" +
      (meta.countries.length ? " | countries: " + meta.countries.join(", ") : " | countries: all") +
      (meta.themes.length    ? " | themes: " + meta.themes.join(", ")       : "") +
      (meta.risks.length     ? " | risks: " + meta.risks.join(", ")         : "") +
      (meta.include_archive ? " | includes archive" : "");
    return "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">" +
      "<title>" + safe(meta.monitor_code) + " - Regulatory Brief - " + safe(meta.date_label) + "</title>" +
      "<style>" + css + "</style></head><body>" +
      "<h1>" + safe(meta.monitor_code) + " - Regulatory Brief</h1>" +
      "<div class=\"meta\">" + metaLine + "</div>" +
      itemsHTML +
      "<div class=\"foot\">" +
        "Generated " + safe(meta.generated_at) + " | " + safe(meta.monitor_name) +
        " | website-export v" + EXPORT_VERSION +
        " | Privileged | Prosus internal + named external counsel" +
      "</div>" +
      "</body></html>";
  }

  function downloadBlob(filename, content, mime) {
    const blob = new Blob([content], { type: mime + ";charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 800);
  }
  function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise((resolve, reject) => {
      try {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.focus(); ta.select();
        const ok = document.execCommand("copy");
        ta.remove();
        ok ? resolve() : reject(new Error("execCommand failed"));
      } catch (e) { reject(e); }
    });
  }

  function runExport() {
    const items = applyExportFilters();
    const meta = exportFilterSummary(items);
    const base = exportFilenameBase();
    if (exportState.format === "markdown") {
      downloadBlob(base + ".md", buildExportMarkdown(items, meta), "text/markdown");
      flashExportStatus("Exported " + meta.count + " items -> " + base + ".md");
    } else if (exportState.format === "slack") {
      const text = buildExportSlack(items, meta);
      copyToClipboard(text).then(
        () => flashExportStatus("Copied Slack block to clipboard (" + meta.count + " items)"),
        () => {
          downloadBlob(base + "-slack.txt", text, "text/plain");
          flashExportStatus("Clipboard blocked - saved as " + base + "-slack.txt");
        }
      );
    } else if (exportState.format === "html") {
      const html = buildExportHTML(items, meta);
      const w = window.open("", "_blank");
      if (w) { w.document.write(html); w.document.close(); }
      else downloadBlob(base + ".html", html, "text/html");
      flashExportStatus("Opened printable brief (" + meta.count + " items)");
    } else if (exportState.format === "pdf") {
      const html = buildExportHTML(items, meta) +
        "<script>window.addEventListener('load', function(){setTimeout(function(){window.print();}, 200);});<\/script>";
      const w = window.open("", "_blank");
      if (w) { w.document.write(html); w.document.close(); }
      else downloadBlob(base + ".html", html, "text/html");
      flashExportStatus("Opened print dialog - choose Save as PDF");
    }
  }

  function flashExportStatus(msg) {
    const el = $("#ex-status");
    if (!el) return;
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(flashExportStatus._t);
    flashExportStatus._t = setTimeout(() => el.classList.remove("show"), 3500);
  }

  /* =====================================================================
     RENDERERS
     ===================================================================== */
  function renderChrome(m) {
    document.title = m.code + " - " + m.name + " - Legal Intelligence Briefing";
    $("#brand-product").innerHTML = "<b>" + esc(m.code) + "</b> - " + esc(m.name);

    const pill = $("#live-pill");
    pill.className = "live-pill " + (m.status || "live");
    $("#live-pill-label").textContent = m.status_label || (m.week_iso || "Live");

    const tabs = $("#tabs");
    tabs.innerHTML = "";
    tabs.appendChild(makeTab("all", "All items", liveItems().length));
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

    const live = liveItems();
    const high = live.filter(i => i.risk === "high").length;
    const med  = live.filter(i => i.risk === "med").length;
    $("#ct-total").textContent = live.length;
    $("#ct-high").textContent  = high;
    $("#ct-med").textContent   = med;
    $("#search-input").placeholder = "Search across " + live.length + " items...";

    $("#footer-meta").textContent =
      (m.privilege_note || "Privileged - Prosus internal + named external counsel") +
      " - " + (m.week_label || "");
    $("#footer-gen").textContent =
      "Generated " + (m.generated_at || "-") + " - v" + (m.version || "0.1");
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
    return liveItems().filter(i => i.theme === topicId).length;
  }

  function topicLookup() {
    const map = {};
    (state.monitor.topics || []).forEach(t => { map[t.id] = t; });
    return map;
  }

  function withinWhen(it) {
    const w = state.filters.when;
    if (w === "all") return true;
    if (!it._date) return false;
    const today = new Date(); today.setHours(0,0,0,0);
    const ms = today.getTime() - it._date.getTime();
    const day = 24 * 60 * 60 * 1000;
    if (w === "today")  return ms < day;
    if (w === "last7")  return ms < 7 * day;
    if (w === "last30") return ms < 30 * day;
    return true;
  }

  function matches(it) {
    if (it._archived) return false;
    if (state.view !== "all" && it.theme !== state.view) return false;
    if (state.filters.countries.length && state.filters.countries.indexOf(it.country) === -1) return false;
    if (state.filters.risks.length     && state.filters.risks.indexOf(it.risk) === -1)     return false;
    if (!withinWhen(it)) return false;
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
        "<p>Clear the search, the filter pills, or pick another tab.</p></div>";
      paintFilterBarSelections();
      return;
    }

    grid.innerHTML = list.map(it => {
      const topic = topics[it.theme] || {};
      const color = topic.color || "#5715B0";
      const domain = topic.label || it.theme;
      const r = it.risk === "high" ? "r-high" : it.risk === "med" ? "r-med" : "r-low";
      const rcls = it.risk === "high" ? "risk-high" : it.risk === "med" ? "risk-med" : "risk-low";
      const rl = it.risk === "high" ? "HIGH" : it.risk === "med" ? "MED" : "LOW";
      const ruleChip = it.rule ? '<span class="ctag ctag-rule">' + esc(it.rule) + "</span>" : "";
      const styleVars =
        "--topic-fg:" + color + ";" +
        "--topic-tint:" + hexToRgba(color, 0.10) + ";" +
        "--topic-border:" + hexToRgba(color, 0.28);
      return '<article class="card ' + rcls + '" data-card-id="' + esc(it.id) + '">' +
        '<header class="card-head">' +
          '<span class="ctag ctag-domain" data-topic-color style="' + styleVars + '">' + esc(domain) + "</span>" +
          (it.catLabel ? '<span class="ctag">' + esc(it.catLabel) + "</span>" : "") +
          (it.countryLabel ? '<span class="ctag ctag-loc">' + esc(it.countryLabel) + "</span>" : "") +
          (it.dateLabel ? '<span class="ctag ctag-date">' + esc(it.dateLabel) + "</span>" : "") +
          ruleChip +
          (it.source ? '<a class="ctag ctag-source" href="' + esc(it.url || "#") +
            '" target="_blank" rel="noopener">' + esc(it.source) + " &#8599;</a>" : "") +
          '<span class="risk-pill ' + r + '">' + rl + "</span>" +
        "</header>" +
        '<h3 class="card-title">' + esc(it.title) + "</h3>" +
        (it.body ? '<p class="card-body">' + esc(it.body) + "</p>" : "") +
        (it.why ? '<div class="card-why"><b>Why it matters -&gt;</b> ' + esc(it.why) + "</div>" : "") +
        '<footer class="card-foot">' +
          (it.co ? '<span class="opc">OpCos: <b>' + esc(it.co) + "</b></span>" : "") +
          (it.owner ? '<span class="owner">' + esc(it.owner) +
            (it.ownerTeam ? " - " + esc(it.ownerTeam) : "") + "</span>" : "") +
        "</footer>" +
        feedbackWidgetHTML() +
      "</article>";
    }).join("");

    $$(".card").forEach((card, idx) => {
      const it = list[idx];
      if (it) wireCardFeedback(card, it);
    });

    $$(".tab").forEach(t => {
      const v = t.dataset.view;
      const ct = v === "all" ? liveItems().length : countByTopic(v);
      const span = t.querySelector(".tab-ct");
      if (span) span.textContent = ct;
    });

    paintFilterBarSelections();
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
        '<button class="fb-panel-btn fb-panel-export" id="fb-export">Export new votes as Markdown...</button>' +
        '<button class="fb-panel-btn fb-panel-clear" id="fb-clear">Clear local feedback...</button>' +
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


  /* =====================================================================
     FILTER BAR (v0.5) - combobox pills below the tabs.
     Country / Risk / When; each pill opens a small popover with options.
     ===================================================================== */
  function mountFilterBar() {
    const tabs = $("#tabs");
    if (!tabs) return;
    let bar = $("#filter-bar");
    if (!bar) {
      bar = document.createElement("nav");
      bar.id = "filter-bar";
      bar.className = "filter-bar";
      bar.setAttribute("aria-label", "Filter items");
      tabs.parentNode.insertBefore(bar, tabs.nextSibling);
    }
    bar.innerHTML =
      '<span class="filter-bar-label">Filter</span>' +
      '<button type="button" class="filter-pill" data-pill="country" aria-haspopup="listbox">' +
        '<span class="filter-pill-text">Country</span><span class="filter-chev">v</span>' +
        '<div class="filter-pop" id="filter-pop-country" role="listbox"></div>' +
      '</button>' +
      '<button type="button" class="filter-pill" data-pill="risk" aria-haspopup="listbox">' +
        '<span class="filter-pill-text">Risk</span><span class="filter-chev">v</span>' +
        '<div class="filter-pop" id="filter-pop-risk" role="listbox">' +
          '<button data-risk="high">High <span class="pop-count" data-count="high">0</span></button>' +
          '<button data-risk="med">Medium <span class="pop-count" data-count="med">0</span></button>' +
          '<button data-risk="low">Low <span class="pop-count" data-count="low">0</span></button>' +
        '</div>' +
      '</button>' +
      '<button type="button" class="filter-pill" data-pill="when" aria-haspopup="listbox">' +
        '<span class="filter-pill-text">When</span><span class="filter-chev">v</span>' +
        '<div class="filter-pop" id="filter-pop-when" role="listbox">' +
          '<button data-when="today">Today</button>' +
          '<button data-when="last7">Last 7 days</button>' +
          '<button data-when="last30">Last 30 days</button>' +
          '<div class="filter-pop-divider"></div>' +
          '<button data-when="all">All time</button>' +
        '</div>' +
      '</button>' +
      '<button type="button" class="filter-pill-clear" id="filter-clear" disabled>Clear filters</button>';

    bar.addEventListener("click", (e) => {
      const trigger = e.target.closest(".filter-pill");
      if (trigger && !e.target.closest(".filter-pop")) {
        e.stopPropagation();
        const wasOpen = trigger.classList.contains("open");
        $$(".filter-pill", bar).forEach(p => p.classList.remove("open"));
        if (!wasOpen) trigger.classList.add("open");
        return;
      }
      const countryBtn = e.target.closest("[data-country]");
      if (countryBtn) {
        e.stopPropagation();
        toggleArrayFilter(state.filters.countries, countryBtn.dataset.country);
        countryBtn.classList.toggle("active");
        renderItems();
        paintFilterBarSelections();
        return;
      }
      const riskBtn = e.target.closest("[data-risk]");
      if (riskBtn) {
        e.stopPropagation();
        toggleArrayFilter(state.filters.risks, riskBtn.dataset.risk);
        riskBtn.classList.toggle("active");
        renderItems();
        paintFilterBarSelections();
        return;
      }
      const whenBtn = e.target.closest("[data-when]");
      if (whenBtn) {
        e.stopPropagation();
        state.filters.when = whenBtn.dataset.when;
        $$("#filter-pop-when button").forEach(b => b.classList.toggle("active", b === whenBtn));
        renderItems();
        paintFilterBarSelections();
        // Auto-close the When popover after a single pick
        const pill = whenBtn.closest(".filter-pill");
        if (pill) pill.classList.remove("open");
        return;
      }
      if (e.target.id === "filter-clear") {
        state.filters.countries = [];
        state.filters.risks = [];
        state.filters.when = "all";
        $$(".filter-pop button.active", bar).forEach(b => b.classList.remove("active"));
        renderItems();
        paintFilterBarSelections();
      }
    });

    document.addEventListener("click", (e) => {
      if (!bar.contains(e.target)) {
        $$(".filter-pill", bar).forEach(p => p.classList.remove("open"));
      }
    });
  }

  function toggleArrayFilter(arr, val) {
    const i = arr.indexOf(val);
    if (i >= 0) arr.splice(i, 1); else arr.push(val);
  }

  function refreshFilterBarOptions() {
    const bar = $("#filter-bar");
    if (!bar) return;
    const seen = {};
    liveItems().forEach(it => {
      if (!it.country) return;
      if (!seen[it.country]) seen[it.country] = { label: it.countryLabel || it.country, count: 0 };
      seen[it.country].count++;
    });
    const countries = Object.keys(seen).sort((a, b) => seen[b].count - seen[a].count);
    const cwrap = $("#filter-pop-country");
    if (cwrap) {
      cwrap.innerHTML = countries.length
        ? countries.map(c =>
            '<button data-country="' + esc(c) + '"' +
              (state.filters.countries.indexOf(c) >= 0 ? ' class="active"' : '') + '>' +
              esc(seen[c].label) +
              ' <span class="pop-count">' + seen[c].count + "</span>" +
            '</button>'
          ).join("")
        : '<div class="filter-pop-section-label">No countries yet</div>';
    }
    const risks = { high: 0, med: 0, low: 0 };
    liveItems().forEach(it => { if (risks[it.risk] != null) risks[it.risk]++; });
    $$("#filter-pop-risk [data-count]").forEach(span => {
      span.textContent = risks[span.dataset.count] || 0;
    });
  }

  function paintFilterBarSelections() {
    const bar = $("#filter-bar");
    if (!bar) return;
    // Country
    const cPill = bar.querySelector('[data-pill="country"]');
    if (cPill) {
      const txt = cPill.querySelector(".filter-pill-text");
      const n = state.filters.countries.length;
      if (n === 0) { txt.textContent = "Country"; cPill.classList.remove("has-value"); }
      else if (n === 1) {
        const c = state.filters.countries[0];
        const opt = bar.querySelector('[data-country="' + cssEscape(c) + '"]');
        const label = opt ? opt.firstChild.textContent.trim() : c;
        txt.textContent = "Country - " + label;
        cPill.classList.add("has-value");
      }
      else { txt.textContent = "Country - " + n; cPill.classList.add("has-value"); }
    }
    // Risk
    const rPill = bar.querySelector('[data-pill="risk"]');
    if (rPill) {
      const txt = rPill.querySelector(".filter-pill-text");
      const rs = state.filters.risks;
      if (rs.length === 0) { txt.textContent = "Risk"; rPill.classList.remove("has-value", "has-value-risk"); }
      else if (rs.length === 1) {
        const word = rs[0] === "high" ? "High" : rs[0] === "med" ? "Medium" : "Low";
        txt.textContent = "Risk - " + word;
        rPill.classList.add("has-value");
        if (rs[0] === "high") rPill.classList.add("has-value-risk"); else rPill.classList.remove("has-value-risk");
      }
      else { txt.textContent = "Risk - " + rs.length; rPill.classList.add("has-value"); rPill.classList.remove("has-value-risk"); }
    }
    // When
    const wPill = bar.querySelector('[data-pill="when"]');
    if (wPill) {
      const txt = wPill.querySelector(".filter-pill-text");
      const w = state.filters.when;
      if (w === "all") { txt.textContent = "When"; wPill.classList.remove("has-value"); }
      else {
        const map = { today: "Today", last7: "Last 7 days", last30: "Last 30 days" };
        txt.textContent = "When - " + (map[w] || w);
        wPill.classList.add("has-value");
      }
      $$("#filter-pop-when button").forEach(b => b.classList.toggle("active", b.dataset.when === w));
    }
    // Clear button enabled state
    const clr = $("#filter-clear");
    if (clr) {
      const dirty = state.filters.countries.length || state.filters.risks.length || state.filters.when !== "all";
      clr.disabled = !dirty;
    }
  }


  /* =====================================================================
     EXPORT DRAWER (Pattern 2) - right-side slide-in. Reuses the same
     control IDs (#ex-from, #ex-to, #ex-go, #ex-count, #ex-status, etc.)
     as the previous dropdown so all event handlers and rendering work
     unchanged. Differences: container is a fixed drawer with a backdrop,
     and the toggle opens/closes via .open class instead of [open] attr.
     ===================================================================== */
  function mountExportPanel() {
    loadExportState();
    const themeContainer = $("#theme-toggle") && $("#theme-toggle").parentElement;
    if (!themeContainer) return;

    const wrap = document.createElement("div");
    wrap.style.position = "relative";
    wrap.style.marginRight = "8px";
    wrap.innerHTML =
      '<button class="theme-toggle ex-toggle" id="ex-toggle" aria-haspopup="dialog" aria-expanded="false" title="Export a regulatory brief">' +
        'Export <span class="ex-badge" id="ex-badge">0</span>' +
      '</button>';
    themeContainer.parentNode.insertBefore(wrap, themeContainer);

    // Drawer + backdrop live at the end of body so they overlay everything.
    const backdrop = document.createElement("div");
    backdrop.className = "ex-backdrop";
    backdrop.id = "ex-backdrop";
    document.body.appendChild(backdrop);

    const drawer = document.createElement("aside");
    drawer.className = "ex-drawer";
    drawer.id = "ex-drawer";
    drawer.setAttribute("role", "dialog");
    drawer.setAttribute("aria-label", "Export a regulatory brief");
    drawer.innerHTML =
      '<div class="ex-drawer-head">' +
        '<div>' +
          '<div class="ex-eyebrow">Export</div>' +
          '<div class="ex-head">Build a regulatory brief</div>' +
        '</div>' +
        '<button class="ex-drawer-close" id="ex-close" aria-label="Close">x</button>' +
      '</div>' +
      '<div class="ex-drawer-body">' +
        '<div class="ex-section">' +
          '<div class="ex-label">Date window</div>' +
          '<div class="ex-row ex-row-segment" id="ex-daterange" role="radiogroup" aria-label="Date window">' +
            '<button data-range="last7"  class="ex-seg">Last 7d</button>' +
            '<button data-range="last14" class="ex-seg">Last 14d</button>' +
            '<button data-range="last30" class="ex-seg">Last 30d</button>' +
            '<button data-range="custom" class="ex-seg">Custom</button>' +
            '<button data-range="all"    class="ex-seg">All</button>' +
          '</div>' +
          '<div class="ex-row ex-row-custom" id="ex-custom" hidden>' +
            '<input type="date" id="ex-from" aria-label="From date">' +
            '<span class="ex-arrow">-&gt;</span>' +
            '<input type="date" id="ex-to" aria-label="To date">' +
          '</div>' +
        '</div>' +
        '<div class="ex-section">' +
          '<div class="ex-label">Country / jurisdiction</div>' +
          '<div class="ex-chiprow" id="ex-countries"></div>' +
        '</div>' +
        '<div class="ex-section">' +
          '<div class="ex-label">Theme</div>' +
          '<div class="ex-chiprow" id="ex-themes"></div>' +
        '</div>' +
        '<div class="ex-section">' +
          '<div class="ex-label">Risk</div>' +
          '<div class="ex-chiprow" id="ex-risks">' +
            '<button data-risk="high" class="ex-chip ex-chip-risk r-high">HIGH</button>' +
            '<button data-risk="med"  class="ex-chip ex-chip-risk r-med">MED</button>' +
            '<button data-risk="low"  class="ex-chip ex-chip-risk r-low">LOW</button>' +
          '</div>' +
        '</div>' +
        '<div class="ex-section ex-archive-row">' +
          '<label class="ex-check"><input type="checkbox" id="ex-archive"> Include archived items (&gt;' + ARCHIVE_DAYS + ' days old)</label>' +
          '<span class="ex-archive-count" id="ex-archive-count"></span>' +
        '</div>' +
        '<div class="ex-section">' +
          '<div class="ex-label">Format</div>' +
          '<div class="ex-row ex-row-segment" id="ex-format" role="radiogroup" aria-label="Export format">' +
            '<button data-format="markdown" class="ex-seg">Markdown</button>' +
            '<button data-format="html"     class="ex-seg">HTML</button>' +
            '<button data-format="slack"    class="ex-seg">Slack</button>' +
            '<button data-format="pdf"      class="ex-seg">PDF</button>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="ex-drawer-foot">' +
        '<div class="ex-actions">' +
          '<button class="ex-go" id="ex-go">Export <span id="ex-count">0</span> items</button>' +
          '<button class="ex-reset" id="ex-reset" title="Reset filters">Reset</button>' +
        '</div>' +
        '<div class="ex-status" id="ex-status"></div>' +
      '</div>';
    document.body.appendChild(drawer);

    const btn = $("#ex-toggle");

    function openDrawer() {
      drawer.classList.add("open");
      backdrop.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
      updateExportPreviewCount();
    }
    function closeDrawer() {
      drawer.classList.remove("open");
      backdrop.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    }

    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (drawer.classList.contains("open")) closeDrawer(); else openDrawer();
    });
    $("#ex-close").addEventListener("click", closeDrawer);
    backdrop.addEventListener("click", closeDrawer);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
    });

    $$("#ex-daterange .ex-seg").forEach(b => {
      b.addEventListener("click", () => {
        exportState.dateRange = b.dataset.range;
        $$("#ex-daterange .ex-seg").forEach(x => x.classList.toggle("active", x === b));
        $("#ex-custom").hidden = (exportState.dateRange !== "custom");
        saveExportState(); updateExportPreviewCount();
      });
    });
    $("#ex-from").addEventListener("change", (e) => { exportState.dateFrom = e.target.value; saveExportState(); updateExportPreviewCount(); });
    $("#ex-to").addEventListener("change",   (e) => { exportState.dateTo   = e.target.value; saveExportState(); updateExportPreviewCount(); });

    $$("#ex-risks .ex-chip-risk").forEach(b => {
      b.addEventListener("click", () => {
        const r = b.dataset.risk;
        const i = exportState.risks.indexOf(r);
        if (i >= 0) exportState.risks.splice(i, 1); else exportState.risks.push(r);
        b.classList.toggle("active");
        saveExportState(); updateExportPreviewCount();
      });
    });

    $("#ex-archive").addEventListener("change", (e) => {
      exportState.includeArchive = !!e.target.checked;
      saveExportState(); updateExportPreviewCount();
    });

    $$("#ex-format .ex-seg").forEach(b => {
      b.addEventListener("click", () => {
        exportState.format = b.dataset.format;
        $$("#ex-format .ex-seg").forEach(x => x.classList.toggle("active", x === b));
        saveExportState();
      });
    });

    $("#ex-go").addEventListener("click", () => { runExport(); });
    $("#ex-reset").addEventListener("click", () => {
      exportState = Object.assign({}, DEFAULT_EXPORT_STATE);
      saveExportState();
      paintExportPanelState();
      refreshExportPanelOptions();
      updateExportPreviewCount();
    });

    paintExportPanelState();
  }

  function paintExportPanelState() {
    $$("#ex-daterange .ex-seg").forEach(b => b.classList.toggle("active", b.dataset.range === exportState.dateRange));
    const cust = $("#ex-custom"); if (cust) cust.hidden = (exportState.dateRange !== "custom");
    const from = $("#ex-from"); if (from) from.value = exportState.dateFrom || "";
    const to   = $("#ex-to");   if (to)   to.value   = exportState.dateTo   || "";
    $$("#ex-risks .ex-chip-risk").forEach(b => b.classList.toggle("active", exportState.risks.indexOf(b.dataset.risk) >= 0));
    const arch = $("#ex-archive"); if (arch) arch.checked = !!exportState.includeArchive;
    $$("#ex-format .ex-seg").forEach(b => b.classList.toggle("active", b.dataset.format === exportState.format));
  }

  function refreshExportPanelOptions() {
    const m = state.monitor;
    if (!m) return;
    const seen = {};
    state.items.forEach(it => {
      if (!it.country) return;
      seen[it.country] = it.countryLabel || it.country;
    });
    const countries = Object.keys(seen).sort();
    const cwrap = $("#ex-countries");
    if (cwrap) {
      cwrap.innerHTML = countries.map(c =>
        '<button data-country="' + esc(c) + '" class="ex-chip ex-chip-country' +
          (exportState.countries.indexOf(c) >= 0 ? " active" : "") + '">' +
          esc(seen[c]) +
        "</button>"
      ).join("");
      $$("#ex-countries .ex-chip-country").forEach(b => {
        b.addEventListener("click", () => {
          const c = b.dataset.country;
          const i = exportState.countries.indexOf(c);
          if (i >= 0) exportState.countries.splice(i, 1); else exportState.countries.push(c);
          b.classList.toggle("active");
          saveExportState(); updateExportPreviewCount();
        });
      });
    }
    const twrap = $("#ex-themes");
    if (twrap) {
      const topics = (m.topics || []);
      twrap.innerHTML = topics.map(t =>
        '<button data-theme="' + esc(t.id) + '" class="ex-chip ex-chip-theme' +
          (exportState.themes.indexOf(t.id) >= 0 ? " active" : "") + '"' +
          (t.color ? ' style="--topic-color:' + esc(t.color) + '"' : "") + '>' +
          esc(t.label) +
        "</button>"
      ).join("");
      $$("#ex-themes .ex-chip-theme").forEach(b => {
        b.addEventListener("click", () => {
          const id = b.dataset.theme;
          const i = exportState.themes.indexOf(id);
          if (i >= 0) exportState.themes.splice(i, 1); else exportState.themes.push(id);
          b.classList.toggle("active");
          saveExportState(); updateExportPreviewCount();
        });
      });
    }
    const archCt = $("#ex-archive-count");
    if (archCt) {
      const n = archivedItems().length;
      archCt.textContent = n ? "(" + n + " archived)" : "(none yet)";
    }
    updateExportPreviewCount();
  }

  function updateExportPreviewCount() {
    const n = applyExportFilters().length;
    const c = $("#ex-count"); if (c) c.textContent = n;
    const badge = $("#ex-badge");
    if (badge) {
      badge.textContent = n;
      badge.classList.toggle("has", n > 0);
    }
  }

  async function boot() {
    mountThemePicker();
    mountSearch();
    mountFeedbackPanel();
    mountExportPanel();
    mountFilterBar();
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
      const rawItems = Array.isArray(items) ? items : (items.items || []);
      state.items = tagArchive(rawItems);
      renderChrome(m);
      refreshFilterBarOptions();
      renderItems();
      updateFeedbackBadge();
      refreshExportPanelOptions();
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
