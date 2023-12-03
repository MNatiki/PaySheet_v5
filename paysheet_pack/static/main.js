const dropdownbtn = document.querySelector(".slide")
const dropdownmenu = document.querySelector(".sidebar")

// Initially hide the sidebar by adding the "hide" class
dropdownmenu.classList.toggle("hide");

dropdownbtn.addEventListener("click", () => {
    dropdownmenu.classList.toggle("hide")
});

dropdownbtn.addEventListener("click", (e) => {
    if (e.target !== dropdownbtn) {
        dropdownmenu.classList.add("hide")
    }
});