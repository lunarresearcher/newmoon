# Builds site/index.html (standalone, for your own domain) from src/page.html (the artifact source).
import pathlib, sys
root = pathlib.Path(__file__).parent
src = (root/"src/page.html").read_text()
head, body = src.split("<!-- /head -->", 1)
domain = sys.argv[1] if len(sys.argv) > 1 else "https://newmoon.tools"
meta = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#07090e">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="Newmoon · your number, off the lists">
<meta property="og:description" content="Six Grok Bots take your phone number and home address off 45 people-search sites and check again every new moon. Free.">
<meta property="og:url" content="{domain}/">
<meta property="og:image" content="{domain}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{domain}/og.png">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""
out = f"<!doctype html>\n<html lang=\"en\">\n<head>\n{meta}{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
(root/"site/index.html").write_text(out)
print("wrote site/index.html", len(out), "bytes")
(root/"site/docs.html").write_text((root/"src/docs.html").read_text())
print("wrote site/docs.html")
