/*
general.js

This file handles the interactive behaviour for the MySpend application.
It supports expense selection, delete confirmation, modal actions, form validation,
general UI behaviour, password toggles, registration redirect, and charts.
The same file is used on multiple pages, so each section checks whether the
required HTML elements exist before running.
*/


/* SELECTING EXPENSES AND BULK DELETE */

// WAIT FOR PAGE TO LOAD
// This code runs only after the HTML page has finished loading.
// That makes sure the table checkboxes and delete button already exist
// before JavaScript tries to use them.
document.addEventListener("DOMContentLoaded", function () {

    // GET IMPORTANT ELEMENTS
    // Get the select-all checkbox from the table header.
    const selectAll = document.getElementById("select-all");

    // Get all expense checkboxes from the table body.
    const checkboxes = document.querySelectorAll(".expense-checkbox");

    // Get the bulk delete button.
    const deleteButton = document.getElementById("delete-button");

    // UPDATE DELETE BUTTON
    // This function counts how many expense rows are selected.
    // It disables the button if no rows are selected.
    // It also updates the button text to show the selected count.
    function updateDeleteButton() {
        let checked = document.querySelectorAll(".expense-checkbox:checked").length;

        if (deleteButton) {
            deleteButton.disabled = checked === 0;
            deleteButton.textContent = `Delete Selected (${checked})`;
        }
    }

    // HANDLE SELECT-ALL CHECKBOX
    // When the user clicks the select-all checkbox, every row checkbox
    // is updated to match its checked state.
    // The code also adds or removes the selected-row class so the table
    // row is visually highlighted.
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

    // HANDLE INDIVIDUAL CHECKBOXES
    // Each row checkbox also needs its own change event.
    // This keeps the row highlight and delete button state correct
    // when the user selects expenses one by one.
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

    // SET INITIAL BUTTON STATE
    // Run this once when the page first loads so the delete button
    // starts in the correct state immediately.
    updateDeleteButton();
});


/* DELETE CONFIRMATION */

// This function is called when the bulk delete form is submitted.
// It prevents submission if nothing is selected and asks the user
// to confirm before the selected expenses are deleted.
function confirmDelete() {
    const checked = document.querySelectorAll(".expense-checkbox:checked").length;

    // STOP EMPTY DELETE ACTION
    // If nothing is selected, stop the form submission
    // and show an alert to the user.
    if (checked === 0) {
        alert("Please select at least one expense.");
        return false;
    }

    // ASK USER FOR FINAL CONFIRMATION
    // Show the browser confirmation dialog before continuing.
    return confirm("Are you sure you want to delete selected expenses?");
}


/* EDIT MODAL */

// This function opens the edit expense modal.
// It also fills the form fields with the values of the expense the user selected.
function openEditModal(id, amount, category, date, description) {

    // GET MODAL ELEMENT
    // Get the edit modal from the page.
    const modal = document.getElementById("editModal");

    // SHOW MODAL
    // If the modal exists, make it visible.
    if (modal) {
        modal.hidden = false;
    }

    // FILL FORM FIELDS
    // Insert the selected expense values into the form
    // so the user can edit the existing data.
    document.getElementById("edit_id").value = id;
    document.getElementById("edit_amount").value = amount;
    document.getElementById("edit_category").value = category;
    document.getElementById("edit_date").value = date;
    document.getElementById("edit_description").value = description;

    // SET FORM ACTION
    // Make sure the form submits to the update route.
    document.getElementById("editForm").action = "/update-expense#expenses";
}

// This function closes the edit modal.
function closeModal() {
    const modal = document.getElementById("editModal");

    // HIDE MODAL
    // If the edit modal exists, hide it.
    if (modal) {
        modal.hidden = true;
    }
}


/* SORT MODAL */

// This function opens the sort modal.
function openSortModal() {
    const modal = document.getElementById("sortModal");

    // SHOW MODAL
    // If the sort modal exists, display it.
    if (modal) {
        modal.hidden = false;
    }
}

// This function closes the sort modal.
function closeSortModal() {
    const modal = document.getElementById("sortModal");

    // HIDE MODAL
    // If the sort modal exists, hide it.
    if (modal) {
        modal.hidden = true;
    }
}


/* SEARCH MODAL */

// This function opens the search modal.
function openSearchModal() {
    const modal = document.getElementById("searchModal");

    // SHOW MODAL
    // If the search modal exists, display it.
    if (modal) {
        modal.hidden = false;
    }
}

// This function closes the search modal.
function closeSearchModal() {
    const modal = document.getElementById("searchModal");

    // HIDE MODAL
    // If the search modal exists, hide it.
    if (modal) {
        modal.hidden = true;
    }
}


/* CLICK OUTSIDE TO CLOSE MODALS */

// This section closes a modal when the user clicks outside the modal card.
// It checks the edit, sort, and search modals.
window.onclick = function(event) {

    // STORE MODAL IDS
    // Keep a list of all modal ids that should close
    // when the user clicks on the modal background.
    const modals = ["editModal", "sortModal", "searchModal"];

    modals.forEach(function (id) {
        const modal = document.getElementById(id);

        // CLOSE MODAL IF BACKGROUND IS CLICKED
        // If the click target is the modal background itself,
        // hide that modal.
        if (modal && event.target === modal) {
            modal.hidden = true;
        }
    });
};


/* FORM FEEDBACK AND VALIDATION */

// This section validates the sort, search, and edit forms before they submit.
// It also shows validation messages inside the modal windows.
document.addEventListener("DOMContentLoaded", function () {
    const sortForm = document.getElementById("sortForm");
    const searchForm = document.getElementById("searchForm");
    const editForm = document.getElementById("editForm");

    const sortFeedback = document.getElementById("sort-feedback");
    const searchFeedback = document.getElementById("search-feedback");
    const editFeedback = document.getElementById("edit-feedback");

    // SHOW FEEDBACK MESSAGE
    // This helper function makes a feedback element visible,
    // applies the correct style class, and inserts the message text.
    function showFeedback(element, type, message) {
        if (!element) {
            return;
        }

        element.hidden = false;
        element.classList.remove("success", "error");
        element.classList.add(type);
        element.textContent = message;
    }

    // CLEAR FEEDBACK MESSAGE
    // This helper function hides the feedback element
    // and removes any old message and styling.
    function clearFeedback(element) {
        if (!element) {
            return;
        }

        element.hidden = true;
        element.classList.remove("success", "error");
        element.textContent = "";
    }

    /* VALIDATION RULES */
    
    // VALIDATE SORT FORM
    // This checks that the user has selected a sort option
    // before the sort form is submitted.
    if (sortForm) {
        sortForm.addEventListener("submit", function (event) {
            clearFeedback(sortFeedback);

            const selectedSort = sortForm.querySelector('input[name="sort"]:checked');
            const selectedCategory = document.getElementById("sort_category_id").value;

            const hasSortOption = selectedSort !== null;
            const hasCategory = selectedCategory && selectedCategory.value.trim() !== "";

            // REQUIRE SORT CHOICE
            // Stop form submission if no sort option is selected.
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

    // VALIDATE SEARCH FORM
    // This checks that at least one field is filled in
    // and that amount and date ranges are valid.
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

            // REQUIRE AT LEAST ONE SEARCH FIELD
            // Stop submission if every search field is empty.
            if (!hasValue) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Please fill at least one field before applying search.");
                return;
            }

            // VALIDATE MINIMUM AMOUNT
            // The minimum amount cannot be negative.
            if (minAmount.value !== "" && Number(minAmount.value) < 0) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Minimum amount must be a positive number.");
                return;
            }

            // VALIDATE MAXIMUM AMOUNT
            // The maximum amount cannot be negative.
            if (maxAmount.value !== "" && Number(maxAmount.value) < 0) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Maximum amount must be a positive number.");
                return;
            }

            // VALIDATE AMOUNT RANGE
            // The minimum amount cannot be greater than the maximum amount.
            if (
                minAmount.value !== "" &&
                maxAmount.value !== "" &&
                Number(minAmount.value) > Number(maxAmount.value)
            ) {
                event.preventDefault();
                showFeedback(searchFeedback, "error", "Minimum amount cannot be greater than maximum amount.");
                return;
            }

            // VALIDATE DATE RANGE
            // The start date cannot be later than the end date.
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

    // VALIDATE EDIT FORM
    // This checks the edit modal fields before the form submits.
    if (editForm) {
        editForm.addEventListener("submit", function (event) {
            clearFeedback(editFeedback);

            const editAmount = document.getElementById("edit_amount");
            const editDate = document.getElementById("edit_date");
            const editCategory = document.getElementById("edit_category");

            // REQUIRE AMOUNT
            // The amount field must not be empty.
            if (editAmount.value.trim() === "") {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Please enter an amount.");
                return;
            }

            // REQUIRE POSITIVE AMOUNT
            // The amount must be greater than zero.
            if (Number(editAmount.value) <= 0) {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Amount must be greater than zero.");
                return;
            }

            // REQUIRE DATE
            // The date field must not be empty.
            if (editDate.value.trim() === "") {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Please choose a date.");
                return;
            }

            // REQUIRE CATEGORY
            // The category field must not be empty.
            if (editCategory.value.trim() === "") {
                event.preventDefault();
                showFeedback(editFeedback, "error", "Please choose a category.");
                return;
            }
        });
    }
});


/* AUTO HIDE TEMPORARY MESSAGES */

// This section hides temporary messages after a short delay.
// It fades them out first, then removes them from view.
document.addEventListener("DOMContentLoaded", function () {
    const timedMessages = document.querySelectorAll(".form-messages li, .table-messages li");

    timedMessages.forEach(function (message) {

        // WAIT BEFORE FADING
        // Leave the message visible for 5 seconds first.
        setTimeout(function () {
            message.style.transition = "opacity 0.4s ease";
            message.style.opacity = "0";

            // REMOVE AFTER FADE
            // After the fade-out finishes, remove the message from layout.
            setTimeout(function () {
                message.style.display = "none";
            }, 400);
        }, 5000);
    });
});


/* GENERAL UI EFFECTS */

// This section handles small user interface effects used across the site.
// It controls the mobile menu, header scroll styling, and pointer cursor styling.
document.addEventListener("DOMContentLoaded", () => {

    // MOBILE MENU
    // Clicking the menu button toggles the show class on the nav menu.
    const toggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("nav-menu");

    if (toggle && menu) {
        toggle.addEventListener("click", () => {
            menu.classList.toggle("show");
        });
    }

    // HEADER SCROLL EFFECT
    // Add a visual class after the user scrolls down the page.
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

    // POINTER CURSOR FIX
    // Force links and buttons to use the pointer cursor.
    document.querySelectorAll("a, button").forEach(el => {
        el.style.cursor = "pointer";
    });

});


/* BUDGET SPLIT CHART */

// This section creates the doughnut chart used in the budget area.
// It reads the chart values from HTML data attributes and colours
// the used portion based on how much of the budget has been spent.
document.addEventListener("DOMContentLoaded", function () {
    const chartCard = document.querySelector(".budget-chart-card");
    const chartCanvas = document.getElementById("budgetSplitChart");

    // CHECK REQUIRED ELEMENTS
    // Stop immediately if the chart card, canvas, or Chart.js is missing.
    if (!chartCard || !chartCanvas || typeof Chart === "undefined") {
        return;
    }

    // READ DATA VALUES
    // Read the values stored in the HTML data attributes.
    const usedAmount = Number(chartCard.dataset.used || 0);
    const leftAmount = Number(chartCard.dataset.left || 0);
    const progressValue = Number(chartCard.dataset.progress || 0);

    // CHOOSE CHART COLOUR
    // Start with green by default, then switch to orange or red
    // when the budget usage reaches warning or danger levels.
    let usedColor = "#16a34a";

    if (progressValue >= 100) {
        usedColor = "#dc2626";
    } else if (progressValue >= 80) {
        usedColor = "#f59e0b";
    } else {
        usedColor = "#16a34a";
    }

    // CREATE CHART
    // Build the budget doughnut chart with used and remaining values.
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


/* PASSWORD TOGGLE */

// This reusable function adds a show or hide toggle to a password field.
// It is used on both the login page and the register page.
function setupPasswordToggle(buttonId, inputId) {
    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);

    // CHECK REQUIRED ELEMENTS
    // Stop if the current page does not contain the required elements.
    if (!button || !input) {
        return;
    }

    // TOGGLE PASSWORD VISIBILITY
    // Switch the input between password and text,
    // and update the button label to match.
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

// APPLY TO MAIN PASSWORD FIELD
setupPasswordToggle("toggle-password", "password");

// APPLY TO CONFIRM PASSWORD FIELD
setupPasswordToggle("toggle-confirm-password", "confirm_password");


/* REGISTER SUCCESS REDIRECT */

// This section handles the delayed redirect after successful registration.
// It reads the target URL from the success message element and redirects
// the user after a 5-second wait.
document.addEventListener("DOMContentLoaded", function () {
    const registerSuccessMessage = document.getElementById("register-success-message");

    // CHECK SUCCESS MESSAGE
    // Stop if the register success message is not present on the page.
    if (!registerSuccessMessage) {
        return;
    }

    // READ REDIRECT URL
    // Get the destination URL from the HTML data attribute.
    const redirectUrl = registerSuccessMessage.dataset.redirectUrl;

    // REDIRECT AFTER DELAY
    // Wait 5 seconds, then send the user to the login page.
    setTimeout(function () {
        window.location.href = redirectUrl;
    }, 5000);
});


/* DAILY OVERVIEW CHART */

// This section creates the daily spending line chart on the overview page.
// The labels and values are read from HTML data attributes.
document.addEventListener("DOMContentLoaded", function () {
    const dailyChartCanvas = document.getElementById("dailyChart");

    // CHECK REQUIRED ELEMENTS
    // Stop if the chart canvas does not exist.
    if (!dailyChartCanvas) {
        return;
    }

    // CHECK CHART.JS
    // Stop if the Chart.js library is not loaded.
    if (typeof Chart === "undefined") {
        return;
    }

    // READ CHART DATA
    // Read chart labels and values from the HTML data attributes.
    const labelsText = dailyChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = dailyChartCanvas.getAttribute("data-values") || "[]";

    // CONVERT JSON TEXT TO ARRAYS
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // DEBUG CHART DATA
    // These logs help check whether the correct data reaches the chart.
    console.log("Daily chart labels:", labels);
    console.log("Daily chart values:", values);

    // CREATE LINE CHART
    // Build the daily spending chart.
    new Chart(dailyChartCanvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Daily Spending",
                    data: values,
                    borderColor: "#10b981",
                    backgroundColor: "rgba(16, 185, 129, 0.10)",
                    fill: true,
                    tension: 0.3,
                    borderWidth: 4,
                    pointRadius: 5,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return "£" + Number(context.raw).toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Days"
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Amount (£)"
                    },
                    ticks: {
                        callback: function (value) {
                            return "£" + value;
                        }
                    }
                }
            }
        }
    });
});


/* WEEKLY OVERVIEW CHART */

// This section creates the weekly spending bar chart on the overview page.
document.addEventListener("DOMContentLoaded", function () {
    const weeklyChartCanvas = document.getElementById("weeklyChart");

    // CHECK REQUIRED ELEMENTS
    // Stop if the chart canvas does not exist.
    if (!weeklyChartCanvas) {
        return;
    }

    // CHECK CHART.JS
    // Stop if the Chart.js library is not loaded.
    if (typeof Chart === "undefined") {
        return;
    }

    // READ CHART DATA
    // Read chart labels and values from the HTML data attributes.
    const labelsText = weeklyChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = weeklyChartCanvas.getAttribute("data-values") || "[]";

    // CONVERT JSON TEXT TO ARRAYS
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // DEBUG CHART DATA
    console.log("Weekly chart labels:", labels);
    console.log("Weekly chart values:", values);

    // CREATE BAR CHART
    // Build the weekly spending chart.
    new Chart(weeklyChartCanvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Weekly Spending",
                    data: values,
                    backgroundColor: "#8b5cf6",
                    borderColor: "#7c3aed",
                    borderWidth: 1,
                    borderRadius: 10
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return "£" + Number(context.raw).toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Weeks"
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Amount (£)"
                    },
                    ticks: {
                        callback: function (value) {
                            return "£" + value;
                        }
                    }
                }
            }
        }
    });
});


/* MONTHLY OVERVIEW CHART */

// This section creates the monthly spending line chart on the overview page.
document.addEventListener("DOMContentLoaded", function () {
    const monthlyChartCanvas = document.getElementById("monthlyChart");

    // CHECK REQUIRED ELEMENTS
    // Stop if the chart canvas does not exist.
    if (!monthlyChartCanvas) {
        return;
    }

    // CHECK CHART.JS
    // Stop if the Chart.js library is not loaded.
    if (typeof Chart === "undefined") {
        return;
    }

    // READ CHART DATA
    // Read chart labels and values from the HTML data attributes.
    const labelsText = monthlyChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = monthlyChartCanvas.getAttribute("data-values") || "[]";

    // CONVERT JSON TEXT TO ARRAYS
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // DEBUG CHART DATA
    console.log("Monthly chart labels:", labels);
    console.log("Monthly chart values:", values);

    // CREATE LINE CHART
    // Build the monthly spending chart.
    new Chart(monthlyChartCanvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Monthly Spending",
                    data: values,
                    borderColor: "#3b82f6",
                    backgroundColor: "rgba(59, 130, 246, 0.10)",
                    fill: true,
                    tension: 0.3,
                    borderWidth: 4,
                    pointRadius: 5,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return "£" + Number(context.raw).toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Months"
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Amount (£)"
                    },
                    ticks: {
                        callback: function (value) {
                            return "£" + value;
                        }
                    }
                }
            }
        }
    });
});


/* CATEGORY PIE CHART */

// This section creates the category spending pie chart on the overview page.
// It also includes a custom Chart.js plugin that draws percentage labels
// directly on each visible slice.
document.addEventListener("DOMContentLoaded", function () {
    const categoryPieChartCanvas = document.getElementById("categoryPieChart");

    // CHECK REQUIRED ELEMENTS
    // Stop if the chart canvas does not exist.
    if (!categoryPieChartCanvas) {
        return;
    }

    // CHECK CHART.JS
    // Stop if the Chart.js library is not loaded.
    if (typeof Chart === "undefined") {
        return;
    }

    // READ CHART DATA
    // Read chart labels and values from the HTML data attributes.
    const labelsText = categoryPieChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = categoryPieChartCanvas.getAttribute("data-values") || "[]";

    // CONVERT JSON TEXT TO ARRAYS
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // DEBUG CHART DATA
    console.log("Category chart labels:", labels);
    console.log("Category chart values:", values);

    // CALCULATE TOTAL
    // Add up all values so the code can calculate percentages for each slice.
    const total = values.reduce(function (sum, value) {
        return sum + Number(value);
    }, 0);

    // CREATE CUSTOM PERCENTAGE PLUGIN
    // This custom plugin runs after the pie chart is drawn.
    // It places percentage text inside each visible slice.
    const piePercentagePlugin = {
        id: "piePercentagePlugin",
        afterDatasetsDraw(chart) {
            const { ctx } = chart;
            const dataset = chart.data.datasets[0];
            const meta = chart.getDatasetMeta(0);

            ctx.save();
            ctx.font = "bold 12px Arial";
            ctx.fillStyle = "#070707";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            meta.data.forEach(function (slice, index) {
                const value = Number(dataset.data[index]);

                // IGNORE EMPTY SLICES
                // Skip empty slices and avoid division errors if total is zero.
                if (value <= 0 || total <= 0) {
                    return;
                }

                const percentage = ((value / total) * 100).toFixed(1) + "%";
                const position = slice.tooltipPosition();

                ctx.fillText(percentage, position.x, position.y);
            });

            ctx.restore();
        }
    };

    // CREATE PIE CHART
    // Build the category spending chart and apply the custom plugin.
    new Chart(categoryPieChartCanvas, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Category Spending",
                    data: values,
                    backgroundColor: [
                        "#8b5cf6",
                        "#3b82f6",
                        "#10b981",
                        "#f59e0b",
                        "#ef4444",
                        "#06b6d4",
                        "#ec4899",
                        "#84cc16",
                        "#6366f1",
                        "#f97316"
                    ],
                    borderColor: "#ffffff",
                    borderWidth: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = Number(context.raw);
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : "0.0";
                            return context.label + ": £" + value.toFixed(2) + " (" + percentage + "%)";
                        }
                    }
                }
            }
        },
        plugins: [piePercentagePlugin]
    });
});