FROM python:3.8

WORKDIR /mydir

COPY . .

RUN chmod +x /mydir/SCPTestCase.py

RUN pip install pexpect
RUN pip install paramiko

CMD python3 /mydir/SCPTestCase.py
