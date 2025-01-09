from fastapi import Depends, Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from app.auth.routes import get_current_user, user_by_id, user_current_user
from app.auth.schemas import SUser
from app.city.routes import city_by_id
from app.city.schema import CitySchema
from .utils import Context

frontend_auth_router = APIRouter(prefix="/profile", tags=["Frontend-Profile"])

templates = Jinja2Templates(directory="frontend/templates")


@frontend_auth_router.get("/login/")
async def login_page(request: Request):
    ctx = Context()  
    return templates.TemplateResponse(request=request, name="auth_login.html", context=ctx.get_context)


@frontend_auth_router.get("/me/")
async def my_profile(request: Request):
    ctx = Context(user=SUser(username="testuser", email="krutoy@mail.com", password=b"123456789", full_name="testname", city=0), city=CitySchema(id=0, name="Moscow")) 
    return templates.TemplateResponse(request=request, name="auth_profile.html", context=ctx.get_context) 


@frontend_auth_router.get("/{id}/")
async def user_profile(request: Request, user: SUser = Depends(user_by_id)):
    city = await city_by_id(user.city) 
    ctx = Context(user=user, city=city)
    return templates.TemplateResponse(request=request, name="auth_profile.html", context=ctx.get_context)
