function extractPythonCode(text) {
    const codeBlocks = text.match(/```python([\s\S]*?)```/gi);
    if (codeBlocks?.length) {
        return codeBlocks
            .map((block) => block.replace(/```python|```/gi, "").trim())
            .filter(Boolean)
            .join("\n\n");
    }
    return text.trim();
}

function isEditableTarget(el) {
    if (!el) return false;
    if (el.tagName === "TEXTAREA") return true;
    return el.isContentEditable === true;
}

function getEditableText(el) {
    if (el.tagName === "TEXTAREA") return el.value || "";
    if (el.isContentEditable) return el.innerText || "";
    return "";
}

let debounceTimer = null;

document.addEventListener("input", (e) => {
    const target = e.target;
    if (!isEditableTarget(target)) return;

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const text = getEditableText(target);
        const codeOnly = extractPythonCode(text);
        if (!codeOnly) return;

        chrome.runtime.sendMessage({ type: "SANITIZE_CODE", code: codeOnly }, (res) => {
            if (chrome.runtime.lastError) {
                console.error("Runtime message error:", chrome.runtime.lastError.message);
                return;
            }
            if (!res?.ok) {
                console.error("Sanitizer failed:", res?.error);
            }
        });
    }, 600);
});