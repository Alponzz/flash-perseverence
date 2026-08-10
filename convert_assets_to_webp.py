from pathlib import Path
from PIL import Image
import io
import sys
import traceback

try:
    root = Path('.')
    png_files = list(root.glob('**/*.png'))
    svg_files = list(root.glob('**/*.svg'))
    converted = []

    for p in png_files:
        webp_path = p.with_suffix('.webp')
        if webp_path.exists():
            print(f"Skipping (exists): {webp_path}")
            continue
        try:
            img = Image.open(p).convert('RGBA')
            img.save(webp_path, 'WEBP', quality=90)
            converted.append(webp_path)
            print(f"Converted PNG -> {webp_path}")
        except Exception as e:
            print(f"Failed to convert {p}: {e}")
            traceback.print_exc()

    for s in svg_files:
        webp_path = s.with_suffix('.webp')
        if webp_path.exists():
            print(f"Skipping (exists): {webp_path}")
            continue
        try:
            import cairosvg
            png_bytes = cairosvg.svg2png(url=str(s))
            img = Image.open(io.BytesIO(png_bytes)).convert('RGBA')
            img.save(webp_path, 'WEBP', quality=90)
            converted.append(webp_path)
            print(f"Converted SVG -> {webp_path}")
        except Exception as e:
            print(f"Failed to convert {s}: {e}")
            traceback.print_exc()

    print('\nDone. Converted files:')
    for c in converted:
        print(c)
except Exception:
    traceback.print_exc()
    sys.exit(1)
