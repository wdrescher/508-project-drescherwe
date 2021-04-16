from fastapi import APIRouter

from api.routes import auth, user, artist, booking, parlor

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(booking.router)
router.include_router(artist.router)
router.include_router(parlor.router)