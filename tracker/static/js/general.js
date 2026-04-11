// ================= SELECT + DELETE =================
document.addEventListener("DOMContentLoaded", function () {

    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".expense-checkbox");
    const deleteButton = document.getElementById("delete-button");

    function updateDeleteButton() {
        let checked = document.querySelectorAll(".expense-checkbox:checked").length;

        if (deleteButton) {
            deleteButton.disabled = checked === 0;
            deleteButton.textContent = `Delete Selected (${checked})`;
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

    document.getElementById("editForm").action = "/update-expense#expenses";
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

    modals.forEach(function (id) {
        const modal = document.getElementById(id);

        if (modal && event.target === modal) {
            modal.hidden = true;
        }
    });
};


// ================= FORM FEEDBACK + VALIDATION =================
document.addEventListener("DOMContentLoaded", function () {
    const sortForm = document.getElementById("sortForm");
    const searchForm = document.getElementById("searchForm");
    const editForm = document.getElementById("editForm");

    const sortFeedback = document.getElementById("sort-feedback");
    const searchFeedback = document.getElementById("search-feedback");
    const editFeedback = document.getElementById("edit-feedback");

    function showFeedback(element, type, message) {
        if (!element) {
            return;
        }

        element.hidden = false;
        element.classList.remove("success", "error");
        element.classList.add(type);
        element.textContent = message;
    }

    function clearFeedback(element) {
        if (!element) {
            return;
        }

        element.hidden = true;
        element.classList.remove("success", "error");
        element.textContent = "";
    }

    if (sortForm) {
        sortForm.addEventListener("submit", function (event) {
            clearFeedback(sortFeedback);

            const selectedSort = sortForm.querySelector('input[name="sort"]:checked');
            const selectedCategory = document.getElementById("sort_category_id").value;

            const hasSortOption = selectedSort !== null;
            const hasCategory = selectedCategory && selectedCategory.value.trim() !== "";

            if (!selectedSort) {
                event.preventDefault();
                showFeedback(
                    sortFeedback, 
                    "error",
                     "Please choose a sort option or select a category before applying."
                );

                return;
            }
        });
    }

    if (searchForm) {
        searchForm.addEventListener("submit", function (event) {
            clearFeedback(searchFeedback);

            const description = document.getElementById("search_description");
            const minAmount = document.getElementById("search_min_amount");
            const maxAmount = document.getElementById("search_max_amount");
            const dateFrom = document.getElementById("search_date_from");
            const dateTo = document.getElementById("search_date_to");

            const hasValue =
                description.value.trim() !== "" ||
                minAmount.value.trim() !== "" ||
                maxAmount.value.trim() !== "" ||
                dateFrom.value.trim() !== "" ||
                dateTo.value.trim() !== "";

            if (!hasValue) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Please fill at least one field before applying search.");
                return;
            }

            if (minAmount.value !== "" && Number(minAmount.value) < 0) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Minimum amount must be a positive number.");
                return;
            }

            if (maxAmount.value !== "" && Number(maxAmount.value) < 0) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Maximum amount must be a positive number.");
                return;
            }

            if (
                minAmount.value !== "" &&
                maxAmount.value !== "" &&
                Number(minAmount.value) > Number(maxAmount.value)
            ) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Minimum amount cannot be greater than maximum amount.");
                return;
            }

            if (
                dateFrom.value !== "" &&
                dateTo.value !== "" &&
                dateFrom.value > dateTo.value
            ) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Date From cannot be later than Date To.");
            }
        });
    }

    if (editForm) {
        editForm.addEventListener("submit", function (event) {
            clearFeedback(editFeedback);

            const editAmount = document.getElementById("edit_amount");
            const editDate = document.getElementById("edit_date");
            const editCategory = document.getElementById("edit_category");

            if (editAmount.value.trim() === "") {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Please enter an amount.");
                return;
            }

            if (Number(editAmount.value) <= 0) {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Amount must be greater than zero.");
                return;
            }

            if (editDate.value.trim() === "") {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Please choose a date.");
                return;
            }

            if (editCategory.value.trim() === "") {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Please choose a category.");
                return;
            }
        });
    }
});


// ================= SUCCESS MESSAGE AUTO HIDE =================
document.addEventListener("DOMContentLoaded", function () {
    const timedMessages = document.querySelectorAll(".form-messages li, .table-messages li");

    timedMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.transition = "opacity 0.4s ease";
            message.style.opacity = "0";

            setTimeout(function () {
                message.style.display = "none";
            }, 400);
        }, 5000);
    });
});


// ================= UI EFFECTS =================
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
    window.addEventListener("scroll", () => {
        const header = document.querySelector("header");

        if (header) {
            if (window.scrollY > 50) {
                header.classList.add("scrolled");
            } else {
                header.classList.remove("scrolled");
            }
        }
    });

    /* POINTER CURSOR FIX */
    document.querySelectorAll("a, button").forEach(el => {
        el.style.cursor = "pointer";
    });

});

// ================= BUDGET SPLIT CHART =================
// ================= BUDGET SPLIT CHART =================
document.addEventListener("DOMContentLoaded", function () {
    const chartCard = document.querySelector(".budget-chart-card");
    const chartCanvas = document.getElementById("budgetSplitChart");

    if (!chartCard || !chartCanvas || typeof Chart === "undefined") {
        return;
    }

    const usedAmount = Number(chartCard.dataset.used || 0);
    const leftAmount = Number(chartCard.dataset.left || 0);
    const progressValue = Number(chartCard.dataset.progress || 0);

    let usedColor = "#16a34a";

    if (progressValue >= 100) {
        usedColor = "#dc2626";
    } else if (progressValue >= 80) {
        usedColor = "#f59e0b";
    } else {
        usedColor = "#16a34a";
    }

    new Chart(chartCanvas, {
        type: "doughnut",
        data: {
            labels: ["Used", "Remaining"],
            datasets: [
                {
                    data: [usedAmount, leftAmount],
                    backgroundColor: [usedColor, "#d1d5db"],
                    borderColor: "#ffffff",
                    borderWidth: 4,
                    hoverOffset: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "74%",
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.label + ": £" + Number(context.raw).toFixed(2);
                        }
                    }
                }
            }
        }
    });
});

/* ================= PASSWORD TOGGLE in LOGIN  and REGISTER FORM ================== */


function setupPasswordToggle(buttonId, inputId) {
    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);

    if (!button || !input) {
        return;
    }

    button.addEventListener("click", function () {
        if (input.type === "password") {
            input.type = "text";
            button.textContent = "Hide";
        } else {
            input.type = "password";
            button.textContent = "Show";
        }
    });
}

setupPasswordToggle("toggle-password", "password");
setupPasswordToggle("toggle-confirm-password", "confirm_password");

/* ================= REGISTER SUCCESS REDIRECT ================== */

document.addEventListener("DOMContentLoaded", function () {
    const registerSuccessMessage = document.getElementById("register-success-message");

    if (!registerSuccessMessage) {
        return;
    }

    const redirectUrl = registerSuccessMessage.dataset.redirectUrl;

    setTimeout(function () {
        window.location.href = redirectUrl;
    }, 5000);
});