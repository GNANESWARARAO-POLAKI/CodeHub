const textarea1 = document.getElementById("textarea1");
const codeBlock = document.getElementById("codeBlock");

function updateCode() {
    let content = textarea1.value;
    content = content.replace(/&/g, '&amp;');
    content = content.replace(/</g, '&lt;');
    content = content.replace(/>/g, '&gt;');
    codeBlock.innerHTML = content;
    highlightJS();
}

function highlightJS() {
    document.querySelectorAll('pre code').forEach((el) => {
        hljs.highlightElement(el);
    });
}

textarea1.addEventListener("input", () => {
    updateCode();
});


textarea1.addEventListener("scroll", () => {
    codeBlock.scrollTop = textarea1.scrollTop;
    codeBlock.scrollLeft = textarea1.scrollLeft;
});

document.getElementById("selectLanguage").addEventListener("change", function () {
    document.getElementById("codeBlock").className = this.value;
    highlightJS();
});


