#!/bin/bash
# Script to convert markdown to docx using pandoc
# Usage: ./md_to_docx.sh /Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/README.md


# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Error: No input file specified"
    echo "Usage: ./md2docx.sh input.md"
    exit 1
fi

# Get the input filename and create output filename by replacing .md with .docx
input_file=$1
output_file="${input_file%.md}.docx"

# Run pandoc
pandoc "$input_file" -o "$output_file"

echo "Conversion complete: $output_file created"