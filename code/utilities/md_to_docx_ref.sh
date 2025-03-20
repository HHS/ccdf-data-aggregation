#!/bin/bash
# Script to convert markdown to docx using pandoc
# Usage: ./md_to_docx_ref.sh /Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/README.md /Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/references/pandoc_reference_scope.docx

# Check if input file is provided
if [ $# -lt 1 ]; then
    echo "Error: No input file specified"
    echo "Usage: ./md_to_docx.sh input.md [reference.docx]"
    exit 1
fi

# Get the input filename
input_file=$1

# Set default reference document or use the one provided
reference_doc="${2:-/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/references/pandoc_reference_scope.docx}"

# Create output filename by replacing .md with .docx
output_file="${input_file%.md}.docx"

# Check if reference document exists
if [ ! -f "$reference_doc" ]; then
    echo "Warning: Reference document '$reference_doc' not found."
    echo "Converting without reference styling..."
    pandoc "$input_file" -o "$output_file"
else
    # Run pandoc with reference document
    pandoc "$input_file" --reference-doc="$reference_doc" -o "$output_file"
    echo "Conversion complete with reference styling: $output_file created"
fi

echo "Conversion complete: $output_file created"