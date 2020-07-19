#!/bin/bash -e

#navigate to right folder
function pusher_of_page(){
cd ../dijkstrar.github.io/ &&
git add . &&
git commit -m "Automatically push changes to github pages of generated plots" &&
echo "Pushing data to remote server!!!" &&
git push -u origin master &&
echo "Done!"
}
pusher_of_page

#https://stackoverflow.com/questions/16709404/how-to-automate-the-commit-and-push-process-git
