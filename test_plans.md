# Part 1: Description of Overall Test Plan

<br>

# Part 2: Test Case Descriptions
## Web Scraper Tests (WS):
- WS1
    - Test that the web scraper is picking up all desired text from a webpage
    - Test web scraper on a sample webpage and compare with predetermined results
    - Input: pre-made sample webpage
    - Output: array containing all text from heading and paragraph HTML tags
    - Normal
    - Whitebox
    - Functional 
    - Unit test
- WS2
  - Test that the text highlight input tool is working properly
  - Test that when using the option to highlight text to fact-check, the proper text is being passed along to the backend
  - Input: specific highlighted text from a webpage
  - Output: array containing the precisely highlighted text
  - Normal
  - Whitebox
  - Functional
  - Unit

## Statement Finder Tests (SF):
- SF1
    - Test that the statement finder tool is finding all desired statements from some text
    - Test statement finder by giving it an array of text and checking against an expected array of outputs
    - Input: array of text gathered from a webpage
    - Output: Array of all statements gathered from the text
    - Normal
    - Whitebox
    - Functional
    - Unit test
- SF2
    - Test that the statement finder tool is not finding opinions
    - Test that the statement finder tool is not including opinions in the output
    - Input: text array with opinion statements
    - Output: array of statements that doesn't include opinions
    - Boundary
    - Whitebox
    - Functional
    - Unit
- SF3
    - Test that the statement finder tool is not finding questions
    - Test that the statement finder tool is not including questions in the output
    - Input: text array with questions
    - Output: array of statements that doesn't include questions
    - Boundary
    - Whitebox
    - Functional
    - Unit
- SF4
    - Test that the statement finder tool is not finding commands
    - Test that the statement finder tool is not including commands in the output
    - Input: text array with commands
    - Output: array of statements that doesn't include commands
    - Boundary
    - Whitebox
    - Functional
    - Unit
- SF5
    - Test that the statement finder tool is not finding salutations (such as "Good Morning!")
    - Test that the statement finder tool is not including salutations in the output
    - Input: text array with salutations
    - Output: array of statements that doesn't include salutations
    - Boundary
    - Whitebox
    - Functional
    - Unit

## Chrome Extension Tests (CE):
- CE1
  - Test that extension toolbar pop-up activates appropriately
  - Click on extension toolbar icon and ensure that the pop-up is fully visable and buttons are clickable
  - Input: Click
  - Output: Superficial extension operation
  - Normal
  - Whitebox
  - Function
  - Integration

- CE2
  - Test that full page fact check feature is activated through pop-up button press
  - Click on extension toolbar icon, click "Fact-Check This Page" button
  - Input: Click
  - Output: Full page fact-check assessment
  - Normal
  - Whitebox
  - Functional
  - Integration

- CE3
  - Test that context menu displays "Fact-Check" option when highlighting text
  - Highlight and right-click text, ensure "Fact-Check" option is available
  - Input: Click
  - Output: Superficial extension operation
  - Normal
  - Whitebox
  - Function
  - Integration

- CE4
  - Test that single statement fact check feature is activated through context menu
  - Highlight and right-click text, click "Fact-Check" option
  - Input: Click
  - Output: Single statement fact-check assessment
  - Normal
  - Whitebox
  - Functional
  - Integration

<br>

# Part 3: Test Case Matrix
| Name | Normal/Abnormal | Blackbox/Whitebox | Functional/Performance | Unit/Integration |
| --- | ---| --- | --- | --- |
| WS1 | Normal | Whitebox | Functional | Unit |
| WS2 | Normal | Whitebox | Functional | Unit |
| SF1 | Normal | Whitebox | Functional | Unit |
| SF2 | Boundary | Whitebox | Functional | Unit |
| SF3 | Boundary | Whitebox | Functional | Unit |
| SF4 | Boundary | Whitebox | Functional | Unit |
| SF5 | Boundary | Whitebox | Functional | Unit |
| CE1 | Normal | Whitebox | Functional | Integration |
| CE2 | Normal | Whitebox | Functional | Integration |
| CE3 | Normal | Whitebox | Functional | Integration |
| CE4 | Normal | Whitebox | Functional | Integration |