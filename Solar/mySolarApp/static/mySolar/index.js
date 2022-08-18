document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#id_delivery_date").setAttribute("type", "datetime-local")
    document.getElementById("requestsBTN").addEventListener("click", () => {
        document.getElementById("questions").style.display = "none";
        document.getElementById("requests").style.display = "block";
    })
    document.getElementById("questionsBTN").addEventListener("click", () => {
        document.getElementById("requests").style.display = "none";
        document.getElementById("questions").style.display = "block";
    })
});