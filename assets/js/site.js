/* Banda Bookkeepers — site script (hand-edited; not generated) */
(function () {
  var t = document.querySelector(".menu-toggle"), l = document.querySelector(".nav-links");
  if (t && l) t.addEventListener("click", function () {
    var o = l.classList.toggle("open"); t.setAttribute("aria-expanded", o ? "true" : "false");
  });
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();

  var f = document.getElementById("enquiry");
  if (!f) return;
  var q = new URLSearchParams(location.search).get("package");
  if (q) { var s = f.querySelector("[name=package]"); if (s) for (var i = 0; i < s.options.length; i++) if (s.options[i].value === q) s.selectedIndex = i; }
  f.querySelector("[name=ts]").value = Date.now();
  var err = document.getElementById("enquiry-err"), btn = f.querySelector("button[type=submit]");

  f.addEventListener("submit", function (e) {
    e.preventDefault();
    err.hidden = true;
    if (!f.checkValidity()) { f.reportValidity(); return; }
    btn.disabled = true; var old = btn.textContent; btn.textContent = "Sending…";
    fetch(f.action, { method: "POST", body: new FormData(f), headers: { "Accept": "application/json" } })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (d) {
        if (d && d.ok) { location.href = "/thank-you/"; return; }
        err.textContent = (d && d.error) || "Your enquiry could not be sent. Please WhatsApp 066 210 5631 or email accounts@thinkmybiz.co.za.";
        err.hidden = false; btn.disabled = false; btn.textContent = old;
      })
      .catch(function () {
        err.textContent = "Your enquiry could not be sent. Please WhatsApp 066 210 5631 or email accounts@thinkmybiz.co.za.";
        err.hidden = false; btn.disabled = false; btn.textContent = old;
      });
  });
})();
