// If a poster image fails to load (no internet / broken link), show our placeholder instead.
document.addEventListener("DOMContentLoaded", function () {
  var fallback = "/static/images/no-poster.svg";
  document.querySelectorAll("img.poster-img").forEach(function (img) {
    img.addEventListener("error", function () {
      if (img.getAttribute("src") !== fallback) {
        img.setAttribute("src", fallback);
      }
    });
  });
});
