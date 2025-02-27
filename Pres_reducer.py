# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 23:05:07 2025

@author: KateClancy
"""

import sys

def reducer():
    
    current_president = None
    total_valence = 0
    count = 0

    for line in sys.stdin:
        # Parse the input (expected format: "president_name \t sentiment_score")
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue  # Skip malformed lines

        president, valence_str = parts
        try:
            valence = float(valence_str)
        except ValueError:
            continue  # Skip if valence is not a valid float

        # Check if we're still processing the same president
        if current_president and current_president != president:
            # Emit result for previous president
            average_valence = total_valence / count if count > 0 else 0
            print(f"{current_president}\t{average_valence:.4f}")
            
            # Reset for new president
            total_valence = 0
            count = 0

        # Update tracking variables
        current_president = president
        total_valence += valence
        count += 1

    # Emit last president's result
    if current_president:
        average_valence = total_valence / count if count > 0 else 0
        print(f"{current_president}\t{average_valence:.4f}")

# Run the reducer if script is executed directly
if __name__ == "__main__":
    reducer()