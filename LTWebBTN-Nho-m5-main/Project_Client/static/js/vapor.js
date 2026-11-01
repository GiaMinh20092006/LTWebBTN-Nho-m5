/* ==========================================================================
   VAPOR GAME STORE — vapor.js
   1. Nút toggle GLITCH/NEON MODE (lưu lựa chọn vào localStorage)
   2. Tự ẩn thông báo flash (alert success)
   3. Nút chọn nhanh số tiền nạp (quick-amounts) cho trang Ví
   4. Hiệu ứng "polychromatic" hover-shift cho tiêu đề glitch
   ========================================================================== */

(function () {
    "use strict";

    /* ---------- 1. GLITCH / NEON MODE TOGGLE ---------- */

    var STORAGE_KEY = "vapor.neonMode";

    function applyNeonMode(on) {
        document.body.classList.toggle("neon-mode", on);
        var label = document.querySelector("#glitch-toggle .toggle-label");
        if (label) label.textContent = on ? "NEON ON" : "GLITCH";
        document.documentElement.style.setProperty("--grid-speed", on ? "1.15s" : "2.8s");
    }

    function initGlitchToggle() {
        var button = document.getElementById("glitch-toggle");
        if (!button) return;

        var stored = null;
        try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) { /* private mode */ }

        // Mặc định bật neon — trang web "chất" hơn ngay lần mở đầu
        applyNeonMode(stored === null ? true : stored === "1");

        button.addEventListener("click", function () {
            var on = !document.body.classList.contains("neon-mode");
            applyNeonMode(on);
            try { localStorage.setItem(STORAGE_KEY, on ? "1" : "0"); } catch (e) { /* noop */ }

            // giật nhẹ màn hình khi chuyển chế độ (glitch transition)
            document.body.classList.add("mode-switching");
            setTimeout(function () {
                document.body.classList.remove("mode-switching");
            }, 420);
        });
    }

    /* ---------- 2. AUTO-DISMIS Flash ALERTS ---------- */

    function initAlertDismiss() {
        var alerts = document.querySelectorAll(".alert.auto-dismiss");

        alerts.forEach(function (alert) {
            setTimeout(function () {
                alert.style.transition = "opacity .35s, transform .35s";
                alert.style.opacity = "0";
                alert.style.transform = "translateY(-8px)";
                setTimeout(function () {
                    alert.remove();
                    var box = document.querySelector(".alerts");
                    if (box && !box.querySelector(".alert")) box.remove();
                }, 380);
            }, 3200);
        });
    }

    /* ---------- 3. WALLET QUICK AMOUNT CHIPS ---------- */

    function initWalletPresets() {
        var amountInput = document.getElementById("amount");
        if (!amountInput) return;

        document.querySelectorAll(".chip-preset").forEach(function (chip) {
            chip.addEventListener("click", function () {
                amountInput.value = chip.getAttribute("data-amount");
                amountInput.focus();
            });
        });
    }

    /* ---------- 4. CHROMATIC SPLIT ON GLITCH TITLES ---------- */

    function initGlitchTitleFlicker() {
        // Thỉnh thoảng "lỗi tín hiệu" ngẫu nhiên cho các glitch-text lớn
        var titles = document.querySelectorAll(".glitch-text");
        if (!titles.length) return;

        setInterval(function () {
            if (!document.body.classList.contains("neon-mode")) return;
            var pick = titles[Math.floor(Math.random() * titles.length)];
            pick.style.filter = "blur(1.5px) hue-rotate(" + (Math.random() * 60 - 30) + "deg)";
            setTimeout(function () { pick.style.filter = ""; }, 130);
        }, 1800);
    }

    /* ---------- boot ---------- */

    document.addEventListener("DOMContentLoaded", function () {
        initGlitchToggle();
        initAlertDismiss();
        initWalletPresets();
        initGlitchTitleFlicker();
    });
})();
