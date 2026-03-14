// popup.js

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function parseMappingMaybe(value) {
    // Supports both object storage and old stringified JSON storage.
    if (value && typeof value === "object" && !Array.isArray(value)) return value;

    if (typeof value === "string") {
        try {
            const parsed = JSON.parse(value);
            return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
        } catch {
            return {};
        }
    }

    return {};
}

function renderEmpty(logEl) {
    logEl.innerHTML = `
        <div class="empty">
            <strong>No mapping yet.</strong>
            <p>Run sanitization in a page textarea first.</p>
        </div>
    `;
}

function renderMapping(logEl, mapping, updatedAt) {
    const entries = Object.entries(mapping).sort((a, b) => a[0].localeCompare(b[0]));

    if (!entries.length) {
        renderEmpty(logEl);
        return;
    }

    const rows = entries
        .map(([original, anonymized]) => {
            return `
                <div class="row">
                    <code class="left">${escapeHtml(original)}</code>
                    <span class="arrow">-></span>
                    <code class="right">${escapeHtml(anonymized)}</code>
                </div>
            `;
        })
        .join("");

    const updated = updatedAt
        ? `<div class="timestamp">Updated: ${new Date(updatedAt).toLocaleString()}</div>`
        : "";

    logEl.innerHTML = `
        <div class="mapping-list">${rows}</div>
        ${updated}
    `;
}

function loadAndRender() {
    const logEl = document.getElementById("log");
    if (!logEl) return;

    chrome.storage.local.get(
        ["sanitizer_mapping", "sanitizer_updated_at"],
        (result) => {
            if (chrome.runtime.lastError) {
                logEl.textContent = `Storage error: ${chrome.runtime.lastError.message}`;
                return;
            }

            const mapping = parseMappingMaybe(result.sanitizer_mapping);
            renderMapping(logEl, mapping, result.sanitizer_updated_at);
        }
    );
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("showMapping");
    if (btn) btn.addEventListener("click", loadAndRender);

    // Render immediately on popup open.
    loadAndRender();
});