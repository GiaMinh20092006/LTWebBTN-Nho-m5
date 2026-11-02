/* ==========================================================================
   VAPOR GAME STORE — radio.js  (VAPOR-RADIO)
   Music player góc màn hình, TỰ TỔNG HỢP ÂM THANH bằng WebAudio API —
   không cần file nhạc, hoạt động offline, 4 đài synthwave:
     0. NEON DREAMS FM   — pad slow, hợp âm Am F C G
     1. MIDNIGHT DRIVE FM — bpm nhanh hơn, arpeggio square
     2. CRYSTAL CHAPEL FM — dreamy triangle pad
     3. SAMURAI 88 FM     — dark pentatonic arp
   Người dùng phải bấm Play (theo đúng chính sách autoplay của trình duyệt).
   ========================================================================== */

(function () {
    "use strict";

    /* ---------- Preset các đài radio ---------- */

    function midi(note) { return 440 * Math.pow(2, (note - 69) / 12); }

    var STATIONS = [
        {
            name: "NEON DREAMS FM",
            bpm: 82, wave: "sawtooth", cutoff: 850, echo: 0.42, echoTime: 0.46,
            chords: [
                [57, 60, 64], // Am
                [53, 57, 60], // F
                [60, 64, 67], // C
                [55, 59, 62]  // G
            ]
        },
        {
            name: "MIDNIGHT DRIVE FM",
            bpm: 104, wave: "square", cutoff: 1300, echo: 0.3, echoTime: 0.29,
            chords: [
                [54, 57, 61], // F#m
                [50, 54, 57], // D
                [57, 61, 64], // Am
                [52, 56, 59]  // E
            ]
        },
        {
            name: "CRYSTAL CHAPEL FM",
            bpm: 66, wave: "triangle", cutoff: 1100, echo: 0.55, echoTime: 0.62,
            chords: [
                [48, 55, 60], // Cmaj7-ish
                [53, 57, 62], // Fmaj7-ish
                [55, 59, 64], // Gmaj7-ish
                [45, 52, 57]  // Am
            ]
        },
        {
            name: "SAMURAI 88 FM",
            bpm: 118, wave: "square", cutoff: 1750, echo: 0.25, echoTime: 0.23,
            chords: [
                [57, 60, 64],
                [64, 67, 71],
                [55, 59, 62],
                [62, 65, 69]
            ]
        }
    ];

    /* ---------- Trạng thái ---------- */

    var ctx = null, master = null, filter = null, delay = null, feedback = null;
    var schedulerId = null, step = 0, chordIndex = 0, startedAt = 0;
    var playing = false, stationIndex = 0;

    var elRadio, elPlay, elStation, elVolume, elName, elTrack, elTime, elMin;

    function station() { return STATIONS[stationIndex]; }

    function beatSeconds() { return 60 / station().bpm; }

    /* ---------- Audio graph (tạo 1 lần) ---------- */

    function ensureAudio() {
        if (ctx) return true;
        var AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) return false;

        ctx = new AC();
        master = ctx.createGain();
        master.gain.value = (parseInt(elVolume.value, 10) || 0) / 100 * 0.32;

        filter = ctx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.value = station().cutoff;
        filter.Q.value = 0.8;

        delay = ctx.createDelay(1.5);
        feedback = ctx.createGain();
        var wet = ctx.createGain();
        wet.gain.value = station().echo;

        filter.connect(master);
        filter.connect(delay);
        delay.connect(feedback);
        feedback.connect(delay);
        delay.connect(wet);
        wet.connect(master);
        master.connect(ctx.destination);
        return true;
    }

    /* ---------- 1 nhịp = 1 bước (8 bước = 1 ô hợp âm 4 phách) ---------- */

    function tone(freq, when, dur, wave, vol, glideTo) {
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = wave || station().wave;
        osc.frequency.setValueAtTime(freq, when);
        if (glideTo) osc.frequency.exponentialRampToValueAtTime(glideTo, when + dur);

        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.exponentialRampToValueAtTime(vol, when + Math.min(0.09, dur * 0.3));
        gain.gain.exponentialRampToValueAtTime(0.0001, when + dur);

        osc.connect(gain);
        gain.connect(filter);
        osc.start(when);
        osc.stop(when + dur + 0.05);
    }

    function scheduleStep(when) {
        var st = station();
        var barSec = beatSeconds() * 2;

        if (step % 8 === 0) {
            chordIndex = (chordIndex + 1) % st.chords.length;
            var chord = st.chords[chordIndex];

            // PAD: 3 dao động hợp âm, ngân dài cả ô
            chord.forEach(function (note) {
                tone(midi(note), when, barSec * 0.98, st.wave, 0.16);
                tone(midi(note + 12), when, barSec * 0.98, "sine", 0.07);
            });

            // BASS: nốt trầm nhất của hợp âm -12
            tone(midi(chord[0] - 12), when, barSec * 0.5, "triangle", 0.3);
            tone(midi(chord[0] - 12), when + barSec * 0.5, barSec * 0.45, "triangle", 0.22);
        }

        // ARP: melody bán nhịp, đi lên các nốt hợp âm + octava
        var chord = st.chords[chordIndex];
        var arpNotes = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[1] + 24];
        var n = arpNotes[step % arpNotes.length];
        tone(midi(n), when, beatSeconds() * 0.42, step % 2 ? "triangle" : st.wave, 0.085);
    }

    /* ---------- Scheduler ---------- */

    function startLoop() {
        var stepDur = beatSeconds() / 2 * 1000;
        var nextTime = ctx.currentTime + 0.06;

        schedulerId = setInterval(function () {
            if (nextTime < ctx.currentTime) nextTime = ctx.currentTime + 0.02;
            scheduleStep(nextTime);
            nextTime += stepDur / 1000;
            step = (step + 1) % 8;
            tickClock();
        }, stepDur);
    }

    function stopLoop() {
        if (schedulerId) { clearInterval(schedulerId); schedulerId = null; }
        step = 0;
    }

    /* ---------- UI ---------- */

    function fmt(sec) {
        var m = Math.floor(sec / 60), s = Math.floor(sec % 60);
        return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }

    function tickClock() {
        if (elTime && playing) {
            elTime.textContent = fmt((Date.now() - startedAt) / 1000);
        }
    }

    function setStationLabel() {
        var st = station();
        elName.textContent = st.name;
        elTrack.textContent = st.bpm + " BPM · " + st.wave.toUpperCase() + " · echo " + st.echoTime.toFixed(2) + "s";
    }

    function play() {
        if (!ensureAudio()) {
            elTrack.textContent = "browser has no WebAudio :(";
            return;
        }
        if (ctx.state === "suspended") ctx.resume();

        filter.frequency.value = station().cutoff;
        delay.delayTime.value = station().echoTime;

        playing = true;
        startedAt = Date.now();
        elRadio.classList.add("playing");
        elPlay.textContent = "❚❚";
        elPlay.title = "Pause";
        setStationLabel();
        startLoop();
    }

    function pause() {
        playing = false;
        stopLoop();
        elRadio.classList.remove("playing");
        elPlay.textContent = "▶";
        elPlay.title = "Play";
        if (ctx) ctx.suspend();
    }

    document.addEventListener("DOMContentLoaded", function () {
        elRadio = document.getElementById("vapor-radio");
        elPlay = document.getElementById("radio-play");
        elStation = document.getElementById("radio-station");
        elVolume = document.getElementById("radio-volume");
        elName = document.getElementById("radio-station-name");
        elTrack = document.getElementById("radio-track-line");
        elTime = document.getElementById("radio-time");
        elMin = document.getElementById("radio-minimize");

        if (!elRadio || !elPlay) return;

        setStationLabel();
        elTime.textContent = "00:00";

        elPlay.addEventListener("click", function () {
            playing ? pause() : play();
        });

        elStation.addEventListener("change", function () {
            stationIndex = parseInt(elStation.value, 10) || 0;
            if (ctx) {
                filter.frequency.value = station().cutoff;
                delay.delayTime.value = station().echoTime;
            }
            var wasPlaying = playing;
            if (wasPlaying) { stopLoop(); startedAt = Date.now(); }
            setStationLabel();
            if (wasPlaying) startLoop();
        });

        elVolume.addEventListener("input", function () {
            if (master) master.gain.value = (parseInt(elVolume.value, 10) || 0) / 100 * 0.32;
        });

        elMin.addEventListener("click", function () {
            var mini = elRadio.classList.toggle("minimized");
            elMin.textContent = mini ? "+" : "−";
        });

        // Space (không focus vào input) = play/pause
        document.addEventListener("keydown", function (e) {
            var tag = (e.target.tagName || "").toLowerCase();
            if (e.code === "Space" && ["input", "textarea", "select"].indexOf(tag) === -1) {
                e.preventDefault();
                playing ? pause() : play();
            }
        });

        // Dọn dẹp khi rời trang
        window.addEventListener("beforeunload", function () {
            if (playing && ctx) ctx.close();
        });
    });
})();
