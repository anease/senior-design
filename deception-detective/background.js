// Initialize extension context menu
chrome.runtime.onInstalled.addListener(function() {
    chrome.contextMenus.create({
      id: "testSelectContextMenu",
      title: "Fact-Check",
      contexts: ["selection"]
  });
});

// Define context menu actions after text highlight and right click
chrome.contextMenus.onClicked.addListener(function(info, tab) {
        // Context Menu reference that makes sense
        // https://chrome-apps-doc2.appspot.com/extensions/contextMenus.html#type-OnClickData
        console.log(info.selectionText);
        //factCheck(info.selectionText);
});
