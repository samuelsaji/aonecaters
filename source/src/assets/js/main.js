(function () {
  var PHONE = "919544541075";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header shadow on scroll
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 10); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Mobile menu
  var burger = document.querySelector(".burger");
  var scrim = document.querySelector(".scrim");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (burger) burger.setAttribute("aria-expanded", String(open));
  }
  if (burger) burger.addEventListener("click", function () { setNav(!document.body.classList.contains("nav-open")); });
  if (scrim) scrim.addEventListener("click", function () { setNav(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });

  // Photo fallback: if a stock photo can't load, show a branded panel instead
  document.querySelectorAll(".media img").forEach(function (img) {
    function fail() { img.parentElement.classList.add("failed"); }
    if (img.getAttribute("loading") !== "lazy" && img.complete && img.naturalWidth === 0) fail();
    img.addEventListener("error", fail);
    img.addEventListener("load", function () { img.parentElement.classList.remove("failed"); });
  });

  // Scroll reveal — only elements below the first screen start hidden
  var items = document.querySelectorAll("[data-reveal]");
  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    var vh = window.innerHeight;
    items.forEach(function (el, i) {
      if (el.getBoundingClientRect().top > vh) {
        el.classList.add("reveal");
        var d = el.getAttribute("data-reveal");
        if (d) el.style.transitionDelay = d + "ms";
        io.observe(el);
      }
    });
  }

  // Soft page transition between internal pages
  document.querySelectorAll("a[href$='.html']").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (reduce || e.metaKey || e.ctrlKey || e.shiftKey || a.target === "_blank") return;
      var href = a.getAttribute("href");
      e.preventDefault();
      document.body.classList.add("leaving");
      setTimeout(function () { window.location.href = href; }, 220);
    });
  });
  window.addEventListener("pageshow", function () { document.body.classList.remove("leaving"); });

  // Year
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Gallery filter + lightbox
  var gallery = document.querySelector(".masonry");
  if (gallery) {
    var figs = Array.prototype.slice.call(gallery.querySelectorAll("figure"));
    document.querySelectorAll(".filters button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".filters button").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        btn.setAttribute("aria-pressed", "true");
        var f = btn.getAttribute("data-filter");
        figs.forEach(function (fig) {
          var show = f === "all" || fig.getAttribute("data-cat") === f;
          fig.classList.toggle("hide", !show);
        });
      });
    });

    var lb = document.querySelector(".lightbox"), lbImg = lb.querySelector("img"), lbCap = lb.querySelector("p"), idx = 0;
    function visible() { return figs.filter(function (f) { return !f.classList.contains("hide"); }); }
    function show(i) {
      var v = visible(); if (!v.length) return;
      idx = (i + v.length) % v.length;
      var img = v[idx].querySelector("img");
      lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt;
      lbCap.textContent = v[idx].querySelector("b").textContent;
    }
    function open(fig) {
      show(visible().indexOf(fig)); lb.hidden = false;
      requestAnimationFrame(function () { lb.classList.add("open"); });
      lb.querySelector(".lb-close").focus();
    }
    function close() { lb.classList.remove("open"); setTimeout(function () { lb.hidden = true; }, 250); }
    figs.forEach(function (fig) {
      fig.tabIndex = 0;
      fig.addEventListener("click", function () { if (!fig.querySelector(".media.failed")) open(fig); });
      fig.addEventListener("keydown", function (e) { if (e.key === "Enter") open(fig); });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  // Enquiry form → prepared WhatsApp message (no server needed)
  var form = document.getElementById("enquiry");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      ["name", "phone", "event"].forEach(function (id) {
        var el = document.getElementById(id), err = el.parentElement.querySelector(".err");
        var bad = !el.value.trim() || (id === "phone" && el.value.replace(/\D/g, "").length < 10);
        err.textContent = bad ? (id === "phone" ? "Enter a 10-digit mobile number." : "This field is required.") : "";
        if (bad) ok = false;
      });
      if (!ok) return;
      var v = function (id) { return (document.getElementById(id).value || "").trim(); };
      var msg = "Hello A-one Caterers, I'd like a quote.%0A" +
        "Name: " + encodeURIComponent(v("name")) + "%0A" +
        "Phone: " + encodeURIComponent(v("phone")) + "%0A" +
        "Event: " + encodeURIComponent(v("event")) + "%0A" +
        "Date: " + encodeURIComponent(v("date") || "Not decided") + "%0A" +
        "Guests: " + encodeURIComponent(v("guests") || "-") + "%0A" +
        "Location: " + encodeURIComponent(v("venue") || "-") + "%0A" +
        "Notes: " + encodeURIComponent(v("message") || "-");
      var url = "https://wa.me/" + PHONE + "?text=" + msg;
      var done = document.getElementById("form-done");
      done.querySelector("a").href = url;
      done.hidden = false;
      done.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" });
    });
  }

  // Instagram reels: play muted while on screen, pause when scrolled away, tap to unmute
  var reels = Array.prototype.slice.call(document.querySelectorAll(".reel-video"));
  if (reels.length) {
    var userPaused = new WeakSet();
    function card(v) { return v.closest(".reel"); }
    function tryPlay(v) {
      var p = v.play();
      if (p && p.catch) p.catch(function () { card(v).classList.add("paused"); });
      card(v).classList.remove("paused");
    }
    function stop(v) { v.pause(); card(v).classList.add("paused"); }
    reels.forEach(function (v) {
      v.muted = true;
      card(v).classList.add("paused");
      var btn = card(v).querySelector(".reel-sound");
      var play = card(v).querySelector(".reel-play");
      btn.addEventListener("click", function () {
        var unmute = v.muted;
        reels.forEach(function (o) { o.muted = true; card(o).querySelector(".reel-sound").setAttribute("aria-pressed", "false"); card(o).querySelector(".reel-sound").setAttribute("aria-label", "Unmute"); });
        if (unmute) { v.muted = false; btn.setAttribute("aria-pressed", "true"); btn.setAttribute("aria-label", "Mute"); userPaused.delete(v); tryPlay(v); }
      });
      play.addEventListener("click", function () { userPaused.delete(v); tryPlay(v); });
      v.addEventListener("click", function () { if (v.paused) { userPaused.delete(v); tryPlay(v); } else { userPaused.add(v); stop(v); } });
    });
    if (!reduce && "IntersectionObserver" in window) {
      var rio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          var v = en.target;
          if (en.isIntersecting && en.intersectionRatio >= 0.5) { if (!userPaused.has(v)) tryPlay(v); }
          else if (!v.paused) { stop(v); }
        });
      }, { threshold: [0, 0.5] });
      reels.forEach(function (v) { rio.observe(v); });
    }
  }
})();
