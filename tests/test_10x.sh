#!/bin/bash

for item in `ls tests/functional | grep .py | grep -v __init__`; do
    if [ -f "tests/functional/$item" ]; then
        for count in `seq 10`; do

            echo "[ $count ]: $item"
            python3 -m unittest "tests/functional/$item"
        done
        read -p 'Continue? Y/N> ' CONTINUE
        case $CONTINUE in
            'y'|'Y')
                echo "[ NEXT ] - $count + 1"
                ;;
            'n'|'N')
                echo "[ STOP ] - $count"
                exit
                ;;
            *)
                echo "[ NEXT ] - $count + 1"
                ;;
        esac
    fi
done
