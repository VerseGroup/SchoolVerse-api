#!/bin/bash

while getopts ":ft:" option; do
    case $option in
        f)
            echo "Option: Reset Flik"
            python3 lib/resets/reset_flik.py
            ;;
        t)
            echo "Option: Reset Tasks"
            python3 lib/resets/reset_tasks.py
            ;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit
            ;;
    esac
done

echo "reset complete"