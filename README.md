dataHelpers
===========

A little subset of tools that will generate breqFast request files from a LASIF project. These can then be submitted to IRIS, and data can be downloaded from the command line.

Instructions.

You should download or place this folder in your LASIF project directory. The following assumes that you have:
  
  1.) Event information downloaded via LASIF.
  
  2.) A list of stations in a text file (see stationList.txt in this repository for an example). Really simple though, just a bunch of columns that go like STATION NETWORK.
  
  3.) A breqFast request template. This is also really easy, see breqFastTemplate.txt for an example.

That should be it I think. The workflow for batch downloading data goes like this.

  1.) Run generateAllBreqFastRequests.py in your LASIF project directory (i.e. ./dataHelpers/generateAllBreqFastRequests.py). This will ask for your stations file, and a recording time (in hours). It will look through your previously-populated events directory and parse out event start times. A script called breqDriver should be created. Run this.

  2.) breqFastDriver.sh should create a ./MISC and ./MISC/breqFastRequests directory. In this ./MISC/BreqFastRequests directory will be a bunch of file which are your breqFastRequests (one per event).

  3.) Run emailBreqFastRequest.sh to batch email all of those requests to IRIS. CAREFUL. MAKE SURE THEY LOOK ALL RIGHT BEFORE YOU DO THIS. Also, remember that my email is the one in the example template, please exchange this with your own to spare me the wrath of IRIS (...which sounds like a good movie title). It is normal for the script to sleep for 5 seconds between sends.

  4.) In a while you will get emails with a wget link. Just copy that to the command line and voila data.

Have fun.

Mike.
