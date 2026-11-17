/* ==================================================================
 * Evermore — main.js
 * Vanilla JavaScript only (no jQuery). One function per feature,
 * guard clauses for missing elements. Bootstrap's bundle is used only
 * for the collapsing mobile menu.
 * ================================================================== */
(function () {
  "use strict";

  /* ----------------------------------------------------------------
   * The event itself — used by the countdown and the .ics calendar
   * file. Edit these to match your wedding.
   * ---------------------------------------------------------------- */
  var EVENT = {
    title: "Clementine & Oliver's wedding",
    start: "2027-06-19T14:00:00+01:00",
    end: "2027-06-20T00:00:00+01:00",
    location: "Ashcombe Park, Lime Avenue, Little Wrenham, Kingsbridge, Oxfordshire OX29 4WR",
    description: "Ceremony at 2:00 pm in the Walled Garden, reception to follow in the Tithe Barn. Black tie optional. Details: hello@example.com",
    file: "clementine-oliver-wedding.ics"
  };

  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ----------------------------------------------------------------
   * Small helpers
   * ---------------------------------------------------------------- */
  function toast(message) {
    var el = document.getElementById("toastNote");
    if (!el) {
      el = document.createElement("div");
      el.id = "toastNote";
      el.className = "toast-note";
      el.setAttribute("role", "status");
      el.setAttribute("aria-live", "polite");
      document.body.appendChild(el);
    }
    el.textContent = message;
    el.classList.add("show");
    clearTimeout(toast.timer);
    toast.timer = setTimeout(function () { el.classList.remove("show"); }, 2600);
  }

  function icsDate(iso) {
    return new Date(iso).toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  }

  function icsText(value) {
    return String(value).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n");
  }

  function buildIcsUrl() {
    var lines = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//Evermore//Wedding Invitation//EN",
      "CALSCALE:GREGORIAN",
      "METHOD:PUBLISH",
      "BEGIN:VEVENT",
      "UID:" + icsDate(EVENT.start) + "-evermore@example.com",
      "DTSTAMP:" + icsDate(new Date().toISOString()),
      "DTSTART:" + icsDate(EVENT.start),
      "DTEND:" + icsDate(EVENT.end),
      "SUMMARY:" + icsText(EVENT.title),
      "LOCATION:" + icsText(EVENT.location),
      "DESCRIPTION:" + icsText(EVENT.description),
      "BEGIN:VALARM",
      "TRIGGER:-P7D",
      "ACTION:DISPLAY",
      "DESCRIPTION:" + icsText(EVENT.title + " is in one week"),
      "END:VALARM",
      "END:VEVENT",
      "END:VCALENDAR"
    ];
    /* RFC 5545: fold lines longer than 75 octets */
    lines = lines.map(function (line) {
      var out = [];
      while (line.length > 73) { out.push(line.slice(0, 73)); line = " " + line.slice(73); }
      out.push(line);
      return out.join("\r\n");
    });
    var blob = new Blob([lines.join("\r\n")], { type: "text/calendar;charset=utf-8" });
    return URL.createObjectURL(blob);
  }

  /* ----------------------------------------------------------------
   * Envelope intro: press the seal, the flap lifts, the card slides
   * out and the page appears. Skippable (button or Escape). The head
   * script decides whether it shows at all.
   * ---------------------------------------------------------------- */
  function initIntro() {
    var intro = document.getElementById("envelopeIntro");
    if (!intro) return;
    var root = document.documentElement;

    if (!root.classList.contains("intro-on") || reduceMotion) {
      root.classList.remove("intro-on");
      intro.remove();
      return;
    }

    try { sessionStorage.setItem("evermore-intro", "seen"); } catch (e) { /* storage blocked */ }

    var openBtn = intro.querySelector("[data-intro-open]");
    var skipBtn = intro.querySelector("[data-intro-skip]");
    var page = document.querySelectorAll(".site-header, main, .site-footer, .skip-link");
    var heading = document.getElementById("coupleNames");
    var done = false;

    page.forEach(function (el) { el.inert = true; });
    if (openBtn) openBtn.focus();

    function finish() {
      if (done) return;
      done = true;
      intro.classList.add("is-leaving");
      setTimeout(function () {
        root.classList.remove("intro-on");
        page.forEach(function (el) { el.inert = false; });
        intro.remove();
        if (heading) {
          heading.setAttribute("tabindex", "-1");
          heading.focus({ preventScroll: true });
        }
      }, 650);
    }

    function open() {
      if (intro.classList.contains("is-opening")) return;
      intro.classList.add("is-opening");
      setTimeout(finish, 2100);
    }

    if (openBtn) openBtn.addEventListener("click", open);
    if (skipBtn) skipBtn.addEventListener("click", finish);

    intro.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { finish(); return; }
      if (e.key !== "Tab") return;
      var items = [skipBtn, openBtn].filter(function (b) { return b && !b.disabled; });
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ----------------------------------------------------------------
   * Mobile menu: close it after a link is tapped.
   * ---------------------------------------------------------------- */
  function initNav() {
    var collapse = document.getElementById("primaryNav");
    if (!collapse) return;
    collapse.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (!collapse.classList.contains("show") || !window.bootstrap) return;
        var inst = window.bootstrap.Collapse.getOrCreateInstance(collapse, { toggle: false });
        inst.hide();
      });
    });
  }

  /* ----------------------------------------------------------------
   * Header hairline + shadow once the page scrolls.
   * ---------------------------------------------------------------- */
  function initStickyHeader() {
    var header = document.getElementById("siteHeader");
    if (!header) return;
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 10); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ----------------------------------------------------------------
   * Highlight the nav link of the section in view.
   * ---------------------------------------------------------------- */
  function initScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".nav-menu [data-spy]"));
    if (!links.length || !("IntersectionObserver" in window)) return;
    var map = {};
    links.forEach(function (link) { map[link.getAttribute("data-spy")] = link; });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove("active"); l.removeAttribute("aria-current"); });
        var active = map[entry.target.id];
        if (active) { active.classList.add("active"); active.setAttribute("aria-current", "location"); }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(map).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }

  /* ----------------------------------------------------------------
   * Fade sections up as they scroll into view.
   * ---------------------------------------------------------------- */
  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (!els.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in");
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (el) { observer.observe(el); });
  }

  /* ----------------------------------------------------------------
   * Countdown to the ceremony.
   * ---------------------------------------------------------------- */
  function initCountdown() {
    var box = document.querySelector("[data-countdown]");
    if (!box) return;
    var target = new Date(box.getAttribute("data-countdown")).getTime();
    if (isNaN(target)) return;
    var units = {};
    box.querySelectorAll("[data-unit]").forEach(function (el) { units[el.getAttribute("data-unit")] = el; });
    var timer;

    function pad(n, len) { n = String(n); while (n.length < len) n = "0" + n; return n; }
    function tick() {
      var diff = target - Date.now();
      if (diff <= 0) {
        box.classList.add("is-done");
        clearInterval(timer);
        return;
      }
      var s = Math.floor(diff / 1000);
      if (units.days) units.days.textContent = pad(Math.floor(s / 86400), 2);
      if (units.hours) units.hours.textContent = pad(Math.floor(s % 86400 / 3600), 2);
      if (units.minutes) units.minutes.textContent = pad(Math.floor(s % 3600 / 60), 2);
      if (units.seconds) units.seconds.textContent = pad(s % 60, 2);
    }
    tick();
    timer = setInterval(tick, 1000);
  }

  /* ----------------------------------------------------------------
   * "Add to calendar" buttons download an .ics file built in the browser.
   * ---------------------------------------------------------------- */
  function initCalendar() {
    document.querySelectorAll("[data-ics]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var a = document.createElement("a");
        a.href = buildIcsUrl();
        a.download = EVENT.file;
        document.body.appendChild(a);
        a.click();
        a.remove();
        toast("Calendar file saved: " + EVENT.file);
      });
    });
  }

  /* ----------------------------------------------------------------
   * Copy the venue address.
   * ---------------------------------------------------------------- */
  function initCopy() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      var label = btn.querySelector("[data-copy-label]");
      var original = label ? label.textContent : "";
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-copy");
        var done = function () {
          if (label) label.textContent = "Address copied";
          toast("Address copied to your clipboard");
          setTimeout(function () { if (label) label.textContent = original; }, 2400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () { toast(text); });
        } else {
          toast(text);
        }
      });
    });
  }

  /* ----------------------------------------------------------------
   * Accessible tabs (directions): arrow keys, Home/End.
   * ---------------------------------------------------------------- */
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (wrap) {
      var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
      if (!tabs.length) return;

      function select(tab, focus) {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", on ? "true" : "false");
          t.tabIndex = on ? 0 : -1;
          var panel = document.getElementById(t.getAttribute("aria-controls"));
          if (panel) panel.hidden = !on;
        });
        if (focus) tab.focus();
      }

      tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { select(tab, false); });
        tab.addEventListener("keydown", function (e) {
          var next = null;
          if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
          else if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
          else if (e.key === "Home") next = tabs[0];
          else if (e.key === "End") next = tabs[tabs.length - 1];
          if (next) { e.preventDefault(); select(next, true); }
        });
      });
      select(tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0] || tabs[0], false);
    });
  }

  /* ----------------------------------------------------------------
   * Character counter for the message to the couple.
   * ---------------------------------------------------------------- */
  function initCharCount() {
    document.querySelectorAll("[data-count-for]").forEach(function (hint) {
      var field = document.getElementById(hint.getAttribute("data-count-for"));
      if (!field) return;
      var max = parseInt(field.getAttribute("maxlength"), 10) || 400;
      var update = function () {
        var left = max - field.value.length;
        hint.textContent = left + " of " + max + " characters left";
        hint.classList.toggle("is-near", left <= 40);
      };
      field.addEventListener("input", update);
      update();
    });
  }

  /* ----------------------------------------------------------------
   * RSVP form: conditional sections, validation, success state.
   * Front-end only — connect the form to a form service to receive replies.
   * ---------------------------------------------------------------- */
  function initRsvpForm() {
    var form = document.querySelector("[data-rsvp-form]");
    if (!form) return;
    var card = document.getElementById("replyCard");
    var success = document.getElementById("replySuccess");
    var summary = document.getElementById("errorSummary");
    var conditionals = Array.prototype.slice.call(form.querySelectorAll("[data-show-when]"));
    var attempted = false;

    form.setAttribute("novalidate", "");

    function valueOf(name) {
      var field = form.elements[name];
      if (!field) return "";
      var first = field.tagName ? field : field[0];
      if (first && first.disabled) return "";
      return (field.value || "").trim();
    }

    function matches(rule) {
      var parts = rule.split("=");
      return valueOf(parts[0]) === parts[1];
    }

    /* Show or hide each conditional block, then disable every control
       that sits inside a hidden block so it is skipped and not submitted. */
    function applyConditions() {
      conditionals.forEach(function (block) {
        var parentHidden = block.parentElement.closest(".conditional[hidden]");
        block.hidden = !!parentHidden || !matches(block.getAttribute("data-show-when"));
      });
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.tagName === "BUTTON" || el.tagName === "FIELDSET") return;
        el.disabled = !!el.closest(".conditional[hidden]");
      });
    }

    var rules = [
      { name: "guest_name", target: "guestName", test: function (v) { return v.length >= 2; }, msg: "Please add your name as it appears on your invitation." },
      { name: "email", target: "guestEmail", test: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }, msg: "Please add an email address we can reach you on, like name@example.com." },
      { name: "attending", target: "attendingGroup", group: true, msg: "Please let us know whether you can join us." },
      { name: "plus_one", target: "plusOneGroup", group: true, msg: "Please tell us whether you are bringing a guest." },
      { name: "plus_one_name", target: "plusOneName", msg: "Please add your guest\u2019s full name." },
      { name: "plus_one_main", target: "plusOneMain", msg: "Please choose a main course for your guest." },
      { name: "starter", target: "starterGroup", group: true, msg: "Please choose a starter." },
      { name: "main", target: "mainGroup", group: true, msg: "Please choose a main course." },
      { name: "dessert", target: "dessertGroup", group: true, msg: "Please choose a dessert." }
    ];

    function isActive(rule) {
      var field = form.elements[rule.name];
      if (!field) return false;
      var first = field.tagName ? field : field[0];
      return !!first && !first.disabled;
    }

    function setError(rule, message) {
      var target = document.getElementById(rule.target);
      var holder = form.querySelector('[data-error-for="' + rule.target + '"]');
      if (holder) holder.textContent = message || "";
      if (!target) return;
      if (rule.group) {
        target.classList.toggle("is-invalid-group", !!message);
        target.querySelectorAll('input[name="' + rule.name + '"]').forEach(function (r) {
          if (message) r.setAttribute("aria-invalid", "true"); else r.removeAttribute("aria-invalid");
        });
      } else if (message) {
        target.setAttribute("aria-invalid", "true");
      } else {
        target.removeAttribute("aria-invalid");
      }
    }

    function focusTarget(rule) {
      var target = document.getElementById(rule.target);
      if (!target) return;
      var el = rule.group ? target.querySelector("input:not([disabled])") : target;
      if (el) el.focus();
    }

    function validate() {
      var errors = [];
      rules.forEach(function (rule) {
        if (!isActive(rule)) { setError(rule, ""); return; }
        var v = valueOf(rule.name);
        var ok = rule.test ? rule.test(v) : v !== "";
        setError(rule, ok ? "" : rule.msg);
        if (!ok) errors.push(rule);
      });
      return errors;
    }

    function showSummary(errors) {
      if (!summary) return;
      var list = summary.querySelector("ul");
      list.innerHTML = "";
      errors.forEach(function (rule) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#" + rule.target;
        a.textContent = rule.msg;
        a.addEventListener("click", function (e) { e.preventDefault(); focusTarget(rule); });
        li.appendChild(a);
        list.appendChild(li);
      });
      summary.hidden = errors.length === 0;
    }

    function addRow(dl, term, detail) {
      if (!detail) return;
      var row = document.createElement("div");
      var dt = document.createElement("dt");
      var dd = document.createElement("dd");
      dt.textContent = term;
      dd.textContent = detail;
      row.appendChild(dt);
      row.appendChild(dd);
      dl.appendChild(row);
    }

    function showSuccess() {
      if (!success) return;
      var name = valueOf("guest_name");
      var first = name.split(/\s|&/)[0] || name;
      var attending = valueOf("attending") === "yes";
      var title = success.querySelector("[data-success-title]");
      var lead = success.querySelector("[data-success-lead]");
      var dl = success.querySelector("[data-success-summary]");
      var ics = success.querySelector("[data-ics-link]");

      title.textContent = attending ? "Thank you, " + first : "We will miss you, " + first;
      lead.textContent = attending
        ? "Your reply card is filled in. Save the date to your calendar, and we will write again in June with the final details."
        : "Thank you for letting us know. We will be thinking of you on the nineteenth and will share photographs afterwards.";

      dl.innerHTML = "";
      addRow(dl, "Reply", attending ? "Joyfully accepts" : "Regretfully declines");
      addRow(dl, "Email", valueOf("email"));
      if (attending) {
        addRow(dl, "Party", valueOf("plus_one") === "yes" ? name + " and " + valueOf("plus_one_name") : name);
        addRow(dl, "To begin", valueOf("starter"));
        addRow(dl, "Main course", valueOf("main"));
        addRow(dl, "To finish", valueOf("dessert"));
        addRow(dl, "Guest\u2019s main", valueOf("plus_one_main"));
        addRow(dl, "Dietary needs", valueOf("dietary"));
        var shuttle = form.elements.shuttle;
        if (shuttle && shuttle.checked && !shuttle.disabled) addRow(dl, "Shuttle", "Seats saved from Kingsbridge");
      }
      addRow(dl, "Your note", valueOf("message"));

      if (ics) {
        ics.hidden = !attending;
        ics.classList.toggle("d-none", !attending);
        if (attending) {
          ics.href = buildIcsUrl();
          ics.setAttribute("download", EVENT.file);
        }
      }

      form.hidden = true;
      success.hidden = false;
      if (card) card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      success.focus({ preventScroll: true });
    }

    form.addEventListener("change", function () {
      applyConditions();
      if (attempted) showSummary(validate());
    });
    form.addEventListener("input", function (e) {
      if (!attempted || e.target.tagName === "TEXTAREA") return;
      showSummary(validate());
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      attempted = true;
      applyConditions();
      var errors = validate();
      showSummary(errors);
      if (errors.length) {
        if (summary) {
          summary.focus();
        } else {
          focusTarget(errors[0]);
        }
        return;
      }
      showSuccess();
    });

    var again = success && success.querySelector("[data-reply-again]");
    if (again) {
      again.addEventListener("click", function () {
        success.hidden = true;
        form.hidden = false;
        var nameField = document.getElementById("guestName");
        if (nameField) nameField.focus();
      });
    }

    applyConditions();
  }

  /* ---------------------------------------------------------------- */
  function init() {
    initIntro();
    initNav();
    initStickyHeader();
    initScrollSpy();
    initReveal();
    initCountdown();
    initCalendar();
    initCopy();
    initTabs();
    initCharCount();
    initRsvpForm();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
