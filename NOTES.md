Resize an image to a target width while preserving aspect ratio, then convert it to **WebP**:

```bash
ffmpeg -i input.jpg \
-vf "scale=1200:-1:flags=lanczos" \
-map_metadata -1 \
-c:v libwebp \
-q:v 80 \
output.webp
```

Crop an image to a square, resize it to a target size, then convert it to **WebP**:

```bash
ffmpeg -i input.jpg \
-vf "crop='min(iw,ih)':'min(iw,ih)',scale=205:205:flags=lanczos" \
-map_metadata -1 \
-c:v libwebp \
-q:v 80 \
output.webp
```
