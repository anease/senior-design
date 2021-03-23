// Initialize extension context menu
chrome.runtime.onInstalled.addListener(function() {
    chrome.contextMenus.create({
      id: "testSelectContextMenu",
      title: "Fact-Check",
      contexts: ["selection"]
  });
});

// Local Flask Server Default URL
let factCheckURL = "http://127.0.0.1:5000/factcheck"

// Define context menu actions after text highlight and right click
chrome.contextMenus.onClicked.addListener(function(info, tab) {
        // Context Menu reference that makes sense
        // https://chrome-apps-doc2.appspot.com/extensions/contextMenus.html#type-OnClickData
        console.log(info.selectionText);
        
        
        // Send Selected Text to the Fact Check API
        fetch(factCheckURL, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            data: info.selectionText
          })
        
        })
        .then(function(response) {
          // Converting response object to JSON
          return response.json(); 
        }).then(function(data) {
          // This is the converted response data that we will use
          console.log(data); 

          // Conditions to display error page instead of result page
          if (data.statementsParsed == 0){
            chrome.tabs.create({url: chrome.extension.getURL("error-page.html")})
          }
          
          else {
            chrome.tabs.create({url: chrome.extension.getURL("result-page.html")},
                      
                      // Really funky workaround to inject data from API into the result page HTML
                      function(tab){
                        var selfTabId = tab.id;
                        chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
                            if (changeInfo.status == "complete" && tabId == selfTabId){
                                // send the data to the page's script:
                                var tabs = chrome.extension.getViews({type: "tab"});

                               tabs[0].injectResultData(info.selectionText, data);
   
                            }
                        });
            });

          }

        });

});
