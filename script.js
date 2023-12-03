const dropdownbtn = document.querySelector(".dropdown_button")
const dropdownmenu = document.querySelector(".dropdown_menu")


dropdownbtn.addEventListener("click", () => {
    dropdownmenu.classList.toggle("hide")
});

window.addEventListener("click", (e) => {
    if (e.target !== dropdownbtn) {
        dropdownmenu.classList.add("hide")
    }
});