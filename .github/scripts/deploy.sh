sudo systemctl stop apptest.service
cd /home/johnpeel/app-engine-test/
git pull
sudo cp /home/johnpeel/app-engine-test/apptest.service /etc/systemd/system/apptest.service
sudo systemctl start apptest.service
