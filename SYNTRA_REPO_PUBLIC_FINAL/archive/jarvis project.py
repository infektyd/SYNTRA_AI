# Jarvis Web Scanner Integration (Passive Learning Module with Curiosity and Reasoning + Toggles + Diag Hook)

from collections import defaultdict
import random
import threading
import time
import json
import csv
import sys
import os
import timeit

# Ensure VSCode compatibility
os.environ['PYTHONIOENCODING'] = 'utf-8'

class SettingsManager:
    def __init__(self):
        self.settings = {
            "learning_enabled": True,
            "curiosity_enabled": True,
            "hypothesis_enabled": True,
            "idle_scanning_enabled": True
        }

    def toggle(self, key, value: bool):
        if key in self.settings:
            self.settings[key] = value

    def get(self, key):
        return self.settings.get(key, False)

class WebScanner:
    def __init__(self, allow_unrestricted=True, require_download_approval=True):
        self.allow_unrestricted = allow_unrestricted
        self.require_download_approval = require_download_approval
        self.learned_terms = set()
        self.topic_interest = defaultdict(int)
        self.curiosity_log = []
        self.hypotheses = []
        self.settings = SettingsManager()
        self.debug_timings = defaultdict(float)

    def timed(func):
        def wrapper(self, *args, **kwargs):
            start = timeit.default_timer()
            result = func(self, *args, **kwargs)
            end = timeit.default_timer()
            self.debug_timings[func.__name__] += end - start
            return result
        return wrapper

    @timed
    def scan_page(self, html_text):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text().lower()
        keywords = self.extract_keywords(text)
        if self.settings.get("learning_enabled"):
            self.learned_terms.update(keywords)
            if self.settings.get("curiosity_enabled"):
                self.update_interest(keywords)
            if self.settings.get("hypothesis_enabled"):
                self.generate_hypotheses(keywords)
        return keywords

    @timed
    def extract_keywords(self, text):
        import re
        words = re.findall(r'\b[a-zA-Z]{5,}\b', text)
        filtered = [word for word in words if word not in self.learned_terms]
        return set(filtered)

    @timed
    def update_interest(self, keywords):
        for word in keywords:
            self.topic_interest[word] += 1
        top = sorted(self.topic_interest.items(), key=lambda x: -x[1])[:5]
        self.curiosity_log.append([t[0] for t in top])

    @timed
    def generate_hypotheses(self, keywords):
        repairs = ["inspect", "repair", "replace", "test"]
        hypothesis_set = []
        for cause in keywords:
            for effect in keywords:
                if cause != effect:
                    hypothesis_set.append(f"If {cause} occurs, then {effect} may result.")
            for repair in repairs:
                hypothesis_set.append(f"To fix {cause}, you may need to {repair} the component.")
        self.hypotheses.extend(hypothesis_set[-5:])

    def get_hypotheses(self):
        return self.hypotheses[-5:]

    def prioritized_links(self, soup, current_url):
        from urllib.parse import urljoin
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            if any(topic in href.lower() for topic in self.top_interests()):
                links.insert(0, (full_url, 0))
            else:
                links.append((full_url, 0))
        return links

    def top_interests(self):
        return sorted(self.topic_interest, key=self.topic_interest.get, reverse=True)[:5]

    def decay_interest(self):
        for key in list(self.topic_interest):
            self.topic_interest[key] *= 0.9
            if self.topic_interest[key] < 1:
                del self.topic_interest[key]

    def crawl(self, url, depth=2):
        import requests
        visited = set()
        to_visit = [(url, 0)]

        while to_visit:
            current_url, level = to_visit.pop(0)
            if current_url in visited or level > depth:
                continue
            visited.add(current_url)
            try:
                response = requests.get(current_url, timeout=5)
                if response.ok:
                    soup = self._get_soup(response.text)
                    self.scan_page(response.text)
                    if self.allow_unrestricted:
                        prioritized = self.prioritized_links(soup, current_url)
                        to_visit.extend([(u, level + 1) for u, _ in prioritized])
                self.decay_interest()
            except Exception:
                continue

    def _get_soup(self, html):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, 'html.parser')

    def export_learned_terms(self):
        return sorted(list(self.learned_terms))

    def export_interest_history(self):
        return self.curiosity_log

    def get_current_keywords(self):
        return list(self.learned_terms)

    def get_top_topics(self):
        return self.top_interests()

    def get_debug_timings(self):
        return dict(self.debug_timings)

    def respond_to_query(self):
        latest = self.curiosity_log[-1] if self.curiosity_log else []
        return {
            "learned": list(self.learned_terms)[-10:],
            "current_interests": latest,
            "latest_hypotheses": self.get_hypotheses()
        }

    def save_to_json(self, filename="scanner_memory.json"):
        with open(filename, 'w') as f:
            json.dump({
                "learned_terms": list(self.learned_terms),
                "interest_history": self.curiosity_log,
                "hypotheses": self.hypotheses,
                "timings": self.get_debug_timings()
            }, f, indent=2)

    def save_to_csv(self, filename="scanner_memory.csv"):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Learned Terms"])
            for term in sorted(self.learned_terms):
                writer.writerow([term])
            writer.writerow([])
            writer.writerow(["Curiosity Log"])
            for row in self.curiosity_log:
                writer.writerow(row)
            writer.writerow([])
            writer.writerow(["Hypotheses"])
            for line in self.hypotheses:
                writer.writerow([line])
            writer.writerow([])
            writer.writerow(["Timing Summary"])
            for k, v in self.debug_timings.items():
                writer.writerow([k, round(v, 3)])

# Integration point for Jarvis-lite
web_scanner = WebScanner()

def analyze_with_scanner(message):
    learned_terms = web_scanner.get_current_keywords()
    match = [term for term in message.lower().split() if term in learned_terms]
    if match:
        print("[DIAG ENHANCEMENT] Matched learned terms:", match)
        print("[DIAG ENHANCEMENT] Hypotheses based on recent learning:")
        for h in web_scanner.get_hypotheses():
            print(" -", h)

# Idle scanning thread (charm.li entrypoint)
def idle_scan():
    while True:
        try:
            if web_scanner.settings.get("idle_scanning_enabled"):
                print("[IDLE SCAN] Crawling charm.li root...")
                web_scanner.crawl("https://charm.li", depth=1)
                print("[IDLE SCAN] Learned:", web_scanner.export_learned_terms()[-5:])
        except Exception as e:
            print("[IDLE SCAN ERROR]", str(e))
        time.sleep(1800)  # 30 minutes

# Background scan thread launch
try:
    idle_thread = threading.Thread(target=idle_scan, daemon=True)
    idle_thread.start()
except RuntimeError as e:
    print("[THREAD ERROR]", e)

# Jarvis command trigger hook
if __name__ == "__main__":
    print("[TEST] Initiating WebScanner test mode...")
    try:
        result = web_scanner.scan_page("""
            <html>
                <body>
                    <h1>Hydraulic Pump Failure Symptoms</h1>
                    <p>Common causes include fluid contamination, overheating, or mechanical damage to seals.</p>
                    <p>Repair involves pressure testing and inspecting return lines and valve assemblies.</p>
                </body>
            </html>
        """)
        print("[LEARNED TERMS]", web_scanner.export_learned_terms())
        print("[CURIOSITY LOG]", web_scanner.export_interest_history())
        print("[HYPOTHESES]", web_scanner.get_hypotheses())
        print("[TIMING SUMMARY]", web_scanner.get_debug_timings())
    except Exception as e:
        print("[SCAN ERROR]", e)