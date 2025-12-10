import json
import requests
import time
import random
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
from src.models.node import AccountNode, EmailNode

class Scanner:
    def __init__(self, sites_file="data/sites.json"):
        self.sites = self._load_sites(sites_file)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
        ]

    def _get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }

    def _load_sites(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    # --- HELPER: URL CLEANER ---
    def _clean_url(self, url):
        """
        Strips unnecessary parts of the URL (like /status/123 or ?ref=...)
        to get the clean profile root.
        """
        try:
            # 1. Clean DuckDuckGo redirects
            if "uddg=" in url:
                start = url.find("uddg=") + 5
                end = url.find("&", start)
                if end != -1: url = unquote(url[start:end])
                else: url = unquote(url[start:])
            
            # 2. Clean Twitter/X status links
            # Converts https://twitter.com/User/status/123 -> https://twitter.com/User
            if "twitter.com" in url or "x.com" in url:
                if "/status/" in url:
                    url = url.split("/status/")[0]
                # Remove query parameters (?lang=en)
                url = url.split("?")[0]

            return url
        except:
            return url

    # --- SEARCH ENGINE PIVOT ---
    def _search_duckduckgo(self, query, expected_domain=None):
        """
        Scans TOP 5 results to find the correct profile link.
        """
        url = f"https://html.duckduckgo.com/html/?q={query}"
        try:
            time.sleep(1.5) # Slight delay for politeness
            resp = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                results = soup.find_all('a', class_='result__a')
                
                # Check the top 5 results, not just the first one
                for link in results[:5]:
                    raw_href = link['href']
                    clean_link = self._clean_url(raw_href)
                    
                    # If we are looking for a specific domain (like linkedin), verify it matches
                    if expected_domain:
                        if expected_domain in clean_link:
                            return clean_link
                    else:
                        # For generic searches, return the first valid one
                        return clean_link
        except Exception:
            pass
        return None

    # --- SPECIALIZED HANDLERS ---

    def _check_linkedin(self, username):
        # Query: site:linkedin.com/in/username
        # We pass 'linkedin.com/in' as expected_domain to filter out noise
        query = f"site:linkedin.com/in/{username}"
        return self._search_duckduckgo(query, expected_domain="linkedin.com/in")

    def _check_twitter(self, username):
        # 1. Try Nitter (Direct)
        try:
            nitter_url = f"https://xcancel.com/{username}"
            resp = requests.get(nitter_url, headers=self._get_headers(), timeout=5)
            if resp.status_code == 200 and "User not found" not in resp.text:
                return f"https://x.com/{username}"
        except:
            pass

        # 2. Search Pivot (Broadened)
        query = f"site:twitter.com/{username} OR site:x.com/{username}" 
        # We accept either domain
        result = self._search_duckduckgo(query, expected_domain="twitter.com")
        if not result:
            result = self._search_duckduckgo(query, expected_domain="x.com")
            
        return result

    def _check_tiktok(self, username):
        url = f"https://www.tiktok.com/@{username}"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            if response.status_code == 200:
                # Stronger check: Title tag usually contains "Name (@handle) | TikTok"
                if f"@{username}" in response.text:
                    return url
                elif "Couldn't find this account" in response.text:
                    return None
        except:
            pass
        return None

    def _check_facebook(self, username):
        url = f"https://www.facebook.com/{username}"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            if "This content isn't available" in response.text:
                return None
            if response.status_code == 200:
                return url
        except:
            pass
        return None

    # --- MAIN ENGINE ---

    def scan_target(self, username, graph, root_node):
        print(f"\n[*] Initializing Scan for target: {username}...")
        print(f"[*] Loaded {len(self.sites)} standard sites to scan.")
        print("[*] Engaging Search Pivot & Evasion modules...\n")

        # 1. Standard JSON Scans
        for site in self.sites:
            site_name = site['name']
            if site_name in ["Facebook", "Twitter", "X", "TikTok", "LinkedIn"]: continue

            url_template = site['url']
            target_url = url_template.format(username)

            try:
                response = requests.get(target_url, headers=self._get_headers(), timeout=5)
                if response.status_code == 200:
                    found_node = self._register_hit(graph, root_node, username, site_name, target_url)
                    if site_name == "GitHub":
                        self.extract_github_email(username, graph, found_node)
            except:
                pass
            time.sleep(0.5)

        # 2. Hard Target Scans
        
        # LinkedIn
        li = self._check_linkedin(username)
        if li: self._register_hit(graph, root_node, username, "LinkedIn", li)
        else: print("[-] LinkedIn: Not found (or unindexed).")

        # X (Twitter)
        x = self._check_twitter(username)
        if x: self._register_hit(graph, root_node, username, "X (Twitter)", x)
        else: print("[-] X (Twitter): Not found.")

        # Facebook
        fb = self._check_facebook(username)
        if fb: self._register_hit(graph, root_node, username, "Facebook", fb)
        else: print("[-] Facebook: Not found or Protected.")
        
        # TikTok
        tt = self._check_tiktok(username)
        if tt: self._register_hit(graph, root_node, username, "TikTok", tt)
        else: print("[-] TikTok: Not found.")

    def _register_hit(self, graph, root_node, username, site_name, url):
        print(f"[+] FOUND: {site_name} -> {url}")
        new_account = AccountNode(username, site_name, url, source="Scanner")
        graph.add_node(new_account)
        graph.add_edge(root_node, new_account, f"has_account_on_{site_name}")
        return new_account

    def extract_github_email(self, username, graph, parent_node):
        print(f"[*] Pivoting: Scanning GitHub profile for emails...")
        api_url = f"https://api.github.com/users/{username}"
        headers = self._get_headers()
        found_email = None
        source = "Unknown"
        
        try:
            resp = requests.get(api_url, headers=headers)
            if resp.status_code == 200 and resp.json().get("email"):
                found_email = resp.json().get("email")
                source = "GitHub Profile"
            
            if not found_email:
                events_url = f"https://api.github.com/users/{username}/events/public"
                events = requests.get(events_url, headers=headers).json()
                if isinstance(events, list):
                    for event in events:
                        if event["type"] == "PushEvent":
                            for commit in event.get("payload", {}).get("commits", []):
                                email = commit.get("author", {}).get("email")
                                if email and "noreply" not in email:
                                    found_email = email
                                    source = "GitHub Commit History"
                                    break
                        if found_email: break

            if found_email:
                print(f"[!] BINGO! Found email via {source}: {found_email}")
                email_node = EmailNode(found_email, source=source)
                graph.add_node(email_node)
                graph.add_edge(parent_node, email_node, "leaked_via_code")
            else:
                print("[-] No email found in Profile OR Commits.")
        except:
            pass
