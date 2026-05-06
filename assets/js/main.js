// AimWolf — main.js
// На prelaunch JS почти не нужен. Только мелкие улучшения UX.

(function () {
  "use strict";

  // Плавная прокрутка по якорным ссылкам (#top, #games, #about, #status и т.п.)
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (event) {
      var hash = link.getAttribute("href");
      if (hash === "#" || hash.length < 2) return;
      var target = document.querySelector(hash);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  // Переключатель анимаций (сохраняется в localStorage)
  var MOTION_KEY = "aw-motion";
  var btn = document.getElementById("motion-toggle");
  function applyMotion(off) {
    document.body.classList.toggle("no-motion", off);
    if (btn) {
      btn.setAttribute("aria-pressed", off ? "true" : "false");
      btn.textContent = off ? "Анимации: выкл" : "Анимации: вкл";
    }
  }
  if (btn) {
    var saved = false;
    try { saved = localStorage.getItem(MOTION_KEY) === "off"; } catch (e) {}
    applyMotion(saved);
    btn.addEventListener("click", function () {
      var willBeOff = !document.body.classList.contains("no-motion");
      try { localStorage.setItem(MOTION_KEY, willBeOff ? "off" : "on"); } catch (e) {}
      applyMotion(willBeOff);
    });
  }
})();
