from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from ..user_router.schemas import User, UserBase


class DisapproveCompetencyDetails(BaseModel):
    # appraisal_form_id: int
    # competency_id: int
    comments: str


class disapprove_competency_details(DisapproveCompetencyDetails):
    pass


class ApproveCompetencyDetails(BaseModel):
    appraisal_form_id: int
    competency_id: int


class approve_competency_details(ApproveCompetencyDetails):
    pass


class Auth(UserBase):
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]


class UserBase2(BaseModel):
    # staff_id:int
    fname: str
    sname: str
    oname: str
    email: EmailStr
    supervisor: int
    gender: str
    role: str
    department: str
    positions: str
    grade: int
    appointment: Optional[datetime]


class UpdateStaff(BaseModel):
    staff_id: int
    fname: str
    sname: str
    oname: str
    email: EmailStr
    supervisor: int
    gender: str
    role: str
    department: str
    positions: str
    grade: int
    appointment: Optional[datetime]


class UpdateDeadline(BaseModel):
    deadline_id: int
    deadline_type: str
    start_date: Optional[datetime]
    ending: Optional[datetime]


class UserCreate(UserBase):
    pass


class update_staff(UpdateStaff):
    pass


class User(UserBase):
    id: int


class DeleteStaff(BaseModel):
    staff_id: int


class delete_staff(DeleteStaff):
    pass


class DeadlineTable(BaseModel):
    deadline_type: str
    start_date: Optional[datetime]
    ending: Optional[datetime]


class DeleteDeadline(BaseModel):
    deadline_id: int


class delete_deadline(DeleteDeadline):
    pass


class create_deadline(DeadlineTable):
    pass


class update_deadline(UpdateDeadline):
    pass


class read_deadline_table(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    ending: DeadlineTable
    deadline_id: DeadlineTable


class DisaproveForm(BaseModel):
    comment: str


class DisaproveCompetencyDetails(BaseModel):
    comments: str


class disaprove_form(DisaproveForm):
    pass


class disaprove_competency_details(DisaproveCompetencyDetails):
    pass


class ApproveMidForm(BaseModel):
    remarks: str


class approve_mid_form(ApproveMidForm):
    pass
