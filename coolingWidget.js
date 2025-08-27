// ==UserScript==
// @name         Cooling Status Widget
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  Cooling status indicator widget
// @match        *://*/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';

    // Create widget
    let widget = document.createElement("div");
    widget.id = "cooling-widget";
    widget.innerHTML = "Connecting...";
    document.body.appendChild(widget);

    const style = document.createElement("style");
    style.textContent = `
      #cooling-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: gray;
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        z-index: 999999;
      }
    `;
    document.head.appendChild(style);

    // Open WebSocket directly
    try {
        const ws = new WebSocket("ws://localhost:8765");

        ws.onopen = () => {
            widget.innerHTML = "Connected";
        };

        ws.onmessage = (msg) => {
            let [temp, action] = msg.data.split(",");
            if (parseInt(action) === 1) {
                widget.style.background = "red";
                widget.innerHTML = `Cooling ON (${temp}°C)`;
            } else {
                widget.style.background = "green";
                widget.innerHTML = `Normal (${temp}°C)`;
            }
        };

        ws.onerror = () => {
            widget.innerHTML = "Error";
            widget.style.background = "orange";
        };

        ws.onclose = () => {
            widget.innerHTML = "Closed";
            widget.style.background = "gray";
        };

    } catch (e) {
        widget.innerHTML = "Init error";
        console.error(e);
    }
})();
