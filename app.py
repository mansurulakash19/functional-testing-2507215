"""Small Flask site that runs the functions of target.py and shows the commit SHA."""
import os

from flask import Flask, jsonify, request

import runner

app = Flask(__name__)

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>target.py playground</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; background: #f4f6f8; color: #1d2733; }
  header { background: #1f3a5f; color: #fff; padding: 1.2rem 1.5rem; }
  header h1 { margin: 0 0 .3rem; font-size: 1.5rem; }
  header p { margin: 0; opacity: .85; font-size: .9rem; }
  main { display: grid; gap: 1rem; padding: 1rem;
         grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); }
  .card { background: #fff; border-radius: 8px; padding: 1rem; box-shadow: 0 1px 3px #0002; }
  .card h2 { margin: 0; font-size: 1.05rem; font-family: monospace; }
  .card p { margin: .3rem 0 .7rem; font-size: .85rem; color: #55657a; }
  label { display: block; font-size: .8rem; margin-top: .4rem; }
  input { width: 100%; box-sizing: border-box; padding: .4rem; font-family: monospace;
          border: 1px solid #b9c4d0; border-radius: 4px; }
  button { margin-top: .7rem; padding: .45rem 1rem; border: 0; border-radius: 4px;
           background: #1f3a5f; color: #fff; cursor: pointer; }
  .out { margin-top: .7rem; padding: .5rem; border-radius: 4px; font-family: monospace;
         font-size: .85rem; word-break: break-word; display: none; }
  .ok { background: #e3f6e8; color: #14532d; display: block; }
  .err { background: #fde8e8; color: #7f1d1d; display: block; }
  footer { padding: 1rem 1.5rem; font-size: .85rem; color: #55657a; }
</style>
</head>
<body>
<header>
  <h1>target.py playground</h1>
  <p>Type a value per argument. Use JSON: 5, "text", [1, 2], true, null.
     Wrong values show the error the function raises.</p>
</header>
<main id="cards"></main>
<footer>Deployed commit: <code id="sha">loading...</code></footer>
<script>
async function run(card, name, inputs, out) {
  const args = inputs.map(function (i) { return i.value; });
  const res = await fetch('/api/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({function: name, args: args})
  });
  const data = await res.json();
  if (data.ok) {
    out.className = 'out ok';
    out.textContent = 'Result: ' + JSON.stringify(data.result) + '  (' + data.type + ')';
  } else {
    out.className = 'out err';
    out.textContent = data.error_type + ': ' + data.message;
  }
}

async function load() {
  const fns = await (await fetch('/api/functions')).json();
  const root = document.getElementById('cards');
  fns.forEach(function (fn, index) {
    const card = document.createElement('div');
    card.className = 'card';
    const title = document.createElement('h2');
    title.textContent = (index + 1) + '. ' + fn.name + '(' + fn.params.join(', ') + ')';
    const doc = document.createElement('p');
    doc.textContent = fn.doc;
    card.append(title, doc);
    const inputs = [];
    fn.params.forEach(function (param, k) {
      const label = document.createElement('label');
      label.textContent = param;
      const input = document.createElement('input');
      input.value = fn.example[k];
      label.append(input);
      card.append(label);
      inputs.push(input);
    });
    const button = document.createElement('button');
    button.textContent = 'Run';
    const out = document.createElement('div');
    out.className = 'out';
    button.addEventListener('click', function () { run(card, fn.name, inputs, out); });
    card.append(button, out);
    root.append(card);
  });
  const health = await (await fetch('/health')).json();
  document.getElementById('sha').textContent = health.sha;
}
load();
</script>
</body>
</html>
"""


@app.get("/")
def index():
    return INDEX_HTML


@app.get("/health")
def health():
    sha = os.environ.get("RENDER_GIT_COMMIT") or os.environ.get("COMMIT_SHA") or "unknown"
    return jsonify(status="ok", sha=sha)


@app.get("/api/functions")
def functions():
    return jsonify(runner.describe())


@app.post("/api/run")
def run():
    data = request.get_json(silent=True) or {}
    name = data.get("function", "")
    args = data.get("args", [])
    if not isinstance(args, list):
        return jsonify(ok=False, error_type="BadRequest", message="args must be a list"), 400
    return jsonify(runner.run_function(name, args))
