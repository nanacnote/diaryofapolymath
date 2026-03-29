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

Create and apply Django migrations after modifying the `models.py` file:
```bash
django-admin makemigrations         # Generate new migration files based on model changes
django-admin migrate --no-input     # Apply migrations to the database
```

Additional useful Django migration commands:
```bash
# Show pending migrations
django-admin showmigrations

# Show SQL for a specific migration (preview before applying)
django-admin sqlmigrate <app> <migration_name>

# Roll back a migration
django-admin migrate <app> <previous_migration_name>

# Create empty migration for custom SQL
django-admin makemigrations --empty <app> --name <description>
```

### TODO:
- [ ] Add scroll-to-top button
- [ ] Add post view count
- [ ] Add post like feature
- [ ] Add comment upvote feature
- [ ] Add post search functionality
- [ ] Add posts pagination
- [ ] Add comment pagination
- [ ] Add RSS feed css (allowing browsers to render the feed rather than downloading it as a file)
- [ ] Add newsletter subscription form and functionality
- [ ] Add sitemap.xml
- [ ] Add email verification for comment posting
- [ ] Add a blogroll with links to other blogs
  - [ ] one for personal currated links
  - [ ] one for community submitted links
