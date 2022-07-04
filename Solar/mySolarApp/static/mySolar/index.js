document.addEventListener("DOMContentLoaded", () => {
    // document.querySelector("#id_delivery_date").setAttribute("type", "datetime-local")

    function showPage(pageName) {
        if (pageName == "main-text") {
            document.getElementById("main-text").style.display = "block";
            document.getElementById("login").style.display = "none";
            document.getElementById("register").style.display = "none";
        }
        if (pageName == "register") {
            document.getElementById("main-text").style.display = "none";
            document.getElementById("login").style.display = "none";
            document.getElementById("register").style.display = "block";
        }
        if (pageName == "login") {
            document.getElementById("main-text").style.display = "none";
            document.getElementById("login").style.display = "block";
            document.getElementById("register").style.display = "none";
        }
    };

    document.querySelectorAll('button').forEach(button => {

        // When a button is clicked, switch to that page
        button.onclick = function() {
            showPage(this.dataset.button);
        }
    })

    // Start off the index with main-text
    showPage("main-text");
});