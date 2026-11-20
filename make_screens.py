"""Render terminal-style screenshots from workflow transcripts."""

from PIL import Image, ImageDraw, ImageFont

for txt, out in [("git_workflow.txt", "git_workflow.png"),
                 ("docker_workflow.txt", "docker_workflow.png")]:
    lines = open(txt, encoding="utf-8").read().splitlines()
    font = None
    for fp in ["C:\\\\Windows\\\\Fonts\\\\consolas.ttf", "C:\\\\Windows\\\\Fonts\\\\consols.ttf", "C:\\\\Windows\\\\Fonts\\\\lucon.ttf", "C:\\\\Windows\\\\Fonts\\\\arial.ttf"]:
        try:
            font = ImageFont.truetype(fp, 14)
            break
        except OSError:
            continue
    lh = 22
    w = max(font.getlength(l) for l in lines) + 40
    h = lh * len(lines) + 30
    img = Image.new("RGB", (int(w), int(h)), "#1e1e1e")
    d = ImageDraw.Draw(img)
    y = 12
    for line in lines:
        colour = "#7ec87e" if line.startswith("$ ") else "#d4d4d4"
        d.text((16, y), line, font=font, fill=colour)
        y += lh
    img.save(out)
    print(out, "written")
