// ================= SELECT + DELETE =================
document.addEventListener("DOMContentLoaded", function () {

    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".expense-checkbox");
    const deleteButton = document.getElementById("delete-button");

    function updateDeleteButton() {
        let checked = document.querySelectorAll(".expense-checkbox:checked").length;

        if (deleteButton) {
            deleteButton.disabled = checked === 0;
        }
    }

    if (selectAll) {
        selectAll.addEventListener("change", function () {
            checkboxes.forEach(function (checkbox) {
                checkbox.checked = selectAll.checked;

                if (checkbox.closest("tr")) {
                    if (selectAll.checked) {
                        checkbox.closest("tr").classList.add("selected-row");
                    } else {
                        checkbox.closest("tr").classList.remove("selected-row");
                    }
                }
            });

            updateDeleteButton();
        });
    }

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {

            if (checkbox.closest("tr")) {
                if (checkbox.checked) {
                    checkbox.closest("tr").classList.add("selected-row");
                } else {
                    checkbox.closest("tr").classList.remove("selected-row");
                }
            }

            updateDeleteButton();
        });
    });

    updateDeleteButton();
});


// ================= DELETE CONFIRM =================
function confirmDelete() {
    const checked = document.querySelectorAll(".expense-checkbox:checked").length;

    if (checked === 0) {
        alert("Please select at least one expense.");
        return false;
    }

    return confirm("Are you sure you want to delete selected expenses?");
}


// ================= EDIT MODAL =================
function openEditModal(id, amount, category, date, description) {

    const modal = document.getElementById("editModal");

    if (modal) {
        modal.hidden = false;   
    }

    document.getElementById("edit_id").value = id;
    document.getElementById("edit_amount").value = amount;
    document.getElementById("edit_category").value = category;
    document.getElementById("edit_date").value = date;
    document.getElementById("edit_description").value = description;

    document.getElementById("editForm").action = "/update-expense";
}

function closeModal() {
    const modal = document.getElementById("editModal");

    if (modal) {
        modal.hidden = true;   
    }
}


// ================= SORT MODAL =================
function openSortModal() {
    const modal = document.getElementById("sortModal");

    if (modal) {
        modal.hidden = false;   
    }
}

function closeSortModal() {
    const modal = document.getElementById("sortModal");

    if (modal) {
        modal.hidden = true;   
    }
}


// ================= SEARCH MODAL =================
function openSearchModal() {
    const modal = document.getElementById("searchModal");

    if (modal) {
        modal.hidden = false;   
    }
}

function closeSearchModal() {
    const modal = document.getElementById("searchModal");

    if (modal) {
        modal.hidden = true;  
    }
}


// ================= CLICK OUTSIDE CLOSE =================
window.onclick = function(event) {

    const modals = ["editModal", "sortModal", "searchModal"];

    modals.forEach(id => {
        const modal = document.getElementById(id);

        if (modal && event.target === modal) {
            modal.hidden = true;   // ✅ changed
        }
    });
};
document.addEventListener("DOMContentLoaded", () => {

    /* MOBILE MENU */
    const toggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("nav-menu");

    if (toggle && menu) {
        toggle.addEventListener("click", () => {
            menu.classList.toggle("show");
        });
    }

    /* HEADER SCROLL EFFECT */
    const header = document.getElementById("header");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 40) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });

    /* POINTER CURSOR FIX */
    document.querySelectorAll("a, button").forEach(el => {
        el.style.cursor = "pointer";
    });
    
    window.addEventListener("scroll", () => {
    const header = document.querySelector("header");

    if (window.scrollY > 50) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});

});

