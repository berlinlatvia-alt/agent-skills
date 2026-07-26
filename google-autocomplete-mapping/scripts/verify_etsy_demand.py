#!/usr/bin/env python3
"""
Etsy & E-commerce Demand Verification CLI Tool
Queries Google Autocomplete for long-tail search intent and generates 
investigative deep links to bypass bot protections.
"""

import argparse
import urllib.request
import urllib.parse
import json
import sys

# ANSI Colors for gorgeous console formatting
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def fetch_suggestions(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                # Google autocomplete format: [query, [suggestions], [descriptions], ...]
                return data[1]
    except Exception as e:
        print(f"{BOLD}{YELLOW}Warning:{RESET} Error fetching suggestions for '{query}': {e}")
        return []
    return []

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Etsy & Google Autocomplete Demand Verification Tool")
    parser.add_argument("keyword", type=str, help="The seed keyword (e.g., 'budget planner', 'glowforge box')")
    parser.add_argument("--limit", type=int, default=10, help="Max results to display")
    
    args = parser.parse_args()
    seed = args.keyword.strip()
    
    print(f"\n{BOLD}{BLUE}=================================================================={RESET}")
    print(f"{BOLD}{BLUE}   E-COMMERCE DEMAND VERIFICATION ENGINE (Google Autocomplete)   {RESET}")
    print(f"{BOLD}{BLUE}=================================================================={RESET}")
    print(f"Seed Keyword: {BOLD}{YELLOW}'{seed}'{RESET}\n")
    
    # Generate variations to capture different buyer intents
    variations = [
        f"etsy {seed}",
        f"{seed} etsy",
        f"{seed} template etsy",
        f"{seed} spreadsheet etsy",
        f"{seed} digital download etsy"
    ]
    
    all_suggestions = {}
    
    print(f"Scanning search intent signals...")
    for var in variations:
        sys.stdout.write(f"  Fetching suggestions for: '{var}'... ")
        sys.stdout.flush()
        suggs = fetch_suggestions(var)
        sys.stdout.write(f"{GREEN}done ({len(suggs)} found){RESET}\n")
        
        for idx, sug in enumerate(suggs):
            # Rank suggestions: earlier suggestions in autocomplete list have higher search priority
            score = 10 - idx  # 1st suggestion gets 10 pts, 2nd gets 9, etc.
            if sug in all_suggestions:
                all_suggestions[sug] += score
            else:
                all_suggestions[sug] = score
                
    # Sort suggestions by combined priority score
    sorted_suggestions = sorted(all_suggestions.items(), key=lambda x: x[1], reverse=True)
    
    if not sorted_suggestions:
        print(f"\n{BOLD}{YELLOW}No suggestions found. Check your internet connection or try a broader seed keyword.{RESET}")
        return
        
    print(f"\n{BOLD}{CYAN}------------------------------------------------------------------{RESET}")
    print(f"{BOLD}{CYAN}   Top Verified Search Queries (Ranked by Autocomplete Priority)  {RESET}")
    print(f"{BOLD}{CYAN}------------------------------------------------------------------{RESET}")
    
    header = f"{'Rank':<5} | {'Search Phrase':<35} | {'Score':<5} | {'Action Links'}"
    print(f"{BOLD}{header}{RESET}")
    print("-" * 80)
    
    for idx, (phrase, score) in enumerate(sorted_suggestions[:args.limit]):
        # Encode for URLs
        encoded_phrase = urllib.parse.quote(phrase)
        trends_url = f"https://trends.google.com/trends/explore?q={encoded_phrase}&geo=US"
        etsy_url = f"https://www.etsy.com/search?q={urllib.parse.quote(phrase.replace('etsy', '').strip())}"
        
        # Format results
        rank_str = f"{idx+1}."
        score_str = f"{score} pts"
        
        print(f"{rank_str:<5} | {BOLD}{phrase:<35}{RESET} | {score_str:<5} | {BLUE}Trends:{RESET} {trends_url}")
        print(f"{' ':5} | {' ':35} | {' ':5} | {GREEN}Etsy Supply Check:{RESET} {etsy_url}")
        print("-" * 80)
        
    print(f"\n{BOLD}{YELLOW}Instructions for Auditing:{RESET}")
    print(f"1. Click the {BOLD}Trends link{RESET} to confirm seasonal interest, geographical demand, and multi-year trajectory.")
    print(f"2. Click the {BOLD}Etsy Supply Check link{RESET} to open your browser (bypassing DataDome scraping blocks).")
    print(f"   Note the total count of listing results (competition index) and review best-seller listings.")
    print(f"3. High Demand / Low Supply = Goldmine opportunity.")
    print(f"{BOLD}{BLUE}=================================================================={RESET}\n")

if __name__ == "__main__":
    main()
