# Statement Finder

## Description
This tool takes text from a given web page, parses it, and returns a list of statements from that webpage that will be used by the next tool in the process of our overall project.

## Table of Contents
- 1-19-21-prototype-model-comparison.PNG
    - This is a screenshot showing the results of testing the statement finder prototype with two different classifier models (RandomForestClassifier and GradientBoostingClassifier). The tool was run with each model 5 times and the precision, recall, and accuracy of each test are shown. The RandomForestClassifier appeared to have better accuracy in general, so that was the classifier I chose to use in the prototype. One observation to note is that the recall was low and inconsistent throughout these test runs. In future iterations of this tool, I hope to consistently increase the recall.
- dataset-binary.txt
    - This dataset is a combined list of statements, opinions, and nonstatements that only differentiates between statements and nonstatements (opinions and nonstatements datasets). This dataset is being used for the early stages of the statement_finder_prototype, but may be replaced later on.
- dataset-nonstatements.txt
    - This dataset is a list of non-statements (questions, commands, exclamations) to be built upon, then added to the aggregate training dataset (either dataset-binary or dataset).
- dataset-opinions.txt
    - This dataset is a list of opinions to be built upon, then added to the aggregate training dataset (either dataset-binary or dataset). For the purposes of our project, opinions are not considered statements.
- dataset-statements.txt
    - This dataset is a list of statements to be built upon, then added to the aggregate training dataset (either dataset-binary or dataset).
- dataset.txt
    - This dataset is a combined list of statements, opinions, and nonstatements. This dataset may replace dataset-binary in a future iteration.
- model_comparison.py
    - This tool is used to test different learning models for the statement finder tool.
- research-and-decisions.md
    - Markdown file containing the research notes relevant to the tool as well as a list of decisions that were made about vasious aspects of the tool.
- sf-design.md
    - Markdown file containing the design documentation for the statement finder program.
- statement_finder_prototype.py
    - This tool finds and determines the statements from text on a webpage.