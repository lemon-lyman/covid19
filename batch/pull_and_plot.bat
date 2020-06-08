cd C:/Users/Nick/workspace/COVID-19
git pull origin master
cd ../covid19/covid19
python main.py no_display
cd ..
git add .
git commit -m "auto fig commit"
git push origin master
cd batch
PAUSE