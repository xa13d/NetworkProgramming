# TCP-based web scrapping service

## Server side
The connection is established using TCP and server is able to serve multiple clients.
It will take URLs and scraps it, showing how many images/paragraphs the link has.

Command to install requirements:
pip install requirements.txt

Command to run it:
_python webscraper.py server_
  
  
* --host "host"  
Provides an interface for the server. Default - 127.0.0.1

* --port "port"  
Provides a port for server to listen. Integer required. Default value - 1060.

## Client side

To run the script as a client the following command in used:  
_python webscraper.py server -p url_


* --host "host"  
Provides an interface for the server. Default - 127.0.0.1

* --port "port"  
Provides a port for server to listen. Integer required. Default value - 1060.

* -p url
Mandatory option, as URL needs to be entered to start the scraping service.
