from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO

router = APIRouter()

from app.core import settings

# Ensure this matches the redirect URI configured in Google Cloud Console
GOOGLE_REDIRECT_URI = "http://localhost:80/api/v1/auth/google/callback"

google_sso = GoogleSSO(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    redirect_uri=GOOGLE_REDIRECT_URI,
    allow_insecure_http=True,
)

@router.get("/google/login")
async def google_login():
    """Generate login URL and redirect"""
    with google_sso:
        return await google_sso.get_login_redirect()

from app.services import user_service
from app.core.security import create_access_token

@router.get("/google/callback")
async def google_callback(request: Request):
    """Process login response from Google and return user info"""
    with google_sso:
        try:
            # Verify Google user
            google_user = await google_sso.verify_and_process(request)
            
            # Get or create user in Supabase
            user = await user_service.get_or_create_user(
                email=google_user.email,
                display_name=google_user.display_name,
                profile_image=google_user.picture,
            )
            
            if not user:
                raise HTTPException(status_code=400, detail="Failed to create or retrieve user")

            # Create JWT
            access_token = create_access_token(subject=user['id'])
            
            # Redirect to frontend with cookie
            response = RedirectResponse(url="/")
            response.set_cookie(
                key="access_token",
                value=f"Bearer {access_token}",
                httponly=True,
                max_age=1800,
                expires=1800,
            )
            return response
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
