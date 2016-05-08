This tool lets you fetch and send RSS feeds via your Kindle email address directly to your Kindle as a book. It is currently developed on a RasPi3 and is intended to run on similiar hardware (especially RasPi2 and 3).

Currently the code is pretty ugly, but it is functional and does the job. I will clean up and prettify the code base and the created Kindle book in the future.

You can set up a cron job to get feeds on a regular basis. Just set up your feeds by running app.py and heading to [ip]:8000 

Currently your Kindle mail address (https://www.amazon.com/mn/dcw/myx.html/#/home/devices/1) can be set up via the WebUI, but is not used at this point and has to be set up manually in PiRSS2Kindle.py.

To get this thing up and running you need the following python packages installed (pip install [package]):

sqlite3<br />
tornado<br />
feedparser<br />
time (if it is not installed)

Also you will need the following packages installed on your system:

ssmtp<br />
mailutils<br />
sqlite3 (might not be needed, but I installed it and am too lazy to test without this package)

You'll then have to set up ssmtp as described here: https://wiki.archlinux.org/index.php/SSMTP
I may add an option in settings to set this up via the WebUI in the future.

After this has been done you can run app.py and add your RSS feeds. There is currently a bug where, after setting up one feed, the list of subscribed feeds is not displayed, so you may have to reload the page (as I said, this thing is currently WIP and needs a lot of work).

To get your feeds just run PiRSS2Kindle.py either manually or via a cron job (https://wiki.archlinux.org/index.php/Cron).
