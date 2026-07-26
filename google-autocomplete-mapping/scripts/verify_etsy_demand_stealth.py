#!/usr/bin/env python3
"""
Etsy Demand & Supply Verification CLI Tool (Stealth Mode)
Uses exported browser JSON cookies (specifically datadome) to bypass 
DataDome protection and scrape Etsy listing counts programmatically.
"""

import argparse
import urllib.request
import urllib.parse
import json
import re
import sys
import os

# ANSI Colors for gorgeous console formatting
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Default User-Agent to match typical Chrome export
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def load_cookies(cookie_file):
    if not os.path.exists(cookie_file):
        print(f"{BOLD}{YELLOW}Warning:{RESET} Cookie file '{cookie_file}' not found.")
        return None
        
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies_data = json.load(f)
        
        cookie_pairs = []
        if isinstance(cookies_data, list):
            # List format: [{"name": "datadome", "value": "value"}, ...]
            for c in cookies_data:
                name = c.get('name')
                value = c.get('value')
                if name and value:
                    cookie_pairs.append(f"{name}={value}")
        elif isinstance(cookies_data, dict):
            # Key-Value dictionary format: {"datadome": "value"}
            for name, value in cookies_data.items():
                cookie_pairs.append(f"{name}={value}")
                
        cookie_header = "; ".join(cookie_pairs)
        return cookie_header
    except Exception as e:
        print(f"{BOLD}{YELLOW}Error loading cookies:{RESET} {e}")
        return None

def fetch_google_suggestions(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={encoded_query}"
    
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data[1]
    except Exception as e:
        print(f"Error fetching suggestions for '{query}': {e}")
    return []

def fetch_etsy_supply(phrase, cookie_header, user_agent):
    # Clean 'etsy' out of the search query to check Etsy's internal catalog supply
    clean_query = phrase.replace('etsy', '').strip()
    encoded_query = urllib.parse.quote(clean_query)
    url = f"https://www.etsy.com/search?q={encoded_query}"
    
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    if cookie_header:
        headers["Cookie"] = cookie_header
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8')
            
            # Find listing count: look for JSON metadata or clean text results
            # Etsy search result count standard format: e.g. "1,234 results" or "12,345 items"
            match = re.search(r'([\d,]+)\s+results', html, re.IGNORECASE)
            if match:
                # Remove commas and convert to int
                return int(match.group(1).replace(',', ''))
                
            # Alternative: check for total_results in JS objects
            match_json = re.search(r'"total_results":\s*(\d+)', html)
            if match_json:
                return int(match_json.group(1))
                
            # Fallback regex patterns
            match_items = re.search(r'([\d,]+)\s+items', html, re.IGNORECASE)
            if match_items:
                return int(match_items.group(1).replace(',', ''))
                
            return "Regex failed"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "403 Blocked (Cookie Expired or Flagged)"
        return f"HTTP {e.code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
        
    parser = argparse.ArgumentParser(description="Etsy Demand & Supply Auditor (Stealth Bypass)")
    parser.add_argument("keyword", type=str, help="The seed keyword (e.g., 'budget planner')")
    parser.add_argument("--cookies", type=str, default="etsy_cookies.json", help="Path to Etsy JSON cookies file")
    parser.add_argument("--user-agent", type=str, default=DEFAULT_USER_AGENT, help="User-Agent string matching browser cookie export")
    parser.add_argument("--limit", type=int, default=5, help="Number of keywords to verify (lower limits protect cookie life)")
    
    args = parser.parse_args()
    seed = args.keyword.strip()
    
    print(f"\n{BOLD}{BLUE}=================================================================={RESET}")
    print(f"{BOLD}{BLUE}   ESTEALTH DEMAND & SUPPLY AUDITOR (DataDome Bypass Activated)   {RESET}")
    print(f"{BOLD}{BLUE}=================================================================={RESET}")
    print(f"Seed Keyword: {BOLD}{YELLOW}'{seed}'{RESET}")
    print(f"Using Cookies: {BOLD}{args.cookies}{RESET}\n")
    
    cookie_header = load_cookies(args.cookies)
    if not cookie_header:
        print(f"{BOLD}{YELLOW}Note:{RESET} Proceeding WITHOUT cookies (expect 403 blocks on Etsy search supply fetches).")
    
    # Generate variations
    variations = [
        f"etsy {seed}",
        f"{seed} etsy",
        f"{seed} template etsy",
        f"{seed} spreadsheet etsy",
    ]
    
    all_suggestions = {}
    print(f"1. Gathering demand trends from Google Autocomplete...")
    for var in variations:
        suggs = fetch_google_suggestions(var)
        for idx, sug in enumerate(suggs):
            score = 10 - idx
            if sug in all_suggestions:
                all_suggestions[sug] += score
            else:
                all_suggestions[sug] = score
                
    sorted_suggestions = sorted(all_suggestions.items(), key=lambda x: x[1], reverse=True)
    if not sorted_suggestions:
        print(f"{BOLD}{YELLOW}No search trends detected.{RESET}")
        return
        
    targets = sorted_suggestions[:args.limit]
    
    print(f"\n2. Querying live Etsy supply data (bypassing DataDome)...")
    results_table = []
    
    for idx, (phrase, score) in enumerate(targets):
        sys.stdout.write(f"  Auditing catalog for: '{phrase}'... ")
        sys.stdout.flush()
        supply = fetch_etsy_supply(phrase, cookie_header, args.user_agent)
        
        if isinstance(supply, int):
            sys.stdout.write(f"{GREEN}done ({supply} listings found){RESET}\n")
            # Calculate ratio: score (Demand indicator) / supply (Competition index) * 1000
            # Higher score = better opportunity
            ratio = round((score / supply) * 1000, 4) if supply > 0 else 999.0
        else:
            sys.stdout.write(f"{YELLOW}failed ({supply}){RESET}\n")
            ratio = "N/A"
            
        results_table.append({
            "phrase": phrase,
            "demand": score,
            "supply": supply,
            "ratio": ratio
        })
        
    print(f"\n{BOLD}{CYAN}------------------------------------------------------------------------------------{RESET}")
    print(f"{BOLD}{CYAN}                      DEMAND / SUPPLY AUDIT REPORT                                  {RESET}")
    print(f"{BOLD}{CYAN}------------------------------------------------------------------------------------{RESET}")
    header = f"{'Rank':<5} | {'Search Phrase':<30} | {'Demand Score':<12} | {'Listing Supply':<15} | {'Opportunity Ratio (High = Best)'}"
    print(f"{BOLD}{header}{RESET}")
    print("-" * 88)
    
    for idx, res in enumerate(results_table):
        phrase = res["phrase"]
        demand = f"{res['demand']} pts"
        
        if isinstance(res["supply"], int):
            supply = f"{res['supply']:,}"
            ratio_val = res["ratio"]
            if ratio_val > 1.0:
                ratio_str = f"{BOLD}{GREEN}{ratio_val}{RESET}"
            elif ratio_val > 0.1:
                ratio_str = f"{YELLOW}{ratio_val}{RESET}"
            else:
                ratio_str = f"{ratio_val}"
        else:
            supply = f"{YELLOW}{res['supply']}{RESET}"
            ratio_str = "N/A"
            
        print(f"{idx+1:<5} | {phrase:<30} | {demand:<12} | {supply:<15} | {ratio_str}")
        
    print("-" * 88)
    print(f"{BOLD}{BLUE}===================================================================================={RESET}\n")

if __name__ == "__main__":
    main()
