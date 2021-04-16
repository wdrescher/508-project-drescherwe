from fastapi import APIRouter, Depends, HTTPException

from api.models.user import Profile
from api.models.booking import Booking
from api.models.responses import BookingListResponse, SuccessResponse
from api.models.requests import CreateBookingRequest, ScheduleBookingRequest
from api.services.booking import create_booking, get_user_bookings, booking_exists, set_price, approve_price, approve_design, schedule_booking
from api.services.dependencies import get_current_user

router = APIRouter(
    prefix="/booking"
)

@router.post("/create", response_model=Booking)
async def new_booking(request: CreateBookingRequest, current_user: Profile = Depends(get_current_user)): 
    booking = await create_booking(request, current_user)
    if booking is None: 
        raise HTTPException(status_code=400, detail="Whoops!")
    return Booking(**dict(booking))

@router.get("/list", response_model=BookingListResponse)
async def list_bookings(current_user: Profile = Depends(get_current_user)): 
    bookings = await get_user_bookings(current_user)
    if bookings is None: 
        return []
    return {"bookings": bookings}

@router.get("/{booking_id}/approve-price")
async def approve_price_call(booking: Booking = Depends(booking_exists),
                        current_user: Profile = Depends(get_current_user)): 
    response = await approve_price(current_user, booking.booking_id, True)
    if response is None: 
        raise HTTPException(status_code=400)
    return SuccessResponse()

@router.get("/{booking_id}/set-price")
async def set_price_call(price: int,
                         booking: Booking = Depends(booking_exists),
                         current_user: Profile = Depends(get_current_user)):
    response = await set_price(current_user, booking.booking_id, price)
    if response is None: 
        raise HTTPException(status_code=400)
    return SuccessResponse()

@router.get("/{booking_id}/approved-design")
async def approve_design_call(booking: Booking = Depends(booking_exists), current_user: Profile = Depends(get_current_user)):
    response = await approve_design(current_user, booking.booking_id)
    if response is None: 
        raise HTTPException(status_code=400)
    return SuccessResponse()

@router.post("/{booking_id}/time-slot")
async def schedule_booking_endpoint(request: ScheduleBookingRequest, booking: Booking = Depends(booking_exists), current_user: Profile = Depends(get_current_user)):
    response = await schedule_booking(request, booking.booking_id)
    if response is False: 
        raise HTTPException(status_code=301)
    return SuccessResponse()