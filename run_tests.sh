python build.py testdb
echo "--- Starting Tests ---"
python3 tests.py testdb
echo "--- End of Tests ---"
rm testdb.sqlite
