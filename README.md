# chew-apache2
A python script that analyses the Apache2 log file

Function
---------

Making more sense out of the Apache2 log file.

How to Use
----------

You should install Python3 first.  After you successfully installed Python3,  type the following command in the command line, 

`python chew_apache2.py`

You might want to change options in the first several lines.  

- log_filename: put your Apache log file name
- cut_ip: put the IPs that you are not interested in (for example, IPs from the search engines companies)
- period: put the particular period you want to look at
- show_only_page_with_words: show me only the links that contain certain words
