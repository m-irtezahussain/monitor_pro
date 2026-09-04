from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import IntegrityError
import bcrypt

from app.models.user import User
from app.schemas.auth import SignupRequest, SignupResponse, LoginRequest, LoginResponse, RefreshRequest

from app.services.security import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(request: SignupRequest):
    email = request.email.lower().strip()

    existing_user = await User.get_or_none(email=email)
    if existing_user: 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    hashed_password = hash_password(request.password)

    try:
        user = await User.create(
            name=request.name.strip(),
            email=email,
            password=hashed_password
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    return SignupResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
async def login(request: LoginRequest):
    email = request.email.lower().strip()
    user = await User.get_or_none(email=email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    
    check_password = verify_password(request.password, user.password)
    
    if check_password is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    
    access_token = create_access_token(user.id, user.name, user.email)
    refresh_token = create_refresh_token(user.id)

    try:
        user.access_token = access_token
        user.refresh_token = refresh_token
        await user.save()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while logging in"
        )

    return LoginResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh")
async def refresh(data: RefreshRequest):
    try:
        payload = decode_refresh_token(data.token)

        user = User.get_or_none(id=payload['sub'])

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        access_token = create_access_token(user.id, user.name, user.email)
        refresh_token = create_refresh_token(user.id)

        try:
            user.access_token = access_token
            user.refresh_token = refresh_token
            await user.save()
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while refreshing tokens"
            )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    