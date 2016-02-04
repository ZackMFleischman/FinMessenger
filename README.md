# FinMessenger
Command line tool to quickly send emails/commands to [Fin](https://www.getfin.com/) via your Gmail account.

## Usage
`python fin.py "Message Body" -s "Message Subject"`


The `-s [Message subject]` is optional, and the subject will be auto-filled if left out.

## Setup
You need to setup a project on the Google Developers Console and download some credentials after enabling the Gmail API for that project.

After you download the `client_secret.json` (Application Name should be "FinMessenger"), stick it in your repo folder and run the program with a test message. This should generate credentials for you (via opening your browser and asking for permission).

You then need to create an `emails.txt` file with two emails in the form
```
from@gmail.com
to@gmail.com
```
and stick it in your repo home directory as well.

That should do it.
