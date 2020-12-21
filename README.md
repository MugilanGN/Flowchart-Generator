# Flowchart-Generator
Automatically creates Flowcharts from Pseudocode!
<img src="flowchart.png" width="629" height="500">

## Video Demo

https://www.youtube.com/watch?v=1gCqPBzU8Z0

## Installation

This project was built on Python 3.7.4

Run this to install the necessary dependencies:

```sh 
pip install Pillow click
```

Next, clone this project.

## Writing the Pseudocode

The Pseudocode is entered into a .txt file. It follows strict rules which must be obeyed

<img src="enter.png" alt="alt text">

### Rules

STOP and START are automatically input by the program, so do not need to be added

Indents don't affect the program, so nothing has to be indented, and incorrect indentation is allowed

The capitalization of the keywords is extremely important. If an error occurs, double check if you have capitalized the keywords like "TO" and "FOR" properly

ELSE IF is not available, but nested IFs are possible

The ENDIF, NEXT var, and ENDWHILE blocks are mandatory

### Syntax Guide

 #### Input and Output:

  - INPUT x 
  - OUTPUT x

   ```sh
   INPUT X
   OUTPUT var
   OUTPUT "hello"
   ```
#### IF statements:
  - IF condition THEN
  - ELSE
  - ENDIF
  
  ```sh
  IF x < 3 THEN
    OUTPUT X
  ELSE
    OUTPUT x*2
  ENDIF
  ```
  The else statement is optional (ENDIF is still necessary)
  
   ```sh
  IF x < 3 THEN
    OUTPUT X
  ENDIF
  ```
  
  #### Process-type blocks:

  ```sh
  x = x + 1
  y = x / 2
  ```
  
  #### While loops:

  - WHILE condition DO
  - ENDWHILE
  
  ```sh
  WHILE x < 5 DO
    OUTPUT x
  ENDWHILE
  ```
  #### For loops:
   
  - FOR var <- start TO end
  - NEXT var
  
  ```sh
  FOR i <- 1 TO 5
    OUTPUT i
  NEXT i
  ```

## CLI usage

To run the code, simply execute the following command:
```sh
python Converter.py
```

### Arguments
  
  Arguments in the CLI are typed like so: ```--size=20``` or ```--code="enter.txt"```
 
  - ```--size``` is the font size used. This controls the size of the entire flowchart as well. By default it is 20px
  - ```--font``` is the font path. A default NotoSans font is used at "./fonts/", but can be changed for different OSs or fonts
  - ```--output``` is the flowchart's image file. Default is "flowchart.png"
  - ```--code``` is the file with the pseudocode. Defaults to "enter.txt"
  - ```--help``` provides CLI help
  
  For example:
  
  ```sh
  python Converter.py --code="code.txt" --size=30 --output="result.png"
  ```

### Flowchart Image

This image contains the created flowchart which can be shared, printed, etc. Its size varies exactly on the size of the flowchart created, so it may even hit a resolution of 10k pixels! However if the generated flowchart is too big, then the image will be unopenable due to being too large. The user should be careful with flowchart sizes.

## Support

If you are having issues, please let me know. You can contact me at mugi.ganesan@gmail.com
