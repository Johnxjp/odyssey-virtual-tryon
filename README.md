# Virtual Try-On

A virtual try-on application for clothing visualization.

## How to Run

### Prerequisites
- Python 3.x installed on your system

### Starting the Development Server

**Start the Python HTTP server:**
```bash
python3 -m http.server 8000
```

**Open your browser and visit:**
```
http://localhost:8000
```

### Changing the Port

To use a different port, replace `8000` with your desired port number:
```bash
python3 -m http.server 3000
```

## Project Structure

- `index.html` - Main application file
- `clothing-config.json` - Clothing configuration
- `assets/` - Project assets

## Development

This project uses a simple Python HTTP server for local development. The production build process is handled by `build.py`.

## Deployment to Render

This application can be deployed as a static site on Render's free tier. The Odyssey API key is injected during the build process via environment variable, keeping it out of version control while still allowing client-side SDK functionality.

### Prerequisites

- GitHub account
- Render account (free tier available at [render.com](https://render.com))
- Odyssey API key (get one from [odyssey.ml](https://odyssey.ml))

### Deployment Steps

#### 1. Push Code to GitHub

If you haven't already, push this repository to GitHub:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### 2. Connect Repository to Render

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Connect your GitHub account if not already connected
4. Select this repository from the list

#### 3. Configure Build Settings

Render should auto-detect the `render.yaml` configuration file. Verify these settings:

- **Name**: `odyssey-virtual-tryon` (or your preferred name)
- **Branch**: `main`
- **Build Command**: `python3 build.py`
- **Publish Directory**: `public`

#### 4. Add Environment Variable

In the Render dashboard for your static site:

1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add:
   - **Key**: `ODYSSEY_API_KEY`
   - **Value**: Your Odyssey API key (e.g., `ody_sjVzTgXISZa3HdoaCBHepQsy8UrKc6Rz`)
4. Click **"Save Changes"**

#### 5. Deploy

Click **"Create Static Site"** or **"Manual Deploy"** → **"Deploy latest commit"**

Render will:
1. Clone your repository
2. Run `python3 build.py` (which injects the API key)
3. Serve the files from the `public/` directory
4. Provide you with a live URL (e.g., `https://odyssey-virtual-tryon.onrender.com`)

### Local Testing with Build Script

To test the build process locally before deploying:

#### Option 1: Using Environment Variable

```bash
export ODYSSEY_API_KEY='your_api_key_here'
python3 build.py
```

Then serve the built files:
```bash
cd public
python3 -m http.server 8000
```

#### Option 2: Using .env File

Create a `.env` file in the project root (already gitignored):

```bash
ODYSSEY_API_KEY=your_api_key_here
```

Load it and run the build:
```bash
export $(cat .env | xargs)
python3 build.py
```

### Configuration Details

#### Build Process

The `build.py` script:
1. Reads `ODYSSEY_API_KEY` from environment variable
2. Reads `index.html` and replaces `ODYSSEY_API_KEY_PLACEHOLDER` with the actual key
3. Copies the modified `index.html` to `public/`
4. Copies `clothing-config.json` and `assets/` directory to `public/`

#### Files Created During Build

- `public/index.html` - Main HTML file with API key injected
- `public/clothing-config.json` - Clothing configuration
- `public/assets/` - All asset files (images, etc.)

**Note**: The `public/` directory is gitignored and should never be committed to version control.

### Verification Steps

After deployment, verify everything works:

1. Visit your deployed URL
2. Open browser DevTools (F12) → Console tab
3. Verify no errors appear
4. Test selecting male/female model
5. Test clicking clothing items to verify try-on works
6. Verify video stream plays correctly
7. Check Network tab to ensure Odyssey API calls succeed
8. Test on both desktop and mobile browsers

### Troubleshooting

#### Build Fails with "ODYSSEY_API_KEY not set"

**Solution**: Make sure you added the environment variable in Render's dashboard under the "Environment" tab.

#### API Key Not Injected (Still Shows Placeholder)

**Solution**:
1. Check Render build logs for errors
2. Verify the placeholder text in `index.html` matches exactly: `ODYSSEY_API_KEY_PLACEHOLDER`
3. Trigger a manual redeploy

#### Video Stream Doesn't Load

**Solution**:
1. Check browser console for errors
2. Verify the Odyssey API key is valid and has sufficient credits
3. Check if domain restrictions are enabled on your API key (see Security Notes below)

#### 404 Errors for Assets

**Solution**:
1. Verify `assets/` directory exists in your repository
2. Check Render build logs to confirm assets were copied
3. Ensure file paths in `clothing-config.json` are correct

### Security Notes

#### API Key Visibility

⚠️ **Important**: The API key will be visible in the browser's source code and DevTools. This is unavoidable because the Odyssey SDK requires client-side execution for WebRTC video streaming.

**What's Protected:**
- ✅ API key is not committed to version control
- ✅ Key is managed securely via Render's environment variables
- ✅ Key can be rotated by updating the env var (triggers automatic rebuild)

**What's Exposed:**
- ⚠️ Anyone visiting your site can view the API key in browser source
- ⚠️ Key can be extracted and potentially used elsewhere

#### Mitigation Strategies

1. **Domain Restrictions** (Recommended)
   - Configure your Odyssey API key to only work on your Render domain
   - Check Odyssey.ml dashboard for domain restriction settings
   - Add: `https://your-app-name.onrender.com`

2. **Usage Monitoring**
   - Regularly check Odyssey dashboard for unexpected usage
   - Set up billing alerts if available
   - Monitor for unusual traffic patterns

3. **Rate Limiting**
   - Consider implementing rate limiting on your site
   - Use a production key with limited quotas for public deployments

4. **Key Rotation**
   - Rotate your API key regularly (monthly or quarterly)
   - Update the environment variable in Render dashboard
   - Render will automatically rebuild and redeploy

#### Rotating the API Key

To rotate your API key:

1. Generate a new key in Odyssey.ml dashboard
2. Update `ODYSSEY_API_KEY` in Render's Environment tab
3. Click **"Save Changes"** - Render will automatically rebuild
4. Revoke the old key in Odyssey.ml dashboard

### Cost Information

#### Render Free Tier
- **Bandwidth**: 100 GB/month included
- **Build minutes**: Shared pool for free accounts
- **Custom domains**: Not available on free tier
- **SSL**: Automatic HTTPS included

#### Odyssey API Pricing
- Check [odyssey.ml](https://odyssey.ml) for current pricing
- Monitor your usage in the Odyssey dashboard
- Set up billing alerts to avoid unexpected charges

### Advanced Configuration

#### Custom Domain

To use a custom domain (requires Render paid plan):

1. Add your domain in Render dashboard
2. Update DNS records as instructed
3. Update Odyssey API key domain restrictions

#### Environment-Specific Keys

To use different API keys for staging/production:

1. Create separate Render services (e.g., `odyssey-staging`, `odyssey-production`)
2. Set different `ODYSSEY_API_KEY` values for each
3. Deploy from different branches if needed

### Rollback Plan

If deployment fails or has issues:

1. **Check Build Logs**: Review Render's build logs for errors
2. **Test Locally**: Run `build.py` locally to isolate the issue
3. **Verify Environment Variable**: Ensure `ODYSSEY_API_KEY` is set correctly
4. **Manual Rollback**: In Render dashboard, go to "Events" and redeploy a previous successful build

### Support

For issues with:
- **Deployment/Render**: Check [Render documentation](https://render.com/docs/static-sites)
- **Odyssey SDK**: Check [Odyssey documentation](https://odyssey.ml/docs)
- **This project**: Open an issue in this repository
