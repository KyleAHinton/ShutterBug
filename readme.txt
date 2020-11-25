This is the ShutterBug class project for CS 324 
Team Members:
Paul Wells
Kyle Hinton
Walid Muhammad 
Somayyeh Kamyab

To install the project clone the repository to a directory.

For Linux-Ubuntu users:
	Make the install.sh file in the main directory editable. (chmod +x install.sh)
	Run the install.sh file (requires sudo privledges!).
	Should be installed with all dependencies! To run you can use the launch.sh file once it is made executable

For Windows or other linux distros:
	Install python3
	Install mysql server
	Install npm
	Install pipenv with a pip install
	
	Once those are installed run the following sql to create the database.
	CREATE DATABASE Shutterbug;CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
	GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
	FLUSH PRIVILEGES;
	
	Then navigate to shutterbug main directory and run "pipenv run pipenv sync"
	Afterwards run "pipenv run python backend\manage.py migrate"
	Then navigate to the shutterbug folder inside of the main folder
	Make sure there is no file called "node_modules" if there is, delete it
	then run "npm install"
	That should conclude the install process
	
	To run it open two terminals and navigate one to Shutterbug. in that terminal run "pipenv run python backend\manage.py runserver"
	Then open the other terminal to Shutterbug\shutterbug and run "npm run serve"
	It should open a website on localhost:8080
	