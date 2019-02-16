# backend

## Running for development

1) Run `./reseed.sh`

2) Run `pipenv install`

3) To run the server, run `pipenv run python3 app.py`

   To run the server in debug mode, run `FLASK_DEBUG=1 pipenv run python3 app.py`

## Running for production

1) Login as the user "energy"

2) Do steps 1 and 2 from above as needed

3) Use make to launch the server

   * Copy Makefile-prod to Makefile
   * Edit Makefile to enter our database password where required
   * Run `make run` or `make debug`
   * **Do not** add Makefile to the repository

## Data pipeline from the Siemens Insight server

1) Create _Trend Interval Reports_

   Use Insight's Report Builder to create reports (mostly by building) for all
   the points we want. Settings should include:

   * Name the report using a naming convention that makes clear that this is one of our reports, not the Facilities staff's production reports. At this writing, all our reports are named "ONDICH-SOMETHING".
   * Add Trend Points using the Trend Points Configure button
   * Date Range: Yesterday
   * Reporting Interval: 15 minutes (or 30 or 60 or 5 if that's what we want)
   * Report Timings: All for all days
   * Screen, Printer, Email, Macro: No
   * Delimiter: Yes - Comma
   * Display: Using System Names
   * File: location and name of file; currently C:\Users\jondich\Documents\insight-reports\boliou1.csv (where "boliou1" is the name of this particular report, which will get extended by the file creation date and time (e.g. "boliou1\_11-30-18\_02-00.csv")

2) Schedule the creation of each report

   Use Insight's Scheduler to schedule regular generation of existing reports.

   * Go to the Schedule -> New -> Report... menu
   * Use the Object Selector dialog to search for your existing report by name (with wildcards as appropriate, e.g. "ondich\*")
   * Add the scheduled report with scheduled date (starting date), time of day (usually middle of the night), Repetition Frequency: Daily

3) Schedule the upload script

   Use the Windows Task Scheduler in the Server Manager application to run our upload script periodically (currently, it's set to run once per hour). This only had to be done one time, so this is just a record of how it was set up in the first place.

   * In Server Manager, navigate to Configuration -> Task Scheduler -> Task Scheduler Library
   * Duplicate the "Lucid BuildingDashboard Push" task
   * In the Action tab, make sure the action is "Start a program" and the program is "wscript.exe" with command-line argument the full path to the script (currently C:\Users\jondich\Documents\scripts\ondich-data-upload.vbs).

4) About the upload script

   This is a copy of the Lucid upload script. It's pretty straightforward Visual Basic, with a ton of configration options at the top of the script. Currently, it is set to submit all files it finds in C:\Users\jondich\Documents\insight-reports\ via POST to http://[OUR-SERVER-NAME]:8080/upload/siemens, and then move those files to C:\Users\jondich\Documents\archive\.

   TO DO: make the script upload only CSV files from the source directory, just in case other files end up there.

5) About ports and firewalls

   The Siemens Insight server can communicate with our server only over ports 80, 8080, or 8081. We'll use port 80 for our web server, port 8080 for our API (including the /upload/siemens and /upload/alc endpoints), and port 8081 for development of any future communications between the Siemens and ALC servers and our server.

