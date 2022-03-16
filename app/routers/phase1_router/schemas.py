from datetime import datetime, time, timedelta
from typing import List, Optional
from pydantic import BaseModel


class FormBase(BaseModel):
    result_areas: str
    target: str
    resources: str
    appraisal_form_id: int
    submit: int


class UpdateAnnualPlan(BaseModel):
    result_areas: str
    target: str
    resources: str
    appraisal_form_id: int
    annual_plan_id: int


class AnnualAppraisal(BaseModel):
    comment: str
    field: str
    appraisal_form_id: int
    status: int


class UpdateAnnualAppraisal(BaseModel):
    comment: str
    field: str
    appraisal_form_id: int
    status: int
    annual_appraisal_id: int


class UpdateAppraisalForm(BaseModel):
    appraisal_form_id: int
    department: str
    grade: int
    positions: str
    date: datetime
    staff_id: int


class AppraisalForm(BaseModel):
    department: str
    grade: int
    positions: str
    date: datetime
    staff_id: int


class CreateAprpaisalForm(BaseModel):
    deadline: str
    department: str
    positions: str
    grade: int
    date: datetime
    staff_id: int
    progress_review: str
    remarks: str
    assessment: str
    score: int
    weight: int
    comment: str


class DeleteAnnualAppraisal(BaseModel):
    annual_appraisal_id: int


class DeleteAnnualPlan(BaseModel):
    annual_plan_id: int


class DeleteAppraisalForm(BaseModel):
    appraisal_form_id: int


class appraisal_form(AppraisalForm):
    pass


class create_appraisal_form(CreateAprpaisalForm):
    pass


class update_appraisal_form(UpdateAppraisalForm):
    pass


class delete_appraisal_form(DeleteAppraisalForm):
    pass


class create_annual_plan(FormBase):
    pass


class update_annual_plan(UpdateAnnualPlan):
    pass


class delete_annual_plan(DeleteAnnualPlan):
    pass


class create_annual_appraisal(AnnualAppraisal):
    pass


class update_annual_appraisal(UpdateAnnualAppraisal):
    pass


class delete_annual_appraisal(DeleteAnnualAppraisal):
    pass


class UpdateForm(BaseModel):
    kra: FormBase
    target: FormBase
    resource_required: FormBase


class update_phase1(BaseModel):
    kra: Optional[FormBase]
    target: Optional[FormBase]
    resource_required: Optional[FormBase]


class get_Phase1(BaseModel):
    kra: FormBase
    target: FormBase
    resource_required: FormBase


class approve_phase1(BaseModel):
    # kra: FormBase
    # target: FormBase
    # resource_required: FormBase
    status: bool
