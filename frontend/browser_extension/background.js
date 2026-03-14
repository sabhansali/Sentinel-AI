chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg?.type !== "SANITIZE_CODE") return;

    (async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/sanitize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: msg.code || "" })
            });

            if (!response.ok) {
                throw new Error(`Sanitizer API error (${response.status})`);
            }

            const data = await response.json();
            const mapping = data?.mapping ?? {};
            const sanitizedCode = data?.sanitized_code ?? "";

            await chrome.storage.local.set({
                sanitizer_mapping: mapping,
                sanitizer_sanitized_code: sanitizedCode,
                sanitizer_updated_at: Date.now()
            });

            sendResponse({ ok: true, data });
        } catch (err) {
            sendResponse({ ok: false, error: String(err) });
        }
    })();

    return true; // async response
});