cls

echo off
echo Beginning fundCoordinates tests > capture.txt
echo. >> capture.txt
python test_findCoordinates.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning findAddress tests >> capture.txt
echo. >> capture.txt
python test_findAddress.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo *********************** All Tests Complete *********************** >> capture.txt





echo on