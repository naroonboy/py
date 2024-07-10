#!/bin/bash

# Define the time frame
start_time="2024-07-08 12:00:00"
end_time="2024-07-08 14:00:00"

# Source and destination files
source_file="application.log"
destination_file="error_log.txt"

# Extract lines with ERROR within the time frame
awk -v start="$start_time" -v end="$end_time" '
$0 ~ /ERROR/ && $0 >= start && $0 <= end
' $source_file > $destination_file
