message = 'GET /static/favicon.ico HTTP/1.1\r\nHost: localhost:8888\r\nConnection: keep-alive\r\nsec-ch-ua-platform: "Windows"\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36\r\nsec-ch-ua: "Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"\r\nsec-ch-ua-mobile: ?0\r\nAccept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: no-cors\r\nSec-Fetch-Dest: image\r\nReferer: http://localhost:8888/httpbin.org\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en,en-US;q=0.9\r\n\r\n'
x = message.partition('Referer: ')[2]
print(x)

headers = message.split('\r\n')
referer_header = [h for h in headers if h.lower().startswith('referer: ')]

print(referer_header)
