# Deployment Guide for Carely AI Backend

## Important Notice About Vercel

While this backend can be deployed to Vercel, there are important considerations:

### Vercel Limitations for This Application

1. **Database**: Vercel serverless functions are stateless. The SQLite database won't persist between deployments.
2. **File System**: File uploads and local storage won't work reliably.
3. **Cold Starts**: First requests may be slow due to function initialization.
4. **Function Timeout**: Limited execution time (10-60 seconds depending on plan).

### Recommended Deployment Options

#### Option 1: Railway (Recommended for Full-Stack Backend)
[Railway](https://railway.app) is ideal for FastAPI applications with databases.

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Add PostgreSQL database
railway add postgresql

# Deploy
railway up
```

#### Option 2: Render
[Render](https://render.com) offers free hosting for web services with PostgreSQL.

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Select `backend` directory
5. Add build command: `pip install -r requirements.txt`
6. Add start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add PostgreSQL database
8. Set environment variables

#### Option 3: Fly.io
[Fly.io](https://fly.io) is great for containerized applications.

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
cd backend
fly launch

# Deploy
fly deploy
```

## Deploying to Vercel (With Limitations)

If you still want to use Vercel, follow these steps:

### Prerequisites
- Vercel account
- Vercel CLI installed: `npm install -g vercel`
- External database (e.g., Supabase, PlanetScale, Neon)

### Steps

1. **Set up external database**:
   
   For PostgreSQL, use [Supabase](https://supabase.com) or [Neon](https://neon.tech):
   ```bash
   # Update DATABASE_URL in Vercel environment variables
   DATABASE_URL=postgresql://user:password@host/database
   ```

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Login to Vercel**:
   ```bash
   vercel login
   ```

4. **Deploy**:
   ```bash
   cd backend
   vercel
   ```

5. **Set environment variables**:
   ```bash
   vercel env add SECRET_KEY
   vercel env add DATABASE_URL
   vercel env add BACKEND_CORS_ORIGINS
   ```

6. **Deploy to production**:
   ```bash
   vercel --prod
   ```

### Vercel Configuration

The `vercel.json` file is already configured. You may need to adjust:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

### Required Changes for Vercel

1. **Use external database** (SQLite won't work):
   ```env
   DATABASE_URL=postgresql://user:password@host/database
   ```

2. **Install PostgreSQL driver**:
   ```bash
   pip install psycopg2-binary
   ```

3. **Update requirements.txt**:
   ```txt
   psycopg2-binary==2.9.9
   ```

## Environment Variables

Set these in your Vercel project settings:

- `SECRET_KEY`: Your secret key for JWT tokens
- `DATABASE_URL`: External database connection string
- `BACKEND_CORS_ORIGINS`: JSON array of allowed origins
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration (default: 10080)
- `MAX_APPOINTMENT_DAYS_AHEAD`: Maximum days for appointments (default: 90)

## Testing Locally

Before deploying, test locally:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Post-Deployment

1. Test all endpoints using the interactive docs
2. Set up monitoring and logging
3. Configure custom domain (if needed)
4. Set up CI/CD pipeline

## Troubleshooting

### Cold Start Issues
- Keep functions warm with periodic health checks
- Consider upgrading to Pro plan for better performance

### Database Connection Errors
- Ensure DATABASE_URL is correctly set
- Check database allows connections from Vercel IPs
- Use connection pooling

### CORS Errors
- Verify BACKEND_CORS_ORIGINS includes your frontend URL
- Check that middleware is properly configured

## Support

For deployment issues:
- Vercel: https://vercel.com/docs
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs

