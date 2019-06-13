echo ""
echo "+--------------------+"
echo "|   Starting Tests   |"
echo "+--------------------+"
echo ""

test_file () {
  echo "> Testing : $1"
  python3 tests/$1.py
  echo "***"
}

test_file Auth
# test_file Load
# test_file Actions
test_file Tick

echo ""
echo "+--------------------+"
echo "|    Ending Tests    |"
echo "+--------------------+"
echo ""
