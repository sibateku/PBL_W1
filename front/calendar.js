const header = document.getElementById("calendar-header");
const dates = document.getElementById("calendar-dates");
const prevButton = document.getElementById("prev-button");
const nextButton = document.getElementById("next-button");
const addButton = document.getElementById("add-button");
const modal = document.getElementById("schedule-modal");
const overlay = document.getElementById("overlay");
const saveButton = document.getElementById("save-button");
const cancelButton = document.getElementById("cancel-button");
const scheduleTitle = document.getElementById("schedule-title");
const scheduleDetails = document.getElementById("schedule-details");
const scheduleBudget = document.getElementById("schedule-budget");
const dateDisplay = document.getElementById("date-display");
const inputDate = document.getElementById("input-date");

const viewModal = document.getElementById("view-modal");
const viewDateDisplay = document.getElementById("view-date-display");
const viewTitle = document.getElementById("view-title");
const viewDetails = document.getElementById("view-details");
const viewBudget = document.getElementById("view-budget");
const closeViewButton = document.getElementById("close-view-button");
const deleteScheduleButton = document.getElementById("delete-schedule-button"); // 削除ボタン

let currentDate = new Date();
let selectedDate = null;
const scheduleData = {};

function renderCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();
    header.textContent = `${year}年${month + 1}月`;

    dates.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
        dates.appendChild(document.createElement("div"));
    }

    for (let i = 1; i <= lastDate; i++) {
        const dateDiv = document.createElement("div");
        dateDiv.textContent = i;
        dateDiv.classList.add("date");
        const fullDate = `${year}-${month + 1}-${i}`;
        dateDiv.dataset.date = fullDate;

        if (scheduleData[fullDate]) {
            dateDiv.classList.add("has-schedule");
        }

        dateDiv.addEventListener("click", () => openViewModal(fullDate));  // クリックで詳細表示
        dates.appendChild(dateDiv);
    }
}

function openModal(date) {
    selectedDate = date;
    dateDisplay.textContent = selectedDate || "選択してください";
    inputDate.value = selectedDate ? selectedDate : ""; // 日付を選択して表示
    modal.classList.add("active");
    overlay.classList.add("active");
}

function closeModal() {
    modal.classList.remove("active");
    overlay.classList.remove("active");
    scheduleTitle.value = "";
    scheduleDetails.value = "";
    scheduleBudget.value = "";
}

function openViewModal(date) {
    const schedule = scheduleData[date];
    if (schedule) {
        viewDateDisplay.textContent = date;
        viewTitle.textContent = schedule.title;
        viewDetails.textContent = schedule.details;
        viewBudget.textContent = `¥${schedule.budget.toLocaleString()}`;
        viewModal.classList.add("active");
        overlay.classList.add("active");
    }
}

function closeViewModal() {
    viewModal.classList.remove("active");
    overlay.classList.remove("active");
}

function deleteSchedule() {
    if (selectedDate && scheduleData[selectedDate]) {
        delete scheduleData[selectedDate];
        renderCalendar(currentDate); // 削除後にカレンダーを再描画
    }
    closeViewModal();
}

function saveSchedule() {
    if (selectedDate) {
        const title = scheduleTitle.value.trim();
        const details = scheduleDetails.value.trim();
        const budget = scheduleBudget.value.trim();

        if (title && budget !== "") {
            scheduleData[selectedDate] = {
                title,
                details,
                budget: parseFloat(budget),
            };

            renderCalendar(currentDate);
        }
    }
    closeModal();
}

saveButton.addEventListener("click", saveSchedule);
cancelButton.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);
closeViewButton.addEventListener("click", closeViewModal);
deleteScheduleButton.addEventListener("click", deleteSchedule); // 削除ボタンにイベントリスナーを追加

prevButton.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
});

nextButton.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
});

addButton.addEventListener("click", () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    selectedDate = `${year}-${month}-${new Date().getDate()}`;
    openModal(selectedDate);
});

renderCalendar(currentDate);
