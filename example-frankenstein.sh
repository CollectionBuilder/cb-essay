#!/bin/bash
# Example: Download and convert Frankenstein to markdown chapters

echo "Downloading Frankenstein from Project Gutenberg..."
wget -q https://www.gutenberg.org/files/84/84-0.txt -O frankenstein.txt

if [ $? -eq 0 ]; then
    echo "✓ Downloaded successfully"
    echo ""
    echo "Converting to markdown chapters..."
    python3 gutenberg_to_markdown.py frankenstein.txt --slug frankenstein --output ./books
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Conversion complete!"
        echo ""
        echo "View your chapters in: ./books/frankenstein/"
        echo "Open ./books/frankenstein/README.md for the chapter index"
    fi
else
    echo "✗ Download failed. Please download manually from:"
    echo "  https://www.gutenberg.org/files/84/84-0.txt"
    echo ""
    echo "Then run:"
    echo "  python3 gutenberg_to_markdown.py frankenstein.txt --slug frankenstein"
fi
