# poopee — CleanTrust

A Vercel-friendly hackathon MVP for public-toilet discovery, sanitation trust scoring, citizen issue reporting and sanitation employment.

## Stack

- HTML/CSS/vanilla JavaScript frontend
- Python serverless API (`api/index.py`)
- Leaflet + OpenStreetMap for the demo map
- Mock data so the app works immediately
- No API keys required for the prototype

## Run locally

Because the frontend is static, you can open `index.html` directly for the UI.

For the Python API, use a Python server or deploy to Vercel. The frontend gracefully keeps working in demo mode if `/api/report` is unavailable.

## Deploy to Vercel

1. Create a GitHub repository and upload these files.
2. Import the repository into Vercel.
3. Deploy with the included `vercel.json`.
4. No environment variables are required for the demo.

## Connect Supabase later

Replace the in-memory `REPORTS` list with Supabase tables such as:

- users
- worker_profiles
- toilets
- toilet_reports
- cleaning_jobs
- job_applications
- cleaning_logs
- ratings
- notifications
- trust_scores

The current UI already separates the main flows so those API calls can be added without redesigning the frontend.

## Demo flow

Citizen → map → toilet details → report issue → admin sees report → worker finds job → completes job → proof/verification → trust score changes.

## Important

The map uses fictional demo facilities around a demo Delhi-area location. They are not presented as verified real-world public facilities.
