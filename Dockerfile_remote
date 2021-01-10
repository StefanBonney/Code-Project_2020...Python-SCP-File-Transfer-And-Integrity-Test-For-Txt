FROM python:3.8

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/StefanBonney/Python-SCP-File-Transfer-And-Integrity-Test-For-Txt.git

RUN mv /mydir/Python-SCP-File-Transfer-And-Integrity-Test-For-Txt/* .

RUN chmod +x /mydir/SCPTestCase.py

RUN pip install pexpect
RUN pip install paramiko

COPY . .
CMD python3 /mydir/SCPTestCase.py
