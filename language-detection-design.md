# 語言檢測功能設計

## 概述
實現根據瀏覽器語言自動顯示相應語言的功能，支援中文（繁體）和英文兩種語言。

## 語言檢測邏輯

### 檢測順序
1. 用戶設定的語言（存儲在本地存儲中）
2. 瀏覽器語言設定
3. 預設語言（zh-TW）

### 支援的語言
- `zh-TW`：繁體中文（預設）
- `en`：英文

### 瀏覽器語言映射
- 以 `zh` 開頭的語言代碼 → `zh-TW`
- 以 `en` 開頭的語言代碼 → `en`
- 其他語言代碼 → `zh-TW`（預設）

## 實現細節

### 1. 語言檢測函數
```javascript
function detectLanguage() {
  // 檢查用戶是否已設定語言偏好
  const userLang = localStorage.getItem('userLanguage');
  if (userLang && ['zh-TW', 'en'].includes(userLang)) {
    return userLang;
  }
  
  // 獲取瀏覽器語言設定
  const browserLang = navigator.language || navigator.userLanguage;
  
  // 根據瀏覽器語言映射到支援的語言
  if (browserLang.startsWith('zh')) {
    return 'zh-TW';
  } else if (browserLang.startsWith('en')) {
    return 'en';
  }
  
  // 預設返回繁體中文
  return 'zh-TW';
}
```

### 2. 語言資源加載
```javascript
async function loadLanguageResources(lang) {
  try {
    const response = await fetch(`/lang/${lang}.json`);
    if (response.ok) {
      return await response.json();
    } else {
      // 如果無法加載指定語言，回退到預設語言
      console.warn(`Failed to load language resources for ${lang}, falling back to zh-TW`);
      const fallbackResponse = await fetch('/lang/zh-TW.json');
      return await fallbackResponse.json();
    }
  } catch (error) {
    console.error('Error loading language resources:', error);
    // 返回基本的預設資源
    return {
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
    };
  }
}
```

### 3. 語言切換功能
```javascript
function switchLanguage(lang) {
  // 保存用戶語言偏好
  localStorage.setItem('userLanguage', lang);
  
  // 重新加載語言資源並更新界面
  loadLanguageResources(lang).then(resources => {
    window.langResources = resources;
    updateUIWithLanguage(resources);
  });
}
```

## 整合到現有應用

### 初始化流程
1. 應用啟動時調用 `detectLanguage()` 檢測語言
2. 根據檢測結果加載對應語言資源
3. 使用語言資源更新界面文本

### 與現有功能的兼容性
- 不影響現有的任務數據結構
- 不改變現有的數據存儲方式
- 僅影響界面顯示文本

## 錯誤處理

### 資源加載失敗
- 回退到預設語言資源
- 記錄錯誤日誌但不中斷應用運行

### 不支援的語言
- 自動映射到最接近的支援語言
- 預設使用繁體中文

## 測試方案

### 支援的測試場景
1. 繁體中文瀏覽器環境
2. 英文瀏覽器環境
3. 其他語言瀏覽器環境（應回退到預設）
4. 網絡問題導致語言資源無法加載
5. 用戶手動切換語言

### 測試步驟
1. 在不同語言設定的瀏覽器中打開應用
2. 驗證界面文本是否正確顯示對應語言
3. 模擬網絡錯誤，驗證回退機制
4. 檢查語言切換功能是否正常工作