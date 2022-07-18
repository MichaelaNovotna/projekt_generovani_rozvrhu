<img src="img/work-schedule.png" alt="Schedule generator" style="width: 10%;" align="right"/>

# Schedule Generator Project

This Python application allows users to generate a schedule for small classes like language teaching, small work schedules etc., based on input criteria:
- possible day and time blocks of lectors
- possible day and time blocks of students
- subjects taught by lectors
- subject registered by students

## Getting started
Program requires 2 configuration files, input from lectors and input from students. Path for these files including example is:
* `/input`

with file names:

* `input_lectors.csv`
  * with 2 required columns `name`, `course`, followed by available time blocks in format `<weekday hh:mm>`
* `input_students.csv`
  * with 2 required columns `name`, `course`, followed by available time blocks in format `<weekday hh:mm>`

#### Testing the input
Your input can be tested with prepared pytest file that can be found in `/test` directory and can be run with `pytest input_test.py` 

## Running the program and output files
Program can be run with `schedule_generator.py` file using Python 3:
* `./python3 schedule_generator.py`

Output of the program is HTML document with constructed schedule visualised as a table for single lector:



## Algorithm
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Limitations




## License
For open source projects, say how it is licensed.
