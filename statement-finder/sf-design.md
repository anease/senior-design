# Statement Finder Design

## Overview
This tool will take some text as input and output a list of statements made within the text.

## Context
The statement-finder tool is one part of the process for the overall fact-checking tool.
- The first step in the fact-checking tool will be to gather the text from the webpage. This is where the input for this tool comes from.
- The second step is this statement-finder tool.
- The third step will take the output from the statement-finder (a list of statements) and determine their factual integrity.
- The final step will be to display the results to the user.

## Goals
- Return a list of statements
- Eliminate opinions from the list
- Replace pronouns with their antecedents before returning the statements to make fact-checking them easier
- Time permitting: find statements within sentences

## Scope
The current scope of this tool is to return sentences containing statements and replace any pronouns within these statements with their antecedents.

The original intended scope of this tool was to return each statement made within the input text. This might not be possible to complete within the allotted time, so it is now a stretch goal rather than the scope of the project.

## Input
The statement-finder method will take a string as input. There are 2 considerations for input in the context of the overall project:
- 1 ) The user highlights some text from a page
    - One string will be passed to the statement-finder method 
- 2 ) The user selects "Fact-check this page" option
    - Multiple strings will be pased to the statement-finder tool

Sample input: "I like going to the zoo. Cheetahs are my favorite animal there! They can run up to 80 miles per hour! What is your favorite animal? Mr. Smith was our guide last time."

## Output
The statement-finder method will output an array of strings. Each string will be a searchable statement to the fact-checker.

Sample output (based on above sample input): ["[cheetahs] can run up to 80 miles per hour", "Mr. Smith was our guide last time"]

## Milestones
Each milestone will be a working version of the tool that will build upon the functionality of the previous milestones.
- First prototype of the tool, returns a list of statements based on elementary classification method.
- Tool replaces pronouns with their antecedents.
- Final version of tool, correctly classifies all tested text and return search-optimized statements.

## Timeline
- 2/6/2021: Doc written, first version complete
- 2/13/2021: First version of pronoun replacement added
- 2/20/2021: Refinement of pronoun replacement complete
- 2/27/2021: Additional refinements of tool in progress
- 3/6/2021: Additional refinements of tool complete
- 3/13/2021: Testing of tool complete
- 3/20/2021: Final draft complete
- 3/27/2021
- 4/3/2021: Hard deadline for final draft
- 4/10/2021: Virtual Expo