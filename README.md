# Landing pages

Private, standalone landing pages for Acheron, Freewhirr and Shipwatch. Acheron is the first implementation. This repository has no remote and nothing is deployed or made public without Andy McCutcheon's specific approval.

## Preview

From the repository root, run:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/acheron/`.

## House rules

- `vendor/pattern/` is a read-only, pinned snapshot. Replace the whole snapshot to update it; never edit files in place.
- Marketing-only pieces live under the `--lp-` namespace in `shared/`.
- A marketing piece is promoted into the Design System Pattern only after two landing pages use it.
- The pages are static HTML and CSS. Small progressive-enhancement scripts are allowed within the documented budget.
- Nothing is deployed or made public without Andy's specific approval.

Run `python3 tools/check_literals.py` and `python3 tools/check_copy.py` before committing page changes.

