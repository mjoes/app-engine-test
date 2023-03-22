sudo systemctl stop apptest.service
cd /home/johnpeel/app-engine-test/
sudo git config --global --add safe.directory /home/johnpeel/app-engine-test
sudo git pull
sudo pip3 install --upgrade -r requirements.txt
sudo cp /home/johnpeel/app-engine-test/apptest.service /etc/systemd/system/apptest.service
sudo systemctl start apptest.service
