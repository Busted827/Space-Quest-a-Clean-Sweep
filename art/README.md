# Art

First-pass art for Supply Closet 13-B and Roger, painted in code from the SQ4/SQ5/SQ6 references
(Art guide in the design doc). Not wired into the game yet; the room still uses placeholder art.

- `supply_closet/` 640x360 full-screen background (256 colors), mop and bucket props, and a preview with Roger.
- `roger/` standing front, side and back sprites (~130 px tall) and a turnaround sheet.
- `source/` the Python scripts that paint them (`python3 closet.py`, `roger.py`, then `compose.py`; needs numpy and Pillow).
