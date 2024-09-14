## Trendz (Part 1)

1. Get jwt secret by visiting `/static../jwt.secret` (same vuln is used to get binary in Trendzzzz)
2. Forge new accesstoken with `role=admin`
3. Go to admin panel `/admin/dashboard` and find post id
4. View the post `/user/posts/<post-id>`
