Project Log Analysis

This project requires a virtual environment which will be made using combination of Virtual Box and Vagrant.

databaseQueries.py is the python code which deals with the database. index.py is the main file which drives the code of the database.

Steps for setup of the virtual environment

Step 1: Clone the project repository and connect to the virtual machine $ git clone https://github.com/mlupin/fullstack-nanodegree-logs-analysis.git

Step 2: $ cd fullstack-nanodegree-logs-analysis $ vagrant up

Step 3: $ vagrant ssh

Step 4: $ cd /vagrant

Step 5: Now load the file containing all the data regarding the log here. Name of the file is newsdata.sql.

Step 6: $ psql -d news -f newsdata.sql

Running the project:

Step 7: $ python databaseQueries.py

Step 8: $ python index.py

Step 9: Open your browser and go to the localhost:8080/log_analysis

Step 10: Click the button to get the desired output
