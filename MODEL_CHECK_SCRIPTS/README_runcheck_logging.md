# run_checks_33_reduced.sh: Run Check Log Simplification and Prioritization
# run_checks_python_V1.sh
This version of run_checks enhances the logging system for run_checks by introducing simplified log outputs, priority-based tagging, and configurable exclusion filtering.

---

## Features

### 1. Simplified Log Generation
- **Purpose**: Streamline logs by excluding noise/known issues.
- **How it works**:
  - Uses an exclusion list located at:
    ```
    /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/log_exclusion_list.csv
    ```
  - Entries in the first column of the CSV are substrings used to match and exclude lines from the output.
  - to add an exclusion add a row to the csv in the following format:
    "<log entry to exclude>", "<username>", "<note explaining why you are excluding this entry with date>" 
- **Output**:
  - A simplified log is generated in the same directory as the original log.
  - File naming format:  
    ```
    <date><time>:<clone>_simplified.log
    ```

### 2. Verbose Log Retention
- A full, unfiltered version of the console output is automatically also generated.
- Located in the same directory and follows the same naming convention (without `_simplified` suffix).

---

#### Script: `reduce_runcheck_log.py`
##### Behavior
  - Reads the generated log file with full script output
  - Applies exclusions from the CSV list
  - Outputs a simplified log with excluded lines removed
  - Leaves the original log intact
  - Automatically kicked off at the end of a run_check execution


  ---

#### Notes
  - Ensure exclusion entries should be kept up to date and reviewed regularly.
  - Be cautious when filtering out log content — excluding too much can hide useful information.
  ---


### 3. Priority Tagging
- Each log entry is now prefixed with a priority label:
  ```
  HIGH PRIORITY:
  MEDIUM PRIORITY:
  LOW PRIORITY:
  ```
- Enables quick identification of critical issues.
- When adding a script, add the folowing code to prepend the priority lable to all of the script's outputs:
  ```
  | sed 's/^/MEDIUM Priority: /'
  ```
  for example, if you wanted to add a new run_check with a script called new_script.py you'd add it like this 
  ```
  python3 new_script.py | sed 's/^/MEDIUM Priority: /'
  ```

### 4. Console Log Coloring
- Console outputs are color-coded based on priority:
  - High priority logs: **Red**
  - Medium priority logs: **Yellow**
  - Low/Default priority logs: **White**
- When adding a new run check, use the following utility functions to set text color:
  ```
  set_red_text
  set_yellow_text
  ```
  After each script make sure to use the following function to set the color back to white:
  ```
  reset_text_color
  ```


  For example, if you wanted to add a new medium priority script called new_script.py, that you want to be color coded
  yellow and have a "MEDIUM Priority:" label prepended, you'd add it like this:
  ```
  set_yellow_text
  python3 new_script.py | sed 's/^/MEDIUM Priority: /'
  reset_text_color
  ``` 
  These ensure consistent visual cues during execution.

### 5. Run Check Grouping
- Checks are bucketed based on severity and operational importance.
- Improves the debugging workflow and incident prioritization.

