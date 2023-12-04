const dropdownbtn = document.querySelector(".slide")
const dropdownmenu = document.querySelector(".sidebar")
const contentSection = document.querySelector(".main");

// Initially hide the sidebar by adding the "hide" class
dropdownmenu.classList.toggle("hide");

dropdownbtn.addEventListener("click", () => {
    dropdownmenu.classList.toggle("hide")
    // Adjust the width of the content section based on the sidebar visibility
    contentSection.classList.toggle("expanded");
});

dropdownbtn.addEventListener("click", (e) => {
    if (e.target !== dropdownbtn) {
        dropdownmenu.classList.add("hide")
    }
});