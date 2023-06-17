from fastapi import APIRouter, Depends

from blog import oauth2_scheme

# we add this here so we have a single router to deal with unless we need to break it into multiple
router = APIRouter(
    prefix="/api",
    tags=[],
    # makes all routes authed, or you can add per route
    dependencies=[Depends(oauth2_scheme)]
)
