# CS429_IR_Final
Final Project Information Retrieval system for CS429

Project Report: https://github.com/tissoSmelly/CS429_IR_Final/blob/main/Project%20Report%20mmednis.pdf

**HOW TO RUN QUERIES SIMPLY**

1. Clone Repo
2. Run flask_app.py
3. Send curl POST request to port 5000 on local machine to /make-query (e.g. 127.0.0.1:5000/make-query)
4. Data POSTED must follow JSON format as follows {"Query": "this is my example query", "K": 10}
5. You will receive ranked results from the default index set in flask_app.py source code
NOTE: JSON is case-sensitive 


I hope this all works on your system
