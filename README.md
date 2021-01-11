#========================================================================================================
# Python-SCP-File-Transfer-And-Integrity-Test-For-Txt

DESCRIPTION

Script that sends a file via scp to remote host, then checks that the wording of the transferred file matches the original.
Variables either defined in the source code or defined when prompted for user input. 
Can be used f.ex. for sending configuration files or script files, and checking for the file integrity once transferred.

COMMAND LINE OPTIONS
- use [ -v ] to have printed the original and transferred content upon making comparison  

#=======================================================================================================

#======================================================================================================
# Dockerfile

To build from Dockerfile and run in Docker follow the following steps:

1. Clone the repository to your local drive
2. Inside the local directory for the repository there is now a file called SCPTestCase.py, this file contains the variables such as remote host and filepath to set, if they are not set the script will ask for them when running.
3. The file you want to copy has to be located in the same folder as the Dockerfile, because the Dockerfile copies all from that folder to the container, and can only send that which is within the container. Alternatively a specific copy path could seperately be specified in the Dockerfile.
4. To run the program from Docker open terminal in the same folder as Dockerfile is located and run the following commands:

docker build -t scp .

docker run -it scp

If you want the container to reflect any changes made on your local drive, inside the container, the container can also be run with a mounted volume. This might be useful f.ex. if you want to run the container first, and only after that copy the file to be transferred to the mounted folder, with the mounted folder being the folder from which the docker command is run. To run the container with volume binding run the following command (after buulding as scp):

docker run -it -v "$(pwd):/mydir" scp

#======================================================================================================

#======================================================================================================
# Docker Hub

The file can also be run directly from Docker Hub with the command below. Please note that if running from Docker Hub it will not be possible to set the runtime variables such as remote host and paths beforehand, instead these must be set on runtime when prompted for them. It is also necessary to run the container with volume bind, as the image already contains the build from Dockerfile, and so no local copying will happen fro the Dockerfile. However,when running the container from Docker Hub with the command below, the folder from which the command is run is mirrored inside the container, thus it is possible to put a file into this local folder and access it for sending inside the container.docker run -it -v "$(pwd):/mydir" stefanbdocker/scp-test-case



docker run -it -v "$(pwd):/mydir" stefanbdocker/scp-test-case


NEED TO REVIEW WHOLE DOCKER PART OF README note: refer to issues doc on changes

#======================================================================================================

#======================================================================================================
# NOTES - RUNNING THE PROGRAMME THROUGH USER INPUT WITH VARIABLES SET THROUGH PROMPT

A typical run of the program, when the variables have not been set in the source code file, will look as following:

1. Getting information on source file
Enter source file location (f.ex. /home/user/testfile.txt): 

2. Getting information on remote address
The remote address has not been determined, please input the name (f.ex. user@localhost):

3. Getting information on password
The password for remote host has not been determined, please input the password:

4. Getting information on destination path variables
A path to transfer the file to has not been assigned, please input the directory path (f.ex. /home/user/): 

5. All the necessary variables have been set to perform the transfer, commencing transfer

6. Getting the transferred content

7. Performing comparison

.
----------------------------------------------------------------------
Ran 1 test in 188.228s

OK


For point 1. above it is sufficient to just input the file name (f.ex. testfile.txt) if running program from the same folder as the file is in.
For point 4. above it is important to use the exact same format as shown in braces f.ex. - /home/user/ not f.ex. /home/user - as then, in the latter case, using the file example above, the program would try to place the file in /home/usertestfile.txt

#======================================================================================================



