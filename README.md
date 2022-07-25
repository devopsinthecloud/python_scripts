What is this repository for?
This is a script which will simultaneously run an application in 4 docker environments, each in a separate terminal window, so that the developer could see all processes.
This program can be run on both MacOS and Linux, it will automatically detect your platform.
For Linux it will use Screen. For Mac just a Macos terminal.
Ports where the apps are running:
Admin: 3001, webpacker: 3037
Login: 1337, webpacker: 3035,
CF: 3000, webpacker: 3038,
CRM: 3002, webpacker: 3039
How do I get set up?
First of all you need to prepare npmrc by following this guide:
XXX
Also, we need to have the following installed:
npm (6.14.17)
nodejs (v14.19.3)
python3
pip3
google-cloud-sdk
If you are on MacOS, edit a file dirs.txt and put there full paths to the project directories:
for example:
/Users/Marinadin.Grin/repositories/remark-vp-admin/
/Users/Marinadin.Grin/repositories/remark-vp-crm/
/Users/Marinadin.Grin/repositories/remark-vp-cf/
/Users/Marinadin.Grin/repositories/remark-vp-login/remark-login/
Your script should be in the same directory as the dirs.file and project folders, it will loop through the list of project directories in this file.
NOTE:
If you are using Linux, the tmux version does not use the dirs file, but hardcoded paths.
So don't forget to check the folder names hardcoded in the def tmux (line 25), you might need to edit them if you have different project names.
In order to run the script you need to install dependencies listed in the requirements file.
I'm sure you know how to do it.
pip3 install -r requirements.txt
To launch a program, simply run
python3 env.py
