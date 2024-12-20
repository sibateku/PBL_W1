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

const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');

const templateButton = document.getElementById('template-button');
const templateEditing = document.getElementById('template-editing');

function graph() {
    if (id === null) {
        location.href = './graph.html';
    }
    else {
        location.href = './graph.html?id=' + id;
    }
}

function template() {
    const style = document.createElement('style');
    style.innerHTML = `
        .template-editing {
            display: flex;
        }
    `;
    document.head.appendChild(style);
}

function buttonCloseEditTemplate() {
    const style = document.createElement('style');
    style.innerHTML = `
        .template-editing {
            display: none;
        }
    `;
    // テンプレート編集画面の要素をクリアする
    editTemplateSelect.value = "";
    templateDetails.value = "";
    templateBudget.value = "";
    document.head.appendChild(style);
}


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
    inputDate.addEventListener("change", (e) => {
        selectedDate = e.target.value;
        dateDisplay.textContent = selectedDate;
    });
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
        try {
            srvDeleteSchedule(selectedDate); // データベースに削除リクエストを送信
        }
        catch (e) {
            console.log(e);
            alert('データベースから削除失敗');
        }
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

            try {
                srvSaveSchedule(title, details, budget, selectedDate); // データベースに保存リクエストを送信
            }
            catch (e) {
                console.log(e);
                alert('データベースに保存失敗');
            }
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
    try {
        srvGetSchedule(); // データベースからスケジュールを取得
    } catch (e) {
        console.log(e);
        alert('データベースからスケジュール取得失敗');
    }
    renderCalendar(currentDate);
});

nextButton.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    try {
        srvGetSchedule(); // データベースからスケジュールを取得
    } catch (e) {
        console.log(e);
        alert('データベースからスケジュール取得失敗');
    }
    renderCalendar(currentDate);
});

addButton.addEventListener("click", () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    selectedDate = `${year}-${month}-${new Date().getDate()}`;
    openModal(selectedDate);
});

if (location.protocol == "file:") {
    ////// ローカルで実行
    url = 'http://127.0.0.1:5000/';
} else {
    ////// サーバ上で実行
    url = 'https://pbl-w1.onrender.com/';
}
try {
    srvGetSchedule(); // データベースからスケジュールを取得
} catch (e) {
    console.log(e);
    alert('データベースからスケジュール取得失敗');
}
renderCalendar(currentDate);

const templateSelect = document.getElementById("template-select");
const editTemplateSelect = document.getElementById("edit-template-select");
const templateTitle = document.getElementById("edit-template-title");
const templateDetails = document.getElementById("edit-template-details");
const templateBudget = document.getElementById("edit-template-budget");
const saveTemplateButton = document.getElementById("save-template-button");

var templates = {
    work: {
        title: "仕事",
        details: "仕事の予定です",
        budget: "5000",
    },
    meeting: {
        title: "会議",
        details: "会議の予定です",
        budget: "1000",
    },
    personal: {
        title: "個人的な予定",
        details: "個人的な予定です",
        budget: "0",
    },
};

// テンプレート選択後にフォームを編集可能にする
templateSelect.addEventListener("change", (e) => {
    const selectedTemplate = e.target.value;

    if (selectedTemplate && templates[selectedTemplate]) {
        // テンプレートに基づいたデータを編集フォームに表示
        scheduleTitle.value = templates[selectedTemplate].title;
        scheduleDetails.value = templates[selectedTemplate].details;
        scheduleBudget.value = templates[selectedTemplate].budget;
    } else {
        // テンプレートを選択しなかった場合はフォームを空にする
        templateTitle.value = "";
        templateDetails.value = "";
        templateBudget.value = "";
    }
});

// テンプレート編集後に選択肢を更新
editTemplateSelect.addEventListener("change", (e) => {
    const selectedTemplate = e.target.value;

    if (selectedTemplate && templates[selectedTemplate]) {
        // テンプレートに基づいたデータを編集フォームに表示
        //templateTitle.value = selectedTemplate;
        templateDetails.value = templates[selectedTemplate].details;
        templateBudget.value = templates[selectedTemplate].budget;
    } else {
        // テンプレートを選択しなかった場合はフォームを空にする
        //templateTitle.value = "";
        templateDetails.value = "";
        templateBudget.value = "";
    }
});

// テンプレートを保存する処理
saveTemplateButton.addEventListener("click", () => {
    const selectedTemplate = editTemplateSelect.value;

    if (selectedTemplate) {
        // ユーザーが編集した内容でテンプレートを更新
        templates[selectedTemplate] = {
            // title: templateTitle.value.trim(),
            details: templateDetails.value.trim(),
            budget: templateBudget.value.trim(),
        };

        alert(`${selectedTemplate} テンプレートが保存されました！`);

        // 編集内容を反映させた後、再度テンプレート選択を空にしておく
        // templateSelect.value = "";
        // templateTitle.value = "";
        // templateDetails.value = "";
        // templateBudget.value = "";
    } else {
        alert("テンプレートを選択してください");
    }
});

// 新しい予定を保存する際に、選択されたテンプレートを適用
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

            // テンプレート保存処理（オプション）
            const selectedTemplate = templateSelect.value;
            if (selectedTemplate && templates[selectedTemplate]) {
                // 編集したテンプレートを適用した予定を保存する
                console.log("選択されたテンプレート", templates[selectedTemplate]);
            }

            // スケジュールをデータベースに保存
            srvSaveSchedule(title, details, budget, selectedDate); // サーバーに保存リクエスト

            renderCalendar(currentDate); // カレンダーを再描画
        }
    }
    closeModal();
}



// **** ネット用の関数ここから ****

function srvSaveSchedule(title, details, budget, date) {
    // date is yyyy-mm-dd
    const xhr = new XMLHttpRequest();
    const reqUrl = url + "schedule?req=set"
            + "&id=" + id
            + "&year=" + date.split('-')[0]
            + "&month=" + date.split('-')[1]
            + "&day=" + date.split('-')[2]
            + "&title=" + title
            + "&budget=" + budget
            + "&details=" + details;
    console.log(reqUrl);
    xhr.open("GET", reqUrl);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            if (data.res === true) {
                alert('データベースにスケジュール登録完了');
            }
            else {
                alert('データベースにスケジュール登録失敗');
            }
        } else {
            alert(`Error: ${xhr.status}`);
        }
    };
}

function srvDeleteSchedule(date) {
    // 1つの日付に1つのスケジュールしかない前提
    var data_id = -1;
    const xhrSearchId = new XMLHttpRequest();
    const reqUrl = url + "schedule?req=getday"
            + "&id=" + id
            + "&year=" + date.split('-')[0]
            + "&month=" + date.split('-')[1]
            + "&day=" + date.split('-')[2];
    console.log(reqUrl);
    xhrSearchId.open("GET", reqUrl);
    xhrSearchId.send();
    xhrSearchId.responseType = "json";
    xhrSearchId.onload = () => {
        if (xhrSearchId.readyState == 4 && xhrSearchId.status == 200) {
            const data = xhrSearchId.response;
            // dataはjsonのlist[dict]の形
            if (data.length === 1) {
                // 1つの日付に1つのスケジュールしかない場合
                data_id = data[0].id;
            } else {
                alert('1つの日付に1つのスケジュールしかない前提でないため削除できません');
            }
        } else {
            alert(`Error: ${xhrSearchId.status}`);
        }
    };

    if (data_id === -1) {
        alert('データid: -1, 削除できません');
        return;
    }

    const xhr = new XMLHttpRequest();
    reqUrl = url + "schedule?req=delete"
            + "&id=" + id
            + "&data_id=" + data_id
    console.log(reqUrl);
    xhr.open("GET", reqUrl);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            if (data.res === true) {
                alert('データベースからスケジュール削除完了');
            }
            else {
                alert('データベースからスケジュール削除失敗');
            }
        } else {
            alert(`Error: ${xhr.status}`);
        }
    };
}

function srvGetSchedule() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    const xhr = new XMLHttpRequest();
    console.log(url + "schedule?req=get"
            + "&id=" + id
            + "&year=" + year
            + "&month=" + month
        );
    xhr.open("GET", url + "schedule?req=get"
            + "&id=" + id
            + "&year=" + year
            + "&month=" + month
        );
    xhr.send();
    xhr.responseType = "json";

    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const resData = xhr.response;
            // dataはjsonのlist[dict]の形
            console.log(resData);
            if (resData.res === false) {
                alert('データベースからスケジュール取得失敗!!!!!!!!!!!!');
                return;
            }
            const data = resData.data
            for (let i = 0; i < data.length; i++) {
                const date = `${year}-${month}-${data[i].day}`;
                console.log(date
                    + " " + data[i].title
                    + " " + data[i].details
                    + " " + data[i].budget
                );
                scheduleData[date] = {
                    title: data[i].title,
                    details: data[i].details,
                    budget: data[i].budget,
                };
            }
            renderCalendar(currentDate);
        } else {
            alert(`Error: ${xhr.status}`);
        }
    };
}
