from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from models.email_verification import EmailVerification
from typing import Optional, Tuple
from sqlalchemy import Result, select

class EmailVerificationRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def get_email_verification(self, email: str)-> Optional[EmailVerification]:
        stmt = select(EmailVerification).where(EmailVerification.email == email)
        result: Result[Tuple[EmailVerification]] = await self.session.execute(stmt)
        email_verf: Optional[EmailVerification] = result.scalar_one_or_none()
        return email_verf

    def create_email_verfification(self, email: str, name: str, otp_hash: str, password_hash: str)-> EmailVerification:
        time_now: datetime =datetime.now(timezone.utc)
        otp_expires_at: datetime = time_now + timedelta(minutes= 5)
        next_resend: datetime = time_now
        email_verf: EmailVerification = EmailVerification(
            email = email,
            otp_hash = otp_hash,
            name = name,
            password_hash = password_hash,
            otp_expires_at = otp_expires_at,
            next_resend_at = next_resend
        )
        self.session.add(email_verf)
        return email_verf

    def update_email_verification(self, email_verf: Optional[EmailVerification], otp_hash: str)-> EmailVerification:
        assert email_verf is not None, "email_verf is None"

        time_now: datetime =datetime.now(timezone.utc)
        otp_expires_at: datetime = time_now + timedelta(minutes= 5)
        next_resend: datetime = time_now + timedelta(minutes=1)

        email_verf.otp_hash = otp_hash
        email_verf.otp_expires_at = otp_expires_at
        email_verf.next_resend_at = next_resend

        return email_verf

    async def delete_email_verification(self, email_verf: Optional[EmailVerification]):
        assert email_verf is not None, "email_verf is None"
        await self.session.delete(email_verf)
        return