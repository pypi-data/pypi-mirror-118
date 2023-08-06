import requests

def download_git(url,zip_name):


    with open(f"{zip_name}.zip","wb") as f:
        asil_url = url +"/archive/refs/heads/main.zip"
        r = requests.get(asil_url)
        f.write(r.content)