// AimWolf — main.js
// На prelaunch JS почти не нужен. Здесь только мелкие улучшения UX.

(function () {
  "use strict";

  // Плавная прокрутка по якорным ссылкам (#top, #games и т.п.)
  // scroll-behavior: smooth в CSS работает не везде на мобильных — подстрахуемся.
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
})();
