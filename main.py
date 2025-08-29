from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import os, re

app = FastAPI()


FULL_NAME = os.getenv("FULL_NAME", "prakarshi baryas")
DOB_DDMMYYYY = os.getenv("DOB_DDMMYYYY", "15022004")
EMAIL = os.getenv("EMAIL", "prakarshibarya@gmail.com")
ROLL_NUMBER = os.getenv("ROLL_NUMBER", "22BCE0473")


class InputModel(BaseModel):
    data: List[str]

int_pat = re.compile(r"^[+-]?\d+$")
def is_int_str(s: str) -> bool: return bool(int_pat.fullmatch(s.strip()))

def alternating_caps_of_reversed(s: str) -> str:
    out, upper = [], True
    for ch in s[::-1]:
        if ch.isalpha():
            out.append(ch.upper() if upper else ch.lower())
            upper = not upper
    return "".join(out)

#ui
@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>BFHL API Tester</title>
  <style>
    body{font-family:system-ui,Segoe UI,Arial;margin:24px;max-width:900px}
    textarea,pre{width:100%;box-sizing:border-box}
    button{padding:8px 14px;cursor:pointer;margin-top:8px}
    code{background:#f6f8fa;padding:2px 6px;border-radius:6px}
  </style>
</head>
<body>
  <h1>BFHL API Tester</h1>
  <p>Send a POST to <code>/bfhl</code> and see the response below.</p>

  <label>Input array JSON</label>
  <textarea id="input" rows="4">["a","1","334","4","R","$"]</textarea>
  <button onclick="run()">Send to /bfhl</button>

  <h3>Response</h3>
  <pre id="out">{}</pre>

<script>
async function run(){
  const arrText = document.getElementById('input').value;
  let data;
  try { data = JSON.parse(arrText); }
  catch(e){ document.getElementById('out').textContent = "Invalid JSON: " + e; return; }
  const resp = await fetch("/bfhl", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ data })
  });
  const text = await resp.text();
  try { document.getElementById('out').textContent = JSON.stringify(JSON.parse(text), null, 2); }
  catch { document.getElementById('out').textContent = text; }
}
</script>
</body>
</html>
"""
#api
@app.post("/bfhl")
def bfhl(payload: InputModel):
    raw_items = [str(x) for x in payload.data]

    even_numbers: List[str] = []
    odd_numbers: List[str] = []
    alphabets: List[str] = []
    special_chars: List[str] = []
    nums_for_sum: List[int] = []

    for item in raw_items:
        s = item.strip()
        if is_int_str(s):
            v = int(s)
            nums_for_sum.append(v)
            (even_numbers if abs(v) % 2 == 0 else odd_numbers).append(s)
        elif s.isalpha():
            alphabets.append(s.upper())
        else:
            special_chars.append(s)

    total_sum = str(sum(nums_for_sum))
    all_letters = "".join(alphabets)
    concat_string = alternating_caps_of_reversed(all_letters)

    return {
        "is_success": True,
        "user_id": f"{FULL_NAME.lower().replace(' ', '_')}_{DOB_DDMMYYYY}",
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_chars,
        "sum": total_sum,
        "concat_string": concat_string
    }
