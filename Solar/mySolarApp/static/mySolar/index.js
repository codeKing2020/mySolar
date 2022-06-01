document.addEventListener("DOMContentLoaded", () => {
    alert("yo!")
    if (document.title == 'Welcome to MySolar | Home') {
        alert("removing color!")
        document.querySelector("nav").classList.remove("bg-white");
    }
});