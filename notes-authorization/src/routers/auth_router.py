import logging
from typing import Dict

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException

from src.core import container
from src.pydantic_models import RegistrationForm
from src.services.user_auth_service import UserAlreadyExists

router = APIRouter()

@router.post('/register')
async def register_user(form: RegistrationForm,
                        background_tasks: BackgroundTasks,
                        auth_service=Depends(container.get_user_auth_service),
                        email_service=container.email_verification_service
                        )-> Dict:
    try:
        user, code = await auth_service.register_user(form)
        background_tasks.add_task(email_service.send_verification_email, user.email, code)
        return {'success': True, 'message': 'User registered successfully'}
    except UserAlreadyExists as error:
        logging.info(error)
        raise HTTPException(status_code=409, detail=str(error))
    except Exception as error:
        logging.exception(error)
        raise HTTPException(status_code=500, detail="Unexpected error")
