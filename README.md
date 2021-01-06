# Python-SCP-File-Transfer-And-Integrity-Test-For-Txt

DESCRIPTION

Script that sends a file via scp to remote host, then checks that the wording of the transferred file matches the original.
Variables either defined in the source code or defined when prompted for user input. 
Can be used f.ex. for sending configuration files or script files, and checking for the file integrity once transferred.

COMMAND LINE OPTIONS
- use [ -v ] to have printed the original and transferred content upon making comparison  

# Dockerfile

To build from Dockerfile and run in Docker follow the following steps:

1. Clone the repository to your local drive
2. Inside the local directory for the repository there is now a file called SCPTestCase.py, this file contains the variables such as remote host and filepath to set, if they are not set the script will ask for them when running.
3. The file you want to copy has to be located in the same folder as the Dockerfile, because the Dockerfile copies all from that folder to the container, and can only send that which is within the container. Alternatively a specific copy path could seperately be specified in the Dockerfile.
4. To run the program from Docker open terminal in the same folder as Dockerfile is located and run the following commands:

docker build -t scp .

docker run -it scp
