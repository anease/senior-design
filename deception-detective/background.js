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
          // Converting response to text (could change this to JSON)
          return response.text(); 
        }).then(function(data) {
          // This is the converted response data that we will use
          console.log(data); 
        });


        chrome.tabs.create({url: chrome.extension.getURL("result-page.html")})


});
