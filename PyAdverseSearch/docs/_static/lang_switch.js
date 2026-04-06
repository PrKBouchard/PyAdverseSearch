document.addEventListener("DOMContentLoaded", function () {
    function switchLanguage(targetLang) {
        var path = window.location.pathname;
        var search = window.location.search || "";
        var hash = window.location.hash || "";

        // Replace an existing /fr/ or /en/ segment wherever it appears in the path.
        if (/(^|\/)fr\//.test(path) || /(^|\/)en\//.test(path)) {
            path = path.replace(/(^|\/)fr\//, "$1" + targetLang + "/");
            path = path.replace(/(^|\/)en\//, "$1" + targetLang + "/");
        } else {
            // Fallback for direct pages without language segment.
            if (!path.endsWith("/")) {
                var lastSlash = path.lastIndexOf("/");
                path = path.slice(0, lastSlash + 1) + targetLang + "/" + path.slice(lastSlash + 1);
            } else {
                path = path + targetLang + "/";
            }
        }

        window.location.href = path + search + hash;
    }

    var langDiv = document.createElement("div");
    langDiv.style.padding = "10px";
    langDiv.style.marginBottom = "20px";
    langDiv.style.backgroundColor = "#f7f7f7";
    langDiv.style.textAlign = "center";
    langDiv.style.border = "1px solid #ccc";
    langDiv.style.borderRadius = "5px";
    langDiv.style.cssFloat = "right";
    langDiv.style.margin = "10px";

    var label = document.createElement("strong");
    label.textContent = "Lang: ";

    var enLink = document.createElement("a");
    enLink.href = "#";
    enLink.textContent = "EN";
    enLink.style.marginRight = "10px";
    enLink.addEventListener("click", function (event) {
        event.preventDefault();
        switchLanguage("en");
    });

    var separator = document.createTextNode(" | ");

    var frLink = document.createElement("a");
    frLink.href = "#";
    frLink.textContent = "FR";
    frLink.style.marginLeft = "10px";
    frLink.addEventListener("click", function (event) {
        event.preventDefault();
        switchLanguage("fr");
    });

    langDiv.appendChild(label);
    langDiv.appendChild(enLink);
    langDiv.appendChild(separator);
    langDiv.appendChild(frLink);

    var container = document.querySelector(".rst-content");
    if (container) {
        container.insertBefore(langDiv, container.firstChild);
    } else {
        var bodyDiv = document.querySelector("div.body");
        if (bodyDiv) {
            bodyDiv.insertBefore(langDiv, bodyDiv.firstChild);
        }
    }
});
