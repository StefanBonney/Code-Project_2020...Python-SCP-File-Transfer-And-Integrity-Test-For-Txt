import unittest
import pexpect
import os
import subprocess
import sys
import paramiko


# DESCRIPTION
# Script that sends a file via scp to remote host
# variables either defined in the source code or defined when prompted for user input, 
# Can be used f.ex. for sending configuration files or script files, and checking for the file integrity once transferred

# Input the file/folder variables here. If they are empty user will be prompted for them during program execution.
# SOURCE
sourceFileLocation = "/home/ubu1-u/tf1.txt" # f.ex. "/home/user/testfile.txt"
# DESTINATION
destinationRemoteAddress = "ubu2-u@192.168.43.140"  # f.ex. user@localhost    : 
destinationFolderPath = "/home/ubu2-u/Desktop/" # f.ex. /home/user/  
destinationFileName = "tf1.txt" # f.ex. transferred.txt  
#PASSWORD
destinationPassw = "hattis2"


class SCPTestCase(unittest.TestCase):

    # Points [1]-[5] below are the functions that the test goes through in chronological order to complete the transfer and perform the test
    #****************************************************************************************[test_scp_file_transfer][MAIN]
    def test_scp_file_transfer(self): 
      
       
        # SET UP, MAKE TRANSFER FOR THE TEST, GATHER TEST RESULT

        #[1] Get the location of the file to be transferred, and the content to be used for matching later. 
        #    If the location variable is not set the user will be prompted for this. 
        sourceLocation, originalContent = get_source_file(sourceFileLocation)
    

        #[2] Get the destination remote location
        remoteUser, remoteIp = set_remote_address(destinationRemoteAddress)
        remoteAddress = remoteuser + "@" + remoteIP

        #[3] Get the passowrd for the remote machine so that connection can be established using that
        passw = set_password(destinationPassw)

        #[4] Get the destination that the file is to be transferred to and the name of the file once it has been transferred.
        #    If the variables for destination folder / name have not been assigned in the code, the user will be prompted for these.
        #    A test is performed to check that the location specified exists, otherwise the location is created.
        destinationPath = set_destination_path_variables(destinationFolderPath, destinationFileName, remoteUser, remoteIp, passw)

        #[5] Using the variables for source and destination location gathered above, the SCP command is performed 
        transfer_file_with_scp(remoteAddress, sourceLocation, destinationPath, passw)

        #[6] Once the file has been transferred, the content of the file is now set into the variable transferredContent
        transferredContent = get_transferred_content(destinationPath, user, ip, passw)

        #[7] Compare that the string content of the original and transferred file. Returns True if they are the same. 
        comparisonResult = perform_comparison(originalContent, transferredContent) 
      

        # PERFORM THE TEST        #[2] Get the destination that the file is to be transferred to and the name of the file once it has been transferred.
 
        self.assertTrue(comparisonResult) 

    #**************************************************************************************** 



#*--------------------------------------------------------------------------------------*[1][get_source_file]
def get_source_file(sourceFileLocation):
    Print("1. Getting information on source file")

    if sourceFileLocation:
        return sourceFileLocation, read_file_to_string(sourceFileLocation)
    else: 
        uInput = raw_input("Enter source file location (f.ex. /home/user/testfile.txt): ")
        return uInput, read_file_to_string(uInput)
#*--------------------------------------------------------------------------------------*

#*--------------------------------------------------------------------------------------*[2][set_remote_address]
def set_remote_address(destinationRemoteAddress):
    Print("2. Getting information on remote address")

    if destinationRemoteAddress:
    	user, ip = destinationRemoteAddress.split("@")
        return user, ip
    else: 
        uInput_Remote = raw_input("The remote address has not been determined, please input the name (f.ex. user@localhost): ") 
        user, ip = uInput_Remote.split("@")
        return user, ip
#*--------------------------------------------------------------------------------------*

#*--------------------------------------------------------------------------------------*[3][set_password]
def set_password(destinationPassw):
	    Print("3. Getting information on password")

    if destinationPassw:
        return destinationPassw
    else: 
        uInput_Passw = raw_input("The password for remote host has not been determined, please input the password: ") 
        return uInput_Passw
#*--------------------------------------------------------------------------------------*

#*--------------------------------------------------------------------------------------*[4][set_destination_path_variables]
def set_destination_path_variables(destinationFolderPath, destinationFileName, remoteUser, remoteIp, passw):
	    Print("4. Getting information on destination path variables")
        
    # DESTINATION FOLDER LOCATION ASSIGNED TO VARIABLE
    if destinationFolderPath:
    	# check that the folder location exists, otherwise inform user that it does not exist and ask if wants it to be created, or exit
        filePath = destinationFolderPath
        command1 = 'if test -d {filePath}; then echo "exist"; else echo "not exist"; fi'.format(filePath=filePath)
        valueToMatch = "exist" 
    	testForFolderPath = perform_ssh_command_return_boolean(remoteUser, remoteIp, passw, command1, valueToMatch)   	
        if not testForFolderPath:
            uInput = raw_input("The path does not exist, would you like it to be created? Exit upon chosing no (y/n)")
            if uInput.lower() == "y":
            	command2 = "mkdir {filePath}".format(filePath=filePath)
            	perform_ssh_command_return_boolean(remoteUser, remoteIp, passw, command2, valueToMatch)   	
            if uInput.lower() == "n":
                sys.exit()
        # check that a name for the file to be transferred has been been assigned to the variable, otherwise ask user to input
        if destinationFileName:
            return filePath + destinationFileName
        else:
            uInput_Name = raw_input("A name for the transferred file has not been determined, please input the name (f.ex. transferred.txt): ") 
            return filePath + uInput_Name
        
        
    # NO DESTINATION FOLDER LOCATION ASSIGNED TO VARIABLE
    else: 
        uInput_Path = raw_input("A path to transfer the file to has not been assigned, please input the directory path: (f.ex. /home/user/)")
    	# check that the folder location exists, otherwise inform user that it does not exist and ask if wants it to be created, or exit
        filePath = uInput_Path
        command1 = 'if test -d {filePath}; then echo "exist"; else echo "not exist"; fi'.format(filePath=filePath)
        valueToMatch = "exist" 
    	testForFolderPath = perform_ssh_command_return_boolean(remoteUser, remoteIp, passw, command1, valueToMatch)   	
        if not testForFolderPath:
            uInput = raw_input("The path does not exist, would you like it to be created? Exit upon chosing no (y/n)")
            if uInput.lower() == "y":
            	command2 = "mkdir {filePath}".format(filePath=filePath)
            	perform_ssh_command_return_boolean(remoteUser, remoteIp, passw, command2, valueToMatch)   	
            if uInput.lower() == "n":
                sys.exit()
        # check that a name for the file to be transferred has been been assigned to the variable, otherwise ask user to input
        if destinationFileName:
            return filePath + destinationFileName
        else:
            uInput_Name = raw_input("A name for the transferred file has not been determined, please input the name (f.ex. transferred.txt: ") 
            return filePath + uInput_Name

#*---------------------------------------------------------------------------------------*


#*---------------------------------------------------------------------------------------*[5][transfer_file_with_scp]
def transfer_file_with_scp(remoteAddress, sourceLocation, destinationPath, passw):
    print("5. All the necessary variables have been set to perform the transfer, commencing transfer")

	source = sourceLocation
	destination = remoteAddress + ":" + destinationPath

	child = pexpect.spawn('scp {source} {destination}'.format(source=source,destination=destination))

	while True:
		ind = child.expect([r"to continue connecting \(yes/no\)\? ", "password:"], timeout=10)
		if ind == 0:
			child.send("yes\n")
		elif ind == 1:
			child.send(passw + "\n")
                break

        # Wait for output to finish.
        pp.expect(pexpect.EOF)
#*---------------------------------------------------------------------------------------*   
      

#*---------------------------------------------------------------------------------------*[6][get_transferred_content] 
def get_transferred_content(destinationPath, user, ip, passw):
    print("6. Getting the transferred content")

    command = "var=$( cat {destinationPath} )"
    return perform_ssh_command_return_string(user, ip, passw, command)
#*---------------------------------------------------------------------------------------* 


#*---------------------------------------------------------------------------------------*[7][perform_comparison] 
def perform_comparison(originalContent, transferredContent):
    print("7. Performing comparison")

    if originalContent == transferredContent:
        return True
    else:
        return False
#*---------------------------------------------------------------------------------------*



#========================================================================================[HELPER FUNCTIONS]

# HELPER 1
def read_file_to_string(path):
    return open(path).read()

# HELPER 2
def perform_ssh_command_return_boolean(user, ip, passw, command, valueToMatch):    
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    com=command
    client.connect(ip, '22', username='user', password=passw)
    output=""
    stdin, stdout, stderr = client.exec_command(com)

    print("ssh succuessful. Closing connection")
    stdout=stdout.readlines()
    client.close()
    print("Connection closed")

    #print(stdout)
    print(com)
    for line in stdout:
        output=output+line
    if output!="":
        splitOutput = output.split("\n")
        print(splitOutput[0])
        compare1 = valueToMatch
        compare2 = splitOutput[0]
        if compare1 == compare2:
    	   return True
        else:
        return False

# HELPER 3
def perform_ssh_command_return_string(user, ip, passw, command):    
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    com=command
    client.connect(ip, '22', username='user', password=passw)
    output=""
    stdin, stdout, stderr = client.exec_command(com)

    print("ssh succuessful. Closing connection")
    stdout=stdout.readlines()
    client.close()
    print("Connection closed")

    print(stdout)
    print(com)
    for line in stdout:
        output=output+line
    if output!="":
        #print(output)
        return output
    else:
        print("There was no output for this command")

#========================================================================================


if __name__ == '__main__':
     unittest.main()





