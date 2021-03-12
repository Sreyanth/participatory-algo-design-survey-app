echo "Running pip freeze"
pip freeze > requirements.txt

echo "Here are the requirements:"
echo "---- START ----"
echo

cat requirements.txt

echo
echo "----- END -----"
