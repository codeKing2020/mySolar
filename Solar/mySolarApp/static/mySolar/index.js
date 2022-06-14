document.addEventListener("DOMContentLoaded", () => {
    if (document.title == 'Welcome to MySolar | Home') {
        document.querySelector("nav").classList.remove("bg-white");
    }
    document.querySelector("#id_delivery_date").setAttribute("type", "datetime-local")
});