from fastapi import Depends, Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from app.auth.routes import user_by_id
from app.auth.schemas import UserSchema
from app.city.routes import city_by_id
from .utils import Context

frontend_auth_router = APIRouter(prefix="/profile", tags=["Frontend-Profile"])

templates = Jinja2Templates(directory="frontend/templates")


@frontend_auth_router.get("/{id}/")
async def profile(request: Request, user: UserSchema = Depends(user_by_id)):
    city = await city_by_id(user.city)
    ctx = Context(user=user, city=city)
    return templates.TemplateResponse(request=request, name="auth_profile.html", context=ctx.get_context)
