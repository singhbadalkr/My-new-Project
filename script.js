document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("scan-url").addEventListener("click", function () {
        const url = document.getElementById("url").value.trim();
        fetch("/scan/url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        })
        .then(res => {
            if (!res.ok) return res.text().then(t => { throw new Error(t); });
            return res.json();
        })
        .then(data => {
            document.getElementById("url-result").innerText = "Result: " + (data.status || data.error);
        })
        .catch(err => {
            document.getElementById("url-result").innerText = "Error: " + err.message;
        });
    });

    document.getElementById("file-form").addEventListener("submit", function (e) {
        e.preventDefault();
        const fileInput = document.getElementById("file");
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        fetch("/scan/file", {
            method: "POST",
            body: formData,
        })
        .then(res => {
            if (!res.ok) return res.text().then(t => { throw new Error(t); });
            return res.json();
        })
        .then(data => {
            document.getElementById("file-result").innerText = "Result: " + (data.status || data.error);
        })
        .catch(err => {
            document.getElementById("file-result").innerText = "Error: " + err.message;
        });
    });

    document.getElementById("scan-login").addEventListener("click", function () {
        const html = document.getElementById("html-content").value;
        fetch("/scan/fake-login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ html: html }),
        })
        .then(res => {
            if (!res.ok) return res.text().then(t => { throw new Error(t); });
            return res.json();
        })
        .then(data => {
            document.getElementById("login-result").innerText = "Result: " + (data.status || data.error);
        })
        .catch(err => {
            document.getElementById("login-result").innerText = "Error: " + err.message;
        });
    });
});
