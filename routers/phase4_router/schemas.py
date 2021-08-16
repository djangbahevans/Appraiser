from datetime import datetime, time, timedelta
from typing import List, Optional, Union
from pydantic import BaseModel
from enum import Enum


class Action(str, Enum):

    submit = 'submit'
    save = 'save'


class CompDetails(BaseModel):
    competency_id: int
    appraisal_form_id: int
    grade: int
    submit: int


class create_comp_details(CompDetails):
    pass


class CompetenceDetails(BaseModel):
    competencies: List[CompDetails]


class create_competence_details(CompetenceDetails):
    pass


class PerformanceDetails(BaseModel):
    appraisal_form_id: int
    weight: str
    comments: str
    final_score: str
    approved_date: datetime
    submit: int


class create_performance_details(PerformanceDetails):
    pass


class OrganizationAndManagement(BaseModel):
    plan_and_manage: int
    worl_systematically: int
    manage_others: int


class InnovationAndStrategicThinking(BaseModel):
    support_for_change: int
    think_broadly: int
    originality_in_thinking: int


class LeadershipAndDecisionMaking(BaseModel):
    initiate_action: int
    accept_responsibility: int
    exercise_judgement: int


class DevelopingAndImproving(BaseModel):
    commitment_to_development: int
    commitment_to_customer: int


class Communication(BaseModel):
    communicate_clearly: int
    negotiate_and_manage: int
    relate_and_network: int


class JobKnowledgeAndTechSkills(BaseModel):
    mental_physical_skills: int
    cross_functional_awareness: int
    building_applying_sharing_expertise: int


class SupportingAndCooperating(BaseModel):
    work_with_teams: int
    show_support: int
    adhere_to_principles: int


class MaximisingAndMaintainingProductivity(BaseModel):
    motivate_and_instigate: int
    accept_challenges: int
    manage_pressure: int


class DevelopingAndManagingBudgets(BaseModel):
    awareness_of_financial_issues: int
    understanding_business_processes: int
    executing_actions: int


class AbilityToDevelopStaff(BaseModel):
    develop_others: int
    provide_guidance: int


class CommitmentToPersonalDevelopment(BaseModel):
    eagerness_for_development: int
    inner_drive_to_training: int


class DeliveringResults(BaseModel):
    ensure_customer_satisfaction: int
    ensure_quality_service: int


class FollowingInstructions(BaseModel):
    keep_to_laid_down_regulations: int
    willingness_to_act_for_customer_satisfaction: int


class RespectAndCommitment(BaseModel):
    respect_and_commitment: int


class AbilityToWorkEffectivelyInATeam(BaseModel):
    ability_to_work_in_a_team: int


class AnnualAppraisal(BaseModel):
    appraisal_form_id: int
    submit: int
    organization_and_management: List[Union[OrganizationAndManagement,
                                      InnovationAndStrategicThinking, LeadershipAndDecisionMaking]]
    innovation_and_strategic_thinking: List[InnovationAndStrategicThinking]
    leadership_and_decision_making: List[LeadershipAndDecisionMaking]
    developing_and_improving: List[DevelopingAndImproving]
    communication: List[Communication]
    job_knowledge_and_technical_skills: List[JobKnowledgeAndTechSkills]
    supporting_and_cooperating: List[SupportingAndCooperating]
    maximising_and_maintaining_productivity: List[MaximisingAndMaintainingProductivity]
    developing_managing_budgets_and_saving_cost: List[DevelopingAndManagingBudgets]
    ability_to_develop_staff: List[AbilityToDevelopStaff]
    commitment_to_own_personal_development_and_training: List[CommitmentToPersonalDevelopment]
    delivering_results_and_ensuring_customer_satisfaction: List[DeliveringResults]
    following_instructions_and_working_towards_organizational_goals: List[
        FollowingInstructions]
    respect_and_commitment: List[RespectAndCommitment]
    ability_to_work_effectively_in_a_team: List[AbilityToWorkEffectivelyInATeam]


class EndOfYearReview(BaseModel):
    assessment: str
    score: int
    weight: int
    comment: str
    appraisal_form_id: int


class create_annual_appraisal(AnnualAppraisal):
    pass


class create_end_of_year_review(EndOfYearReview):
    pass


class CoreCompetencies(BaseModel):
    annual_appraisal_id: int
    grade: int


class UpdateCoreCompetencies(BaseModel):
    competency_id: int
    annual_appraisal_id: int
    grade: int


class create_core_competencies(CoreCompetencies):
    pass


class create_non_core_competencies(CoreCompetencies):
    pass


class update_core_competencies(UpdateCoreCompetencies):
    pass


class FormBase(BaseModel):
    result_areas: str
    target: str
    resources: str
    appraisal_form_id: int
    status: int
    form_hash: str


class UpdateAnnualPlan(BaseModel):
    result_areas: str
    target: str
    resources: str
    appraisal_id: int
    annual_plan_id: int
    status: int
    form_hash: str


class UpdateAnnualAppraisal(BaseModel):
    comment: str
    field: str
    appraisal_form_id: int
    status: int
    annual_appraisal_id: int


class UpdateAppraisalForm(BaseModel):
    appraisal_form_id: int
    department: str
    # grade: int
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
    status: bool
