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

// ================= DAILY OVERVIEW CHART =================

document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element for the daily chart. If it doesn't exist, we simply return and do not attempt to render the chart. This allows us to safely include this JavaScript file on pages that do not have the daily chart without causing errors.
    const dailyChartCanvas = document.getElementById("dailyChart");

    // Check if the Chart.js library is loaded. If it's not available, we return early to avoid any errors when trying to create a new chart instance. This ensures that the rest of the page can function properly even if the chart cannot be rendered.
    if (!dailyChartCanvas) {
        return;
    }
    // Check if the Chart object is defined, which indicates that the Chart.js library is loaded. If it's not defined, we return early to prevent any errors when trying to create a new chart instance. This allows the page to work without the chart if the library is missing or fails to load.
    if (typeof Chart === "undefined") {
        return;
    }
    // read data from HTML data attributes on the canvas element. The labels and values are expected to be JSON strings, so we parse them into JavaScript arrays. These arrays will be used as the x-axis labels and y-axis data points for the daily spending chart, allowing us to visualize the user's spending trends over the past week.
    const labelsText = dailyChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = dailyChartCanvas.getAttribute("data-values") || "[]";

    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    console.log("Daily chart labels:", labels);
    console.log("Daily chart values:", values);

    // Create a new line chart using Chart.js to display daily spending. The chart is configured with various options for styling, responsiveness, and tooltips. The x-axis represents the days of the week, while the y-axis shows the amount spent in pounds. The chart also includes a legend and custom tooltip formatting to enhance the user experience when viewing their spending trends.
    new Chart(dailyChartCanvas, {
        //cerate line chart with the provided labels and values. The chart is styled with a green line and a light green fill area, and it includes smooth curves between data points for a more visually appealing look. The chart options also specify how the axes should be displayed and how tooltips should format the data when hovering over points on the chart.
        type: "line",
        data: {  //show simple legend with "Daily Spending" label and the data points from the values array. The line is styled with a green color and a light green fill, and the chart is configured to be responsive and maintain its aspect ratio across different screen sizes.
            labels: labels,
            datasets: [ // The dataset for the daily spending chart includes a label, the data points from the values array, and styling options such as border color, background color, fill, tension for smooth curves, border width, and point radius. This configuration creates a visually appealing line chart that represents the user's daily spending over the past week.
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
        options: { // The chart options specify that the chart should be responsive, maintain its aspect ratio, and include custom legend and tooltip configurations.
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
            scales: { // The scales configuration defines the appearance and behavior of the x and y axes. The x-axis is labeled "Days", while the y-axis starts at zero, is labeled "Amount (£)", and formats the tick values with a pound sign for better readability.
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
                    ticks: { // The ticks configuration for the y-axis includes a callback function that formats the tick values by adding a pound sign (£) in front of the value. This enhances the readability of the chart by clearly indicating that the values represent amounts in pounds.
                        callback: function (value) {
                            return "£" + value;
                        }
                    }
                }
            }
        }
    });
});

// ================= WEEKLY OVERVIEW CHART =================

document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element for the weekly chart. If it does not exist,
    // stop here safely so the script does not cause errors on other pages.
    const weeklyChartCanvas = document.getElementById("weeklyChart");

    // Check if the canvas exists on the page.
    // If it does not exist, return immediately.
    if (!weeklyChartCanvas) {
        return;
    }

    // Check if Chart.js is loaded.
    // If it is missing, stop here to avoid JavaScript errors.
    if (typeof Chart === "undefined") {
        return;
    }

    // Read the weekly labels and values from the HTML data attributes.
    // These values were prepared in the Flask route and passed into the template.
    const labelsText = weeklyChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = weeklyChartCanvas.getAttribute("data-values") || "[]";

    // Convert the JSON text into normal JavaScript arrays.
    // The labels array will be used on the x-axis and the values array
    // will be used to control the height of the bars.
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // Show the data in the browser console so it is easy to test
    // whether the weekly values are reaching JavaScript correctly.
    console.log("Weekly chart labels:", labels);
    console.log("Weekly chart values:", values);

    // Create a new bar chart using Chart.js.
    // This chart compares the user's total spending across the last 4 weeks.
    new Chart(weeklyChartCanvas, {
        // Use the bar chart type so each week is shown as a separate bar.
        type: "bar",
        data: {
            // Use the weekly labels on the x-axis.
            labels: labels,
            datasets: [
                // The dataset contains the weekly spending values and
                // the basic styling options for the bars.
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
            // Make the chart responsive so it adapts to different screen sizes.
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        // Format the tooltip values in pounds with two decimal places.
                        label: function (context) {
                            return "£" + Number(context.raw).toFixed(2);
                        }
                    }
                }
            },
            scales: {
                // Configure both axes for clarity.
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
                        // Add the pound sign to the y-axis values.
                        callback: function (value) {
                            return "£" + value;
                        }
                    }
                }
            }
        }
    });
});

// ================= MONTHLY OVERVIEW CHART =================

document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element for the monthly chart. If it does not exist,
    // stop here safely so the script does not cause errors on pages that
    // do not include the monthly chart.
    const monthlyChartCanvas = document.getElementById("monthlyChart");

    // Check if the canvas exists on the page.
    // If it does not exist, return immediately.
    if (!monthlyChartCanvas) {
        return;
    }

    // Check if Chart.js is loaded.
    // If it is missing, stop here to avoid JavaScript errors.
    if (typeof Chart === "undefined") {
        return;
    }

    // Read the monthly labels and values from the HTML data attributes.
    // These values were prepared in the Flask route and passed into the template.
    const labelsText = monthlyChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = monthlyChartCanvas.getAttribute("data-values") || "[]";

    // Convert the JSON text into normal JavaScript arrays.
    // The labels array will be used on the x-axis and the values array
    // will be used as the monthly spending totals on the y-axis.
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // Show the monthly data in the browser console so it is easy to test
    // whether the monthly values are reaching JavaScript correctly.
    console.log("Monthly chart labels:", labels);
    console.log("Monthly chart values:", values);

    // Create a new line chart using Chart.js.
    // This chart compares the user's spending totals across all 12 months
    // of the current year.
    new Chart(monthlyChartCanvas, {
        // Use the line chart type so the user can easily see the overall
        // trend rising or falling across the year.
        type: "line",
        data: {
            // Use the month names on the x-axis.
            labels: labels,
            datasets: [
                // The dataset contains the monthly spending totals and
                // the styling options for the line and points.
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
            // Make the chart responsive so it adapts well to different screen sizes.
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        // Format the tooltip values in pounds with two decimal places.
                        label: function (context) {
                            return "£" + Number(context.raw).toFixed(2);
                        }
                    }
                }
            },
            scales: {
                // Configure both axes for clarity.
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
                        // Add the pound sign to the y-axis values.
                        callback: function (value) {
                            return "£" + value;
                        }
                    }
                }
            }
        }
    });
});

// ================= CATEGORY PIE CHART =================

document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element for the category pie chart. If it does not exist,
    // stop here safely so the script does not cause errors on pages that do
    // not include the category chart.
    const categoryPieChartCanvas = document.getElementById("categoryPieChart");

    // Check if the canvas exists on the page.
    // If it does not exist, return immediately.
    if (!categoryPieChartCanvas) {
        return;
    }

    // Check if Chart.js is loaded.
    // If it is missing, stop here to avoid JavaScript errors.
    if (typeof Chart === "undefined") {
        return;
    }

    // Read the category labels and values from the HTML data attributes.
    // These values were prepared in the Flask route and passed into the template.
    const labelsText = categoryPieChartCanvas.getAttribute("data-labels") || "[]";
    const valuesText = categoryPieChartCanvas.getAttribute("data-values") || "[]";

    // Convert the JSON text into normal JavaScript arrays.
    // The labels array will contain category names, and the values array
    // will contain the total amount spent in each category.
    const labels = JSON.parse(labelsText);
    const values = JSON.parse(valuesText);

    // Show the category data in the browser console so it is easy to test
    // whether the pie chart values are reaching JavaScript correctly.
    console.log("Category chart labels:", labels);
    console.log("Category chart values:", values);

    // Calculate the full total of all category values.
    // This is needed so we can work out the percentage share of each slice.
    const total = values.reduce(function (sum, value) {
        return sum + Number(value);
    }, 0);

    // Create a custom plugin to draw the percentage text directly
    // on each visible slice of the pie chart.
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

                // Skip slices with zero values because they have no visible area.
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

    // Create a new pie chart using Chart.js.
    // Each slice of the pie will represent one category and its share
    // of the user's spending for the current month.
    new Chart(categoryPieChartCanvas, {
        // Use the pie chart type so the user can easily see how spending
        // is divided between categories.
        type: "pie",
        data: {
            // Use category names as the chart labels.
            labels: labels,
            datasets: [
                // The dataset contains the category totals and the colours
                // used for the pie slices.
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
            // Make the chart responsive so it adapts to different screen sizes.
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        // Show both the amount and percentage in the tooltip.
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