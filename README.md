TO RUN:

Have latest Python3.X

Have pip

Run "pip install notion"

TO CONFIGURE

in the top of the script are some config strings that need to be filled for the script to work:

icalURL is the link to the ical file of the calendar, for google calendar this is the Calender settings > secret address in iCal format, although it should take any ical file.

client is the token_v2 cookie of a user on the notion page with read/write permissions, (In months of use, this hasn't refreshed on me yet, but might need to be updated occasionally) the script acts as this user (if you notion is setup to autofil the user thats creating/adjusting the page, it will assume the identity of the person owning the cookie

calendarPage is the complete url of a Table view version of the database you want the iCal data to be written to
recordEndDate is a boolean choice on whether any end times found in the ical should be passed on to the Notion database, for aesthetic reasons I would turn this off unless your system relies on that data.


Last notes

This script polls the ical location once and then terminates itself, you would need to make a script/procedure that runs this scripts yourself based on your needs.
This script also assumes that all existing data in a database is valid data (i.e. no empty or incomplete rows).

iCals are weird with timezones, google calendar specificly sometimes adds timezones to its ical and sometimes not, I filter out those that I had trouble with in the filter array at line 9, this is a horrible way to fix this issue, but it works for my use case, GLHF americans.

Lastely, this script was designed for google calendar, it should work with many other icals though.

Enjoy
