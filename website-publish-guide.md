# Website Publish Guide

The website files are ready in this folder:

- `index.html`
- `styles.css`
- `script.js`
- `favicon.svg`
- `rendered/`
- `application-figures/`

## Local preview

Run a static server in this folder:

```powershell
& "C:\Users\KomisarisP1-Ahmad_PM\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000/index.html
```

## Option 1: Publish with GitHub Pages

1. Create a GitHub repository.
2. Upload all website files and folders from this workspace.
3. In the repository settings, open `Pages`.
4. Set the source to the main branch root.
5. Wait for GitHub Pages to generate the public URL.

## Option 2: Publish with Netlify

1. Open Netlify.
2. Choose `Add new site`.
3. Drag and drop this folder, or connect a Git repository.
4. Since this is a static site, no build command is required.
5. Netlify will generate a public URL immediately.

## Option 3: Publish with Vercel

1. Open Vercel.
2. Import the folder or connect a Git repository.
3. Keep the project as a static site.
4. Deploy without a build step.

## Important note

When publishing, keep the folder structure unchanged so that all figure images and PDF download links continue to work.