#!/bin/bash
#QF 90, 80, 50, 20, 10 and 5. 
echo "filename: $2"
echo "QF: 90"
python3 main.py c $1 90 $2
python3 main.py d $1 90 $2
python3 main.py p $1 90 $2
echo "QF: 80"
python3 main.py c $1 80 $2
python3 main.py d $1 80 $2
python3 main.py p $1 80 $2
echo "QF: 50"
python3 main.py c $1 50 $2
python3 main.py d $1 50 $2
python3 main.py p $1 50 $2
echo "QF: 20"
python3 main.py c $1 20 $2
python3 main.py d $1 20 $2
python3 main.py p $1 20 $2
echo "QF: 10"
python3 main.py c $1 10 $2
python3 main.py d $1 10 $2
python3 main.py p $1 10 $2
echo "QF: 5"
python3 main.py c $1 5 $2
python3 main.py d $1 5 $2
python3 main.py p $1 5 $2
