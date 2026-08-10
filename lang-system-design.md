# 多語言支援系統設計

## 語言資源文件結構

### 中文語言資源 (zh-TW.json)
```json
{
  "appTitle": "HajimiTodotxt",
  "pageTitle": "☕ 待辦筆記",
  "addTask": "新增任務",
  "editTask": "編輯任務",
  "saveTask": "保存任務",
  "deleteTask": "刪除任務",
  "taskTitlePlaceholder": "任務標題 (可多行，存檔自動轉單行)",
  "taskDescriptionPlaceholder": "詳細描述 (支援多行，會被保存為 desc:\"...\")",
  "parentTask": "父任務",
  "priority": "優先級",
  "dueDate": "截止 (due)",
  "thresholdDate": "隱藏至 (t)",
  "recurrence": "重複 (rec)",
  "insertTag": "插入標籤",
  "insertCurrentTime": "插入現在時間",
  "today": "今",
  "tomorrow": "明",
  "none": "(無)",
  "noPriority": "-",
  "searchPlaceholder": "搜尋...",
  "clear": "清空",
  "savedFilters": "常用過濾器",
  "saveCurrentFilter": "儲存當前過濾",
  "noTags": "無標籤",
  "noSavedFilters": "尚無儲存的過濾器",
  "deleteFilterConfirm": "刪除此過濾器？",
  "filterInputEmpty": "過濾欄是空的",
  "nameFilter": "請為此過濾器命名:",
  "doneSection": "📦 已完成",
  "expand": "展開...",
  "collapse": "收起",
  "taskTree": "🌳 任務族譜",
  "settings": "⚙️ 設定",
  "theme": "主題 (Theme):",
  "neutral": "中性 (Neutral)",
  "dark": "暗黑 (Dark)",
  "girly": "少女 (Girly)",
  "confirmDelete": "刪除前確認:",
  "showDeleteButton": "顯示刪除按鈕:",
  "syncInfo": "尚待實作",
  "sortPriority": "排序優先級",
  "ascending": "正序",
  "priorityLabel": "優先級",
  "dueDateLabel": "截止日",
  "createdDateLabel": "建立日",
  "doneDateLabel": "完成日",
  "subjectLabel": "標題",
  "noSort": "(無)",
  "showHiddenTasks": "顯示/隱藏未來任務",
  "addTaskButton": "新增任務 (Add)",
  "sortButton": "排序 (Sort)",
  "settingsButton": "設定 (Settings)",
  "deleteConfirm": "確定刪除？",
  "deleteChildrenConfirm": "刪除將連帶刪除 {count} 個子任務，確定？",
  "completeChildrenConfirm": "完成此任務將同步完成 {count} 個子任務，確定？",
  "saveFilter": "+ 儲存當前過濾"
}
```

### 英文語言資源 (en.json)
```json
{
  "appTitle": "HajimiTodotxt",
  "pageTitle": "☕ Todo Notes",
  "addTask": "Add Task",
  "editTask": "Edit Task",
  "saveTask": "Save Task",
  "deleteTask": "Delete Task",
  "taskTitlePlaceholder": "Task title (multiline, auto-convert to single line when saved)",
  "taskDescriptionPlaceholder": "Detailed description (supports multiline, will be saved as desc:\"...\")",
  "parentTask": "Parent Task",
  "priority": "Priority",
  "dueDate": "Due Date",
  "thresholdDate": "Threshold Date",
  "recurrence": "Recurrence",
  "insertTag": "Insert Tag",
  "insertCurrentTime": "Insert Current Time",
  "today": "Today",
  "tomorrow": "Tomorrow",
  "none": "(None)",
  "noPriority": "-",
  "searchPlaceholder": "Search...",
  "clear": "Clear",
  "savedFilters": "Saved Filters",
  "saveCurrentFilter": "Save Current Filter",
  "noTags": "No Tags",
  "noSavedFilters": "No Saved Filters",
  "deleteFilterConfirm": "Delete this filter?",
  "filterInputEmpty": "Filter input is empty",
  "nameFilter": "Please name this filter:",
  "doneSection": "📦 Completed",
  "expand": "Expand...",
  "collapse": "Collapse",
  "taskTree": "🌳 Task Tree",
  "settings": "⚙️ Settings",
  "theme": "Theme:",
  "neutral": "Neutral",
  "dark": "Dark",
  "girly": "Girly",
  "confirmDelete": "Confirm Delete:",
  "showDeleteButton": "Show Delete Button:",
  "syncInfo": "Yet to be implemented.",
  "sortPriority": "Sort Priority",
  "ascending": "Ascending",
  "priorityLabel": "Priority",
  "dueDateLabel": "Due Date",
  "createdDateLabel": "Created Date",
  "doneDateLabel": "Done Date",
  "subjectLabel": "Subject",
  "noSort": "(None)",
  "showHiddenTasks": "Show/Hide Future Tasks",
  "addTaskButton": "Add Task",
  "sortButton": "Sort",
  "settingsButton": "Settings",
  "deleteConfirm": "Confirm delete?",
  "deleteChildrenConfirm": "Deleting will also delete {count} child tasks, confirm?",
  "completeChildrenConfirm": "Completing this task will also complete {count} child tasks, confirm?",
  "saveFilter": "+ Save Current Filter"
}
```

## 語言檢測實現

### 前端語言檢測
```javascript
function detectLanguage() {
  // 優先順序：
  // 1. 用戶設定的語言
  // 2. 瀏覽器語言
  // 3. 預設語言 (zh-TW)
  
  const userLang = localStorage.getItem('userLanguage');
  if (userLang) return userLang;
  
  const browserLang = navigator.language || navigator.userLanguage;
  if (browserLang.startsWith('zh')) return 'zh-TW';
  if (browserLang.startsWith('en')) return 'en';
  
  return 'zh-TW'; // 預設語言
}
```

## 多語言實現方案

### 1. 資源加載
- 在應用啟動時加載相應語言的資源文件
- 將資源存儲在全局變量中供後續使用

### 2. 文本替換
- 創建一個翻譯函數 `t(key)` 用於獲取對應語言的文本
- 在HTML中使用數據屬性標記需要翻譯的元素
- 在JavaScript中動態替換文本內容

### 3. 動態更新
- 當語言切換時，重新渲染界面
- 保持用戶數據不變

## 實現步驟

1. 創建語言資源文件系統
2. 實現語言檢測功能
3. 修改前端HTML以支援多語言
4. 更新JavaScript以支援語言切換
5. 測試多語言功能