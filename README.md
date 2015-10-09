# chew-apache2
`chew-apache2` is a python script that analyzes the Apache2 access log file.

Function
---------

Make more sense out of the Apache2 access log file.  Print unique visting IPs.  Sort these IPs according to their visiting frequency.  Get the geological location of these IPs.  Print pages visited, sorted in decreasing order of visit times.

How to Use
----------

You should install Python3 first.  After you successfully installed Python3,  type the following command in the command line, 

`python chew_apache2.py`

You might want to change options in the first several lines.  

- log_filename: put your Apache log file name
- cut_ip: put the IPs that you are not interested in (for example, IPs from the search engines companies)
- period: put the particular period you want to look at
- show_only_page_with_words: show me only the links that contain certain words

Output
------

The first line gives a summary of visits.  It contains three numbers.  The first number is the total number of visits (IPs) within `log_filename`, the second number is the total number of IPs that are not in list `cut_ip`, and the last number is the number of unique IPs from the second number.

You can search for `**` for remaining summaries.

