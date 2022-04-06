--
-- PostgreSQL database dump
--

-- Dumped from database version 12.8 (Debian 12.8-1.pgdg110+1)
-- Dumped by pg_dump version 12.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: gender_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.gender_type AS ENUM (
    'male',
    'female'
);


--
-- Name: add_staff(character varying, character varying, character varying, character varying, integer, character varying, character varying, character varying, integer, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.add_staff(stdfname character varying, stdsname character varying, stdoname character varying, stdemail character varying, stdsupervisor integer, stdgender character varying, stddepartment character varying, stdpositions character varying, stdgrade integer, stdappointment date, stdroles integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.staff(fname,sname,oname,email,supervisor,gender,department,positions,grade,appointment,roles)
values(stdfname,stdsname,stdoname,stdemail,stdsupervisor,stdgender,stddepartment,stdpositions,stdgrade,stdappointment,stdroles);
return 'inserted successfully';
	   end;
$$;


--
-- Name: annual_appraisal_form_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_appraisal_form_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO annual_appraisal(appraisal_form_id)

         VALUES(NEW.appraisal_form_id);
RETURN NEW;

END;
$$;


--
-- Name: annual_plan(character varying, character varying, character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_plan(stdresult_areas character varying, stdtarget character varying, stdresources character varying, stdappraisal_form_id integer, stdstaff_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.annual_plan(result_areas,target,resources,appraisal_form_id,staff_id)
values(stdresult_areas,stdtarget,stdresources,stdappraisal_form_id,stdstaff_id);
return 'inserted successfully';
end;
$$;


--
-- Name: appraisal_form(character varying, integer, character varying, bigint, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisal_form(stddepartment character varying, stdgrade integer, stdposition character varying, stdappraisal_form_id bigint, stddate date, stdstaffid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.appraisal_form(department,grade,position,appraisal_form_id,date,staff_id)
values(stddepartment,stdgrade,stdposition,stdappraisal_form_id,stddate,stdstaff_Id)
;

return 'inserted successfully';
end;
$$;


--
-- Name: appraisal_form_id_hash_table_trigger_function(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisal_form_id_hash_table_trigger_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO hash_table(appraisal_form_id)
	SELECT NEW.appraisal_form_id WHERE NOT EXISTS
( SELECT * FROM public.hash_table WHERE appraisal_form_id = NEW.appraisal_form_id);

         VALUES(NEW.appraisal_form_id);
RETURN NEW;

END;
$$;


--
-- Name: appraisal_id_end_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisal_id_end_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO public.endofyear_review(appraisal_form_id)
SELECT NEW.appraisal_form_id WHERE NOT EXISTS
( SELECT * FROM public.endofyear_review WHERE appraisal_form_id = NEW.appraisal_form_id);

--          VALUES(NEW.appraisal_form_id);
RETURN NEW;

END;
$$;


--
-- Name: appraisalformid_insert_supcom_trigger_func(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisalformid_insert_supcom_trigger_func() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO supervisor_comment(appraisal_form_id)

         VALUES(NEW.appraisal_form_id);
RETURN NEW;

END;
$$;


--
-- Name: appraisalformid_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisalformid_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO annual_plan(appraisal_form_id)

         VALUES(NEW.appraisal_form_id);
RETURN NEW;


END;
$$;


--
-- Name: approve_competency_details(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.approve_competency_details(stdappraisal_form_id integer, stdcompetency_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
verified bool;
vstaff_id integer;
 approved integer;
 id_verified integer;
begin

select exists(select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id) into verified;
select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id into vstaff_id;
select competency_id from competency_details where appraisal_form_id=stdappraisal_form_id into id_verified;

perform *FROM public.competency_details;
update competency_details set status=1
where appraisal_form_id=stdappraisal_form_id and competency_id=stdcompetency_id;
update competency_details set disapprove_status=0
where appraisal_form_id=stdappraisal_form_id and competency_id=stdcompetency_id;

return 'Form Approved';
	   end;
$$;


--
-- Name: approve_form_details(integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.approve_form_details(stdappraisal_form_id integer, stdtype_form character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
user_email character varying;
verified bool;
vstaff_id integer;
 approved integer;
 new_hash character varying;
 mid integer;
begin

select exists(select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id) into verified;
select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id into vstaff_id;
select email from staff where staff_id=vstaff_id  into user_email;

select start_status from public.view_users_form_details where appraisal_form_id=stdappraisal_form_id and  start_status=1  into approved; 
select mid_status from public.view_users_form_details where  appraisal_form_id=stdappraisal_form_id and mid_status=1 into mid;

select hash from hash_table where email=user_email into new_hash;
sELECT public.generate_hash() into new_hash;

if verified='false'
then 
return 'Form Not Found';

--elsif approved=1
--then 
--return'Form Already Approved';

--elsif mid=1
--then 
--return'Form Already Approved';

elsif verified='true' 
then

if  stdtype_form='Start'then
perform *FROM public.view_users_form_details;
update annual_plan set start_status=1
where appraisal_form_id=stdappraisal_form_id;
update annual_plan set annual_plan_status=0
where appraisal_form_id=stdappraisal_form_id;
update hash_table set hash=new_hash
where email=user_email;
update annual_plan set submit=1
where appraisal_form_id=stdappraisal_form_id;

elsif stdtype_form='Mid'then
perform *FROM public.view_users_form_details;
update midyear_review set mid_status=1
where appraisal_form_id=stdappraisal_form_id;
update midyear_review set midyear_review_status=0
where appraisal_form_id=stdappraisal_form_id;
update hash_table set hash=new_hash
where email=user_email;
update midyear_review set submit=1
where appraisal_form_id=stdappraisal_form_id;

elsif  stdtype_form='End'then
perform * FROM public.vw_endofyear_review;
update endofyear_review set end_status=1
where appraisal_form_id=stdappraisal_form_id;
update endofyear_review set endyear_review_status=0
where appraisal_form_id=stdappraisal_form_id;
update performance_details set status=1
where appraisal_form_id=stdappraisal_form_id;
update hash_table set hash=new_hash
where email=user_email;
update endofyear_review set submit=1
where appraisal_form_id=stdappraisal_form_id;
update performance_details set submit=1
where appraisal_form_id=stdappraisal_form_id;

else 
select '[]'::character varying;
end if;
end if;
return 'Form Approved';
	   end;
$$;


--
-- Name: approve_mid_form_details(integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.approve_mid_form_details(stdappraisal_form_id integer, stdremarks character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
user_email character varying;
verified bool;
vstaff_id integer;
 approved integer;
 new_hash character varying;
 mid integer;
begin

select exists(select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id) into verified;
select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id into vstaff_id;
select email from staff where staff_id=vstaff_id  into user_email;

select mid_status from public.view_users_form_details where  appraisal_form_id=stdappraisal_form_id and mid_status=1 into mid;

select hash from hash_table where email=user_email into new_hash;
sELECT public.generate_hash() into new_hash;

perform *FROM public.view_users_form_details;
update midyear_review set mid_status=1
where appraisal_form_id=stdappraisal_form_id;
update midyear_review set midyear_review_status=0
where appraisal_form_id=stdappraisal_form_id;
update hash_table set hash=new_hash
where email=user_email;
UPDATE public.midyear_review
	SET remarks=stdremarks
	WHERE appraisal_form_id=stdappraisal_form_id;
update midyear_review set submit=1
where appraisal_form_id=stdappraisal_form_id;
return 'Form Approved';
	   end;
$$;


--
-- Name: assessments(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.assessments(stdappraisal_form_id integer, stdtype integer) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
declare

cal float;
core float;
non_core float;
begin

if  stdtype=1 then
select avg(score)
	FROM vw_competency
	where category = 'Core' AND appraisal_form_id = stdappraisal_form_id into cal;

elsif stdtype=2 then
select avg(score)
	FROM vw_competency
	where category = 'None Core' AND appraisal_form_id = stdappraisal_form_id into cal;

else 
select '[]'::character varying;
end if;
return cal;
	   end;
$$;


--
-- Name: create_appraisal_form_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.create_appraisal_form_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO appraisal_form(staff_id)

         VALUES(NEW.staff_id,old.staff_id);
RETURN NEW;

END;
$$;


--
-- Name: date_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.date_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO appraisal_form(date)

         VALUES(NEW.appointment);
RETURN NEW;

END;
$$;


--
-- Name: deactivate_staff(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.deactivate_staff(stdstaff_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
verified bool;
user_email character varying;
status integer;
begin

select exists(select staff_id from staff where staff_id=stdstaff_id) into verified;
select email from staff where staff_id=stdstaff_id  into user_email;
select staff_id from staff where staff_id=stdstaff_id and staff_status=0 into status;

if  verified ='false'
then 
return 'STAFF NOT FOUND';
 
 elsif status=stdstaff_id
then 
return 'STAFF ALREADY DEACTIVATED';


elsif verified='true'
then
UPDATE public.staff
	SET  staff_status=0
	WHERE staff_id=stdstaff_id;
	update hash_table set hash = NULL
where email=user_email;


else
select '[]'::character varying;

end if;

return 'STAFF DEACTIVATED';
	   end;
$$;


--
-- Name: deadline(character varying, date, date, bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.deadline(stddeadline_type character varying, stdstart date, stdending date, stddeadline_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.deadline(deadline_type,start_date,ending)
values(stddeadline_type,stdstart,stdending)
;

return 'inserted successfully';
end;
$$;


--
-- Name: delete_annual_plan(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_plan(stdannual_plan_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_plan
where staff_id=stdannual_plan_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_appraisal_form(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_appraisal_form(stdappraisal_form_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from appraisal_form
where staff_id=stdappraisal_form_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_midyear_review(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_midyear_review(stdmidyear_review_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from midyear_review
where staff_id=stdmidyear_review_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_staff(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_staff(stdstaff_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from staff
where staff_id=stdstaff_id;
return 'Deleted';
	   end;
$$;


--
-- Name: disapprove_competency_details(integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.disapprove_competency_details(stdappraisal_form_id integer, stdcompetency_id integer, stdcomments character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
verified bool;
vstaff_id integer;
 approved integer;
 id_verified integer;
begin

select exists(select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id) into verified;
select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id into vstaff_id;
select competency_id from competency_details where appraisal_form_id=stdappraisal_form_id into id_verified;

perform *FROM public.competency_details;
update competency_details set disapprove_status=1
where appraisal_form_id=stdappraisal_form_id and competency_id=stdcompetency_id;

update competency_details set status=0
where appraisal_form_id=stdappraisal_form_id and competency_id=stdcompetency_id;

insert  into public.disapprove_competency_comment(appraisal_form_id,comments, competency_id)
values(stdappraisal_form_id,stdcomments, stdcompetency_id) on conflict (competency_id,appraisal_form_id) do update set comments=stdcomments;
UPDATE public.competency_details
	SET disapprove_comments=stdcomments
	WHERE appraisal_form_id=stdappraisal_form_id and competency_id=stdcompetency_id;
return 'Form Disapproved';
	   end;
$$;


--
-- Name: disapprove_form_details(integer, character varying, character); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.disapprove_form_details(stdappraisal_form_id integer, stdtype_form character varying, stdcomment character) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
user_email character varying;
verified bool;
vstaff_id integer;
 disapproved integer;
 mid integer;
begin

select exists(select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id) into verified;
select staff_id from appraisal_form where appraisal_form_id=stdappraisal_form_id into vstaff_id;
select email from staff where staff_id=vstaff_id  into user_email;
select submit from annual_plan where appraisal_form_id=stdappraisal_form_id and annual_plan_status=1 into disapproved; 
select submit from midyear_review where appraisal_form_id=stdappraisal_form_id and midyear_review_status=1 into mid; 

if verified='false'
then 
return 'Form Not Found';

--elsif disapproved =1
--then 
--return'Form Already Disapproved';

--elsif  mid=1
--then 
--return'Form Already Disapproved';

elsif verified='true' 
then

if  stdtype_form='Start'then
perform * FROM public.vw_annual_plan;
update annual_plan set annual_plan_status=1
where appraisal_form_id=stdappraisal_form_id;
update annual_plan set submit=0
where appraisal_form_id=stdappraisal_form_id;
update annual_plan set start_status=0
where appraisal_form_id=stdappraisal_form_id;
insert into public.supervisor_comment(appraisal_form_id,annual_plan_comment)
values(stdappraisal_form_id,stdcomment) on conflict(appraisal_form_id) do update set annual_plan_comment = stdcomment;

elsif stdtype_form='Mid'then
perform * FROM public.vw_midyear_review;
update midyear_review set midyear_review_status=1
where appraisal_form_id=stdappraisal_form_id;
update midyear_review set submit=0
where appraisal_form_id=stdappraisal_form_id;
update midyear_review set mid_status=0
where appraisal_form_id=stdappraisal_form_id;
insert  into public.supervisor_comment(appraisal_form_id,midyear_review_comment)
values(stdappraisal_form_id,stdcomment) on conflict(appraisal_form_id) do update set midyear_review_comment = stdcomment;
UPDATE public.midyear_review
	SET remarks=stdcomment
	WHERE appraisal_form_id=stdappraisal_form_id;

elsif  stdtype_form='End'then
perform * FROM public.vw_endofyear_review;
update endofyear_review set endyear_review_status=1
where appraisal_form_id=stdappraisal_form_id;
update endofyear_review set submit=0
where appraisal_form_id=stdappraisal_form_id;
update performance_details set submit=0
where appraisal_form_id=stdappraisal_form_id;
update endofyear_review set end_status=0
where appraisal_form_id=stdappraisal_form_id;
insert  into public.supervisor_comment(appraisal_form_id,endofyear_review)
values(stdappraisal_form_id,stdcomment) on conflict(appraisal_form_id) do update set endofyear_review = stdcomment;


else 
select '[]'::character varying;
end if;
end if;
return 'Form Disapproved';
	   end;
$$;


--
-- Name: email_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.email_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
--   NEW.staff."Email" := NEW.hash."email";
INSERT INTO hash_table(email)

         VALUES(NEW.email);
RETURN NEW;

END;
$$;


--
-- Name: function_copy(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.function_copy() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO
        table2(id,name)
        VALUES(new.id,new.name);

           RETURN new;
END;
$$;


--
-- Name: generate_hash(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hash() RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
   ddate date;
  hash character varying;
BEGIN
    select start_date from deadline into ddate where start_date=start_date;
  if not found then
  raise notice'date mismatch';	  		
else  select md5(''||now()::text||random()::text) into hash;
  end if;
    RETURN hash;
END;
$$;


--
-- Name: get_annual_plan(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_annual_plan() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare annual_plan_details jsonb;
begin
select json_agg (annual_plan) from annual_plan into annual_plan_details ;

return annual_plan_details;
	   end;
$$;


--
-- Name: get_appraisal_form(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_appraisal_form() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare appraisal_form_details jsonb;
begin
select json_agg (appraisal_form) from appraisal_form into appraisal_form_details  ;
return appraisal_form_details;
	   end;
$$;


--
-- Name: get_deadline(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_deadline() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare deadline_details jsonb;
begin
select json_agg ( deadline) from deadline into deadline_details;
 
return deadline_details;
	   end;
$$;


--
-- Name: get_entire_hash_table(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_entire_hash_table() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare hash_email jsonb;
begin
select json_agg(hash_table) from hash_table into hash_email;
return hash_email;
	   end;
$$;


--
-- Name: get_form_details_yearly(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_form_details_yearly(vstaff_id integer, vform_year integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare results jsonb; 
begin
SELECT json_agg (form_details) FROM (
SELECT
	appraisal_form.appraisal_form_id,
	extract(year from appraisal_form.date) as appraisal_year,
	staff.fname as firstname,
	staff.sname as lastname,
	staff.oname as middlename,
	staff.email,
	staff.gender,
	staff.appointment,
	yearly_details.department,
	yearly_details.position,
	yearly_details.grade,	
	annual_plan.result_areas,
	annual_plan.target,
	annual_plan.resources,
	annual_plan.start_status as approve,
	annual_plan.submit as save,
	annual_plan.annual_plan_status as disapprove,
	midyear_review.progress_review,
	midyear_review.remarks,
	midyear_review.competency,
	midyear_review.mid_status,
	endofyear_review.end_status,
	endofyear_review.average_per_rating,
	endofyear_review.average_total,
	endofyear_review.average_per_rating_id,
	endofyear_review.appraisers_comment_on_workplan,
	endofyear_review.training_development_comments,
	endofyear_review.appraisees_comments_and_plan,
	endofyear_review.head_of_divisions_comments,
	competency_details.grade,
	competency_details.competency_id,
	competency_details.id,
	performance_details.id,
	performance_details.weight,
	performance_details.comments,
	performance_details.final_score,
	performance_details.approved_date,
	performance_details.p_a AS performance_assessments,
	training_received.programme AS training_received_programme,
	training_received.institution AS training_receied_institution,
	training_received.date AS training_received_date

		
FROM
	staff 
INNER JOIN appraisal_form  
    ON appraisal_form.staff_id =staff.staff_id
INNER JOIN yearly_details  
    ON yearly_details.staff_id =staff.staff_id	
	LEFT JOIN annual_plan  
    ON annual_plan.appraisal_form_id  = appraisal_form.appraisal_form_id
	LEFT JOIN midyear_review  
    ON midyear_review.appraisal_form_id  = appraisal_form.appraisal_form_id
	LEFT JOIN endofyear_review  
    ON endofyear_review.appraisal_form_id=appraisal_form.appraisal_form_id
	left join 	competency_details
	on 	competency_details.appraisal_form_id=appraisal_form.appraisal_form_id
	left join 	performance_details
	on 	performance_details.appraisal_form_id=appraisal_form.appraisal_form_id
	left join 	training_received
	on 	training_received.appraisal_form_id=appraisal_form.appraisal_form_id
	
	WHERE staff.staff_id=vstaff_id
	AND 
	(appraisal_form.date is null 
	OR extract(year from appraisal_form.date) = vform_year
	 )
	AND extract(year from yearly_details.year)=vform_year
)form_details into results; 
RETURN results;	
	   end;
$$;


--
-- Name: get_hash_verification(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_hash_verification(stdhash character varying) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare
vstaff_id integer;
verified bool;
user_email character varying;
user_details jsonb;
begin
select exists(select email from hash_table where hash=stdhash) into verified;
if verified='true' 
then
select email from hash_table where hash=stdhash into user_email;
select staff_id into vstaff_id from staff where email=user_email;

select get_form_details_yearly(vstaff_id,  extract (year from now())::integer) into user_details;
else
select '[]'::jsonb 
into user_details;
end if;

return user_details;
	   end;
$$;


--
-- Name: get_list_of_appraisee(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_appraisee(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_appraisee jsonb;
declare user_role integer ;
begin
select roles into user_role from staff where staff_id = user_id;
if user_role=1 then
select json_agg (staff) from staff into list_appraisee;
elsif user_role=2 then
select json_agg (staff) from staff where supervisor=user_id into list_appraisee;
else 
select '[]'::jsonb into list_appraisee;
end if;
return list_appraisee;
end;
$$;


--
-- Name: get_list_of_appraisee_commented(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_appraisee_commented(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_appraisee_commented jsonb;
user_role integer;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;


if user_role=1 then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( appraisees_comments_and_plan is not null and appraisal_comment_on_workplan is null ) )
results into list_of_appraisee_commented;
elsif user_role=2 then
select json_agg (results) from (select * from view_users_form_details
where(appraisees_comments_and_plan is not null and appraisal_comment_on_workplan is null)
and supervisor=user_id) results into list_of_appraisee_commented;




else 
select '[]'::jsonb into list_of_appraisee_commented;

end if;
return list_of_appraisee_commented;
end;

$$;


--
-- Name: get_list_of_appraisees_not_commented(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_appraisees_not_commented(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_appraisee_not_commented jsonb;
user_role integer;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;


if user_role=1 then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( appraisees_comments_and_plan is null ) )
results into list_of_appraisee_not_commented;
elsif user_role=2 then
select json_agg (results) from (select * from view_users_form_details
where(appraisees_comments_and_plan is null)
and supervisor=user_id) results into list_of_appraisee_not_commented;




else 
select '[]'::jsonb into list_of_appraisee_not_commented;

end if;
return list_of_appraisee_not_commented;
end;

$$;


--
-- Name: get_list_of_appraisers_commented(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_appraisers_commented(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_appraisers_commented jsonb;
user_role integer;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;


if user_role=1 then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( appraisal_comment_on_workplan is not null and head_of_divisions_comments is null ) )
results into list_of_appraisers_commented;
elsif user_role=2 then
select json_agg (results) from (select * from view_users_form_details
where(appraisal_comment_on_workplan is not null and head_of_divisions_comments is null)
and supervisor=user_id) results into list_of_appraisers_commented;




else 
select '[]'::jsonb into list_of_appraisers_commented;

end if;
return list_of_appraisers_commented;
end;

$$;


--
-- Name: get_list_of_appraisers_not_commented(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_appraisers_not_commented(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_appraisers_not_commented jsonb;
user_role integer;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;


if user_role=1 then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( appraisal_comment_on_workplan is null ) )
results into list_of_appraisers_not_commented;
elsif user_role=2 then
select json_agg (results) from (select * from view_users_form_details
where(appraisal_comment_on_workplan is null)
and supervisor=user_id) results into list_of_appraisers_not_commented;




else 
select '[]'::jsonb into list_of_appraisers_not_commented;

end if;
return list_of_appraisers_not_commented;
end;

$$;


--
-- Name: get_list_of_approved_form(character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_approved_form(stddeadline character varying, user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_approved_form jsonb;
user_role integer;
section_type character varying;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;
select deadline_type into section_type from deadline where deadline_type=stddeadline;

if user_role=1 and stddeadline='Start'then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( start_status=1 ) )
results into list_of_approved_form;
elsif user_role=2 and stddeadline='Start' then
select json_agg (results) from (select * from view_users_form_details
where(start_status=1)
and supervisor=user_id) results into list_of_approved_form;

elsif user_role=1 and stddeadline='Mid'then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( mid_status=1 ) )
results into list_of_approved_form;
elsif user_role=2 and stddeadline='Mid' then
select json_agg (results) from (select * from view_users_form_details
where(mid_status=1)
and supervisor=user_id) results into list_of_approved_form;

elsif user_role=1 and stddeadline='End'then
select json_agg (results) from (select * from view_users_form_details
where ( end_status=1 ))
results into list_of_approved_form;
elsif user_role=2 and stddeadline='End' then
select json_agg (results) from (select * from view_users_form_details
where (end_status=1) 
and supervisor=user_id) results into list_of_approved_form;

else 
select '[]'::jsonb into list_of_approved_form;

end if;
return list_of_approved_form;
end;
$$;


--
-- Name: get_list_of_disapproved_form(character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_disapproved_form(stddeadline character varying, user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_disapproved_form jsonb;
user_role integer;
section_type character varying;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;
select deadline_type into section_type from deadline where deadline_type=stddeadline;

if user_role=1 and stddeadline='Start'then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( annual_plan_status=1 ) )
results into list_of_disapproved_form;
elsif user_role=2 and stddeadline='Start' then
select json_agg (results) from (select * from view_users_form_details
where(annual_plan_status=1)
and supervisor=user_id) results into list_of_disapproved_form;

elsif user_role=1 and stddeadline='Mid'then
select json_agg (results) from (SELECT * FROM public.view_users_form_details  
where ( mid_status=0 ) )
results into list_of_disapproved_form;
elsif user_role=2 and stddeadline='Mid' then
select json_agg (results) from (select * from public.view_users_form_details  
where(mid_status=0)
and supervisor=user_id) results into list_of_disapproved_form;

elsif user_role=1 and stddeadline='End'then
select json_agg (results) from (SELECT * FROM view_users_form_details
where ( end_status=0 ))
results into list_of_disapproved_form;
elsif user_role=2 and stddeadline='End' then
select json_agg (results) from (select * from view_users_form_details
where (  end_status=0  ) 
and supervisor=user_id) results into list_of_disapproved_form;

else 
select '[]'::jsonb into list_of_disapproved_form;

end if;
return list_of_disapproved_form;
end;
$$;


--
-- Name: get_list_of_final_completed(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_final_completed(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_final_completed jsonb;
user_role integer;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;


if user_role=1 then
select json_agg (results) from (SELECT * FROM view_users_form_details  
where ( appraisees_comments_and_plan is not null and appraisal_comment_on_workplan is not null and head_of_divisions_comments is not null and training_development_comments is not null) )
results into list_of_final_completed;
elsif user_role=2 then
select json_agg (results) from (select * from view_users_form_details
where(appraisees_comments_and_plan is not null and appraisal_comment_on_workplan is not null and head_of_divisions_comments is not null and training_development_comments is not null)
and supervisor=user_id) results into list_of_final_completed;




else 
select '[]'::jsonb into list_of_final_completed;

end if;
return list_of_final_completed;
end;

$$;


--
-- Name: get_list_of_hod_commented(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_hod_commented(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_hod_commented jsonb;
user_role integer;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;


if user_role=1 then
select json_agg (results) from (SELECT view_users_form_details.appraisal_form_id, view_users_form_details.firstname, view_users_form_details.lastname, view_users_form_details.middlename, view_users_form_details.email, view_users_form_details.gender, view_users_form_details.staff_id, view_users_form_details.supervisor, view_users_form_details.supervisor_fname,view_users_form_details.supervisor_oname,view_users_form_details.supervisor_sname, view_users_form_details.supervisor_email, view_users_form_details.roles, view_users_form_details.role_description, view_users_form_details.department, view_users_form_details.positions, view_users_form_details.grade, view_users_form_details.result_areas, view_users_form_details.target, view_users_form_details.resources, view_users_form_details.start_status, view_users_form_details.submit, view_users_form_details.annual_plan_status, view_users_form_details.annual_plan_comment, view_users_form_details.progress_review, view_users_form_details.remarks, view_users_form_details.midyear_review_status, view_users_form_details.competency, mid_status, view_users_form_details.midyear_review_comment, view_users_form_details.end_status, view_users_form_details.average_per_rating, view_users_form_details.average_total, view_users_form_details.average_per_rating_id, view_users_form_details.appraisal_comment_on_workplan, view_users_form_details.training_development_comments, view_users_form_details.core_assessments, view_users_form_details.non_core_assessments, view_users_form_details.appraisees_comments_and_plan, view_users_form_details.head_of_divisions_comments, view_users_form_details.endofyear_review, view_users_form_details.performance_assessment, view_users_form_details.overall_total, view_users_form_details.overall_performance_rating, view_end.appraisal_form_id, view_end.comments, view_end.status, view_end.approved_date, view_end.submit, view_end.weight, view_end.final_score, view_end.performance_details_id, performance_details.p_a
	FROM public.view_users_form_details inner join public.view_end on view_users_form_details.appraisal_form_id=view_end.appraisal_form_id inner join public.performance_details on view_users_form_details.appraisal_form_id=performance_details.appraisal_form_id   
where(view_users_form_details.head_of_divisions_comments is not null ) )
results into list_of_hod_commented;
elsif user_role=2 then
select json_agg (results) from (SELECT view_users_form_details.appraisal_form_id, view_users_form_details.firstname, view_users_form_details.lastname, view_users_form_details.middlename, view_users_form_details.email, view_users_form_details.gender, view_users_form_details.staff_id, view_users_form_details.supervisor, view_users_form_details.supervisor_fname,view_users_form_details.supervisor_oname,view_users_form_details.supervisor_sname, view_users_form_details.supervisor_email, view_users_form_details.roles, view_users_form_details.role_description, view_users_form_details.department, view_users_form_details.positions, view_users_form_details.grade, view_users_form_details.result_areas, view_users_form_details.target, view_users_form_details.resources, view_users_form_details.start_status, view_users_form_details.submit, view_users_form_details.annual_plan_status, view_users_form_details.annual_plan_comment, view_users_form_details.progress_review, view_users_form_details.remarks, view_users_form_details.midyear_review_status, view_users_form_details.competency, mid_status, view_users_form_details.midyear_review_comment, view_users_form_details.end_status, view_users_form_details.average_per_rating, view_users_form_details.average_total, view_users_form_details.average_per_rating_id, view_users_form_details.appraisal_comment_on_workplan, view_users_form_details.training_development_comments, view_users_form_details.core_assessments, view_users_form_details.non_core_assessments, view_users_form_details.appraisees_comments_and_plan, view_users_form_details.head_of_divisions_comments, view_users_form_details.endofyear_review, view_users_form_details.performance_assessment, view_users_form_details.overall_total, view_users_form_details.overall_performance_rating, view_end.appraisal_form_id, view_end.comments, view_end.status, view_end.approved_date, view_end.submit, view_end.weight, view_end.final_score, view_end.performance_details_id, performance_details.p_a
	FROM public.view_users_form_details inner join public.view_end on view_users_form_details.appraisal_form_id=view_end.appraisal_form_id inner join public.performance_details on view_users_form_details.appraisal_form_id=performance_details.appraisal_form_id   
where(view_users_form_details.head_of_divisions_comments is not null )
and supervisor=user_id) results into list_of_hod_commented;

else 
select '[]'::jsonb into list_of_hod_commented;

end if;
return list_of_hod_commented;
end;

$$;


--
-- Name: get_list_of_incompleted_form(character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_incompleted_form(stddeadline character varying, user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_incompleted_form jsonb;
user_role integer;
section_type character varying;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;
select deadline_type into section_type from deadline where deadline_type=stddeadline;

if user_role=1 and 
stddeadline='Start'then
select json_agg (results) from (SELECT * FROM public.view_users_form_details  
where (submit=0 or submit is null ))
	results into list_incompleted_form;
elsif user_role=2 and 
stddeadline='Start' then
select json_agg (results) from (select * from public.view_users_form_details
where(submit=0 or submit is null)
and supervisor=user_id) results into list_incompleted_form;

elsif user_role=1 and 
stddeadline='Mid'then
select json_agg (results) from (SELECT * FROM public.view_mid  
where (submit=0 or submit is null and appraisal_form_id is not null))
	results into list_incompleted_form;
elsif user_role=2 and 
stddeadline='Mid' then
select json_agg (results) from (select * from public.view_mid
where(submit=0 or submit is null and appraisal_form_id is not null)
and supervisor=user_id) results into list_incompleted_form;

elsif user_role=1 and stddeadline='End'then
select json_agg (results) from (select * FROM public.view_end
where (submit=0 or submit is null and appraisal_form_id is not null) ) results into list_incompleted_form;
elsif user_role=2 and stddeadline='End' then
select json_agg (results) from (select * FROM public.view_end
where (submit=0 or submit is null and appraisal_form_id is not null) 
and supervisor=user_id) results into list_incompleted_form;

else 
select '[]'::jsonb into list_incompleted_form;

end if;
return list_incompleted_form;
end;
$$;


--
-- Name: get_list_of_waiting_approval(character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_waiting_approval(stddeadline character varying, user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_of_waiting_approval jsonb;
user_role integer;
section_type character varying;
staff_role integer;
begin
select roles into user_role from staff where staff_id = user_id;
-- select role_id into user_role from roles where role_id=user_role;
select deadline_type into section_type from deadline where deadline_type=stddeadline;

if user_role=1 and stddeadline='Start' then
select json_agg (results) from (SELECT * FROM view_start 
where (target is not null and  resources is not null and result_areas is not null and start_status=0 and submit=1)) 
results into list_of_waiting_approval;
elsif user_role=2 and stddeadline='Start' then
select json_agg (results) from (select * from view_start
where( target is not null and  resources is not null and result_areas is not null and start_status=0 and submit=1)
and supervisor=user_id) results into list_of_waiting_approval;

elsif user_role=1 and stddeadline='Mid' then
select json_agg (results) from (SELECT * FROM view_mid 
where (progress_review is not null and competency is not null and mid_status=0 and submit=1)) 
results into list_of_waiting_approval;
elsif user_role=2 and stddeadline='Mid' then
select json_agg (results) from (select * from view_mid
where( progress_review is not null and   competency is not null and mid_status=0 and submit=1)
and supervisor=user_id) results into list_of_waiting_approval;

elsif user_role=1 and stddeadline='End' then
select json_agg (results) from ((select * from view_end
where ( comments is  not null  and weight is not  null and final_score is not  null and submit=1 and status=0 )))
results into list_of_waiting_approval;
elsif user_role=2 and stddeadline='End' then
select json_agg (results) from (select * from view_end
where ( comments is  not null  and weight is not  null and final_score is not  null and submit=1 and status=0) 
and supervisor=user_id) results into list_of_waiting_approval;

else 
select '[]'::jsonb into list_of_waiting_approval;

end if;
return list_of_waiting_approval;
end;
$$;


--
-- Name: get_staff(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_staff() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare staff_details jsonb;
begin
select json_agg ( id) from view_staff_details into staff_details;
 
return staff_details;
	   end;
$$;


--
-- Name: get_view_supervisors(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_view_supervisors() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare supervisor_details jsonb;
begin

select json_object_agg (Appraiser,Appraisee order by Appraiser)
from(
	select Appraiser,json_agg(Appraisee) Appraisee
from public.vw_supervisor into supervisor_details group by 1 ) s;
 
return supervisor_details;
	   end;
$$;


--
-- Name: midyear_review(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.midyear_review(stdremarks character varying, stdprogress_review character varying, stdcompetency character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.midyear_review(progress_review,remarks,competency)
values(stdremarks,stdtarget,stdprogress_review,stdcompetency);
return 'inserted successfully';
end;
$$;


--
-- Name: midyear_review(character varying, character varying, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.midyear_review(stdprogress_review character varying, stdremarks character varying, stdmid_status integer, stdappraisal_form_id integer, stdannual_plan_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.midyear_review(progress_review,remarks,mid_status,appraisal_form_id,annual_plan_id)
values(stdprogress_review,stdremarks,stdmid_status,stdappraisal_form_id,stdannual_plan_id);
return 'inserted successfully';
end;
$$;


--
-- Name: overall_performance_rating(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.overall_performance_rating(stdappraisal_form_id integer) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
declare

cal float;
core float;
non_core float;
begin

select ((sum(score)::float)/5) * 10
FROM vw_competency where appraisal_form_id = stdappraisal_form_id into cal;

return cal;
	   end;
$$;


--
-- Name: overall_total(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.overall_total(stdappraisal_form_id integer) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
declare

cal float;
core float;
non_core float;
begin

select core_assessments + non_core_assessments + performance_assessment
FROM public.vw_endofyear_review
 where appraisal_form_id = stdappraisal_form_id into cal;

return cal;
	   end;
$$;


--
-- Name: performance_assessment(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.performance_assessment(stdappraisal_form_id integer) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
declare

cal float;
core float;
non_core float;
begin

select avg(score)*0.6
FROM vw_competency where appraisal_form_id = stdappraisal_form_id into cal;

return cal;
	   end;
$$;


--
-- Name: reactivate_staff(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.reactivate_staff(stdstaff_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
verified bool;
user_email character varying;
status integer;
new_hash character varying;
begin

select exists(select staff_id from staff where staff_id=stdstaff_id) into verified;
select email from staff where staff_id=stdstaff_id  into user_email;
select staff_id from staff where staff_id=stdstaff_id and staff_status=1 into status;
sELECT public.generate_hash() into new_hash;

if  verified ='false'
then 
return 'STAFF NOT FOUND';
 
 elsif status=stdstaff_id
then 
return 'STAFF ALREADY REACTIVATED';

elsif verified='true'
then
UPDATE public.staff
	SET  staff_status=1
	WHERE staff_id=stdstaff_id;
	update hash_table set hash =new_hash
where email=user_email;

else
select '[]'::character varying;

end if;

return 'STAFF REACTIVATED';
	   end;
$$;


--
-- Name: staff_id_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.staff_id_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO appraisal_form(staff_id)

         VALUES(NEW.staff_id);
RETURN NEW;

END;
$$;


--
-- Name: sup_all_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.sup_all_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO public.users(staff_id,email,user_type_id)

         VALUES(new.staff_id,NEW.email,new.roles);
RETURN NEW;

END;
$$;


--
-- Name: update_all_status(integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_all_status(stdannual_plan_id integer, stddeadline_status character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
if stddeadline_status='start_status'then
perform *FROM public.vw_annual_appraisal;
update annual_plan set start_status=1
where target is not null and resources is not null and result_areas is not null;

elsif stddeadline_status='mid_status'then
perform *FROM public.vw_midyear_review;
update midyear_review set mid_status=1
where progress_review is not null and remarks is not null;

elsif stddeadline_status='end_status'then
perform *FROM public.vw_endofyear_review;
update endofyear_review set end_status=1
where assessment is not null and score is not null and comment is not null and weight is not null;

else 
select '[]'::jsonb;
end if;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_annual_plan(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_plan(stdresult_areas character varying, stdtarget character varying, stdresources character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE  annual_plan
    SET result_areas = stdresult_areas, 
       target = stdtarget, 
       resources = resources
 
    WHERE   annual_plan_id = annual_plan_id; 
END;
$$;


--
-- Name: update_appraisal_form(character varying, character varying, integer, character varying, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_appraisal_form(appraisal_form_id character varying, stddepartment character varying, stdgrade integer, stdpositions character varying, stddate date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE  annual_plan                                         
    SET department = stddepartment, 
      grade = stdgrade, 
       positions = stdpostion
	  
 
    WHERE  appraisal_form_id=stdappraisal_form_id ; 
	return 'Appraisal Form Updated';
END;
$$;


--
-- Name: update_deadline(bigint, date, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_deadline(stddeadline_id bigint, stdstart_date date, ending date) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE  annual_plan
    SET start_date = stdstart_date, 
       ending = stdending
 
    WHERE   deadline_id = stddeadline_id; 
END;
$$;


--
-- Name: update_staff(integer, character varying, character varying, character varying, character varying, character varying, integer, character varying, character varying, integer, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_staff(stdstaff_id integer, stdfname character varying, stdsname character varying, stdoname character varying, stdgender character varying, stdemail character varying, stdsupervisor integer, stddepartment character varying, stdpositions character varying, stdgrade integer, stdappointment date, stdroles integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE  staff
    SET fname = stdfname,            
       sname = stdsname,
	   oname=stdoname,
	   email=stdemail,
      gender = stdgender,
 	supervisor=stdsupervisor ,
	department= stddepartment,
	positions= stdpositions,
	grade= stdgrade,
	appointment=stdappointment,
	roles=stdroles
    WHERE   staff_id = stdstaff_id; 
return 'Staff Updated';
END;

$$;


--
-- Name: yearly_details(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.yearly_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	
		 INSERT INTO "yearly_details"("department","grade","position","staff_id")
		 VALUES(new."department",new."grade",new."positions",new."staff_id");

	RETURN NEW;
END;
$$;


--
-- Name: annual_appraisal_annual_appraisal_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.annual_appraisal_annual_appraisal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: annual_appraisal; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annual_appraisal (
    comment character varying,
    field character varying,
    appraisal_form_id integer NOT NULL,
    status integer DEFAULT 0,
    annual_appraisal_id bigint DEFAULT nextval('public.annual_appraisal_annual_appraisal_id_seq'::regclass) NOT NULL
);


--
-- Name: annual_plan_annual_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.annual_plan_annual_plan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: annual_plan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annual_plan (
    result_areas character varying,
    target character varying,
    resources character varying,
    appraisal_form_id integer,
    annual_plan_id bigint DEFAULT nextval('public.annual_plan_annual_plan_id_seq'::regclass) NOT NULL,
    start_status integer DEFAULT 0,
    submit integer,
    annual_plan_status integer DEFAULT 0
);


--
-- Name: appraisal_form; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appraisal_form (
    department character varying,
    grade integer,
    positions character varying,
    appraisal_form_id bigint NOT NULL,
    date date DEFAULT now(),
    staff_id integer NOT NULL
);


--
-- Name: appraisal_form_appraisal_form_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.appraisal_form_appraisal_form_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: appraisal_form_appraisal_form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.appraisal_form_appraisal_form_id_seq OWNED BY public.appraisal_form.appraisal_form_id;


--
-- Name: competency; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.competency (
    category character varying,
    sub character varying NOT NULL,
    main character varying,
    weight double precision,
    competency_id bigint
);


--
-- Name: competency_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.competency_details (
    id bigint NOT NULL,
    competency_id integer NOT NULL,
    appraisal_form_id integer NOT NULL,
    status integer DEFAULT 0,
    grade integer,
    submit integer DEFAULT 1,
    disapprove_status integer DEFAULT 0,
    disapprove_comments character varying
);


--
-- Name: competency_details_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.competency_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: competency_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.competency_details_id_seq OWNED BY public.competency_details.id;


--
-- Name: deadline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deadline (
    deadline_type character varying NOT NULL,
    start_date date,
    ending date NOT NULL,
    deadline_id bigint NOT NULL
);


--
-- Name: deadline_deadline_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.deadline_deadline_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: deadline_deadline_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.deadline_deadline_id_seq OWNED BY public.deadline.deadline_id;


--
-- Name: department_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.department_type (
    id integer NOT NULL,
    title character varying
);


--
-- Name: department_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.department_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: department_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.department_type_id_seq OWNED BY public.department_type.id;


--
-- Name: disapprove_competency_comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.disapprove_competency_comment (
    appraisal_form_id integer,
    competency_id integer,
    comments character varying
);


--
-- Name: endofyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.endofyear_review (
    appraisal_form_id integer,
    endofyear_review_id bigint NOT NULL,
    performance_details_id bigint,
    end_status integer DEFAULT 0,
    average_per_rating integer,
    average_total integer,
    average_per_rating_id bigint,
    appraisers_comment_on_workplan character varying,
    training_development_comments character varying,
    submit integer DEFAULT 1,
    endyear_review_status integer DEFAULT 0,
    appraisees_comments_and_plan character varying,
    head_of_divisions_comments character varying
);


--
-- Name: endofyear_review_endofyear_review_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.endofyear_review_endofyear_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: endofyear_review_endofyear_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.endofyear_review_endofyear_review_id_seq OWNED BY public.endofyear_review.endofyear_review_id;


--
-- Name: form_completion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form_completion (
    form_completion_id bigint NOT NULL,
    appraisal_id integer,
    date date,
    status integer
);


--
-- Name: form_completion_form_completion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.form_completion_form_completion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: form_completion_form_completion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.form_completion_form_completion_id_seq OWNED BY public.form_completion.form_completion_id;


--
-- Name: hash_table; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hash_table (
    hash character varying(1000) DEFAULT public.generate_hash(),
    email character varying NOT NULL,
    hash_table_id bigint NOT NULL
);


--
-- Name: hash_table_hash_table_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hash_table_hash_table_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hash_table_hash_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hash_table_hash_table_id_seq OWNED BY public.hash_table.hash_table_id;


--
-- Name: midyear_review_midyear_review_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.midyear_review_midyear_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: midyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.midyear_review (
    midyear_review_id bigint DEFAULT nextval('public.midyear_review_midyear_review_id_seq'::regclass) NOT NULL,
    progress_review character varying,
    remarks character varying,
    mid_status integer DEFAULT 0,
    appraisal_form_id integer,
    competency character varying,
    submit integer DEFAULT 1,
    midyear_review_status integer DEFAULT 0
);


--
-- Name: overall_performance; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.overall_performance (
    id bigint NOT NULL,
    description character varying,
    performance character varying
);


--
-- Name: overall performance_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."overall performance_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: overall performance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."overall performance_id_seq" OWNED BY public.overall_performance.id;


--
-- Name: overall_assessment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.overall_assessment (
    aprpaisal_form_id bigint,
    performance_assessment_score integer,
    core_assessment_score integer,
    non_core_assessment_score integer,
    overall_total_score integer,
    overall_performance_rating integer
);


--
-- Name: performance_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.performance_details (
    id bigint NOT NULL,
    appraisal_form_id integer,
    comments character varying,
    status integer DEFAULT 0,
    approved_date date,
    submit integer DEFAULT 0,
    weight character varying,
    final_score character varying,
    performance_details_id integer,
    p_a character varying
);


--
-- Name: performance_details_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.performance_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: performance_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.performance_details_id_seq OWNED BY public.performance_details.id;


--
-- Name: reset_password_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reset_password_codes (
    id integer NOT NULL,
    code character varying,
    user_id integer,
    user_email character varying,
    status boolean NOT NULL,
    date_created timestamp without time zone,
    date_modified timestamp without time zone
);


--
-- Name: reset_password_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reset_password_codes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reset_password_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reset_password_codes_id_seq OWNED BY public.reset_password_codes.id;


--
-- Name: reset_password_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reset_password_token (
    id integer NOT NULL,
    user_id integer,
    token character varying,
    date_created timestamp without time zone
);


--
-- Name: reset_password_token_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reset_password_token_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reset_password_token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reset_password_token_id_seq OWNED BY public.reset_password_token.id;


--
-- Name: revoked_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.revoked_tokens (
    id integer NOT NULL,
    jti character varying,
    date_created timestamp without time zone,
    date_modified timestamp without time zone
);


--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.revoked_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.revoked_tokens_id_seq OWNED BY public.revoked_tokens.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_description character varying NOT NULL
);


--
-- Name: save_annual_plan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.save_annual_plan (
    result_areas character varying,
    target character varying,
    resources character varying,
    appraisal_form_id integer
);


--
-- Name: staff; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staff (
    staff_id bigint NOT NULL,
    fname character varying NOT NULL,
    sname character varying NOT NULL,
    oname character varying,
    email character varying NOT NULL,
    supervisor integer,
    gender character varying NOT NULL,
    department character varying,
    positions character varying,
    grade integer,
    appointment date,
    roles integer,
    staff_status integer DEFAULT 1
);


--
-- Name: staff_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.staff_staff_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: staff_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.staff_staff_id_seq OWNED BY public.staff.staff_id;


--
-- Name: supervisor_comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.supervisor_comment (
    annual_plan_comment character varying,
    midyear_review_comment character varying,
    endofyear_review character varying,
    appraisal_form_id integer
);


--
-- Name: table1; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.table1 (
    id integer NOT NULL,
    name character varying
);


--
-- Name: table2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.table2 (
    id integer NOT NULL,
    name character varying
);


--
-- Name: training_received; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.training_received (
    institution character varying,
    date character varying,
    programme character varying,
    appraisal_form_id integer,
    submit integer
);


--
-- Name: user_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_type (
    id integer NOT NULL,
    title character varying
);


--
-- Name: user_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_type_id_seq OWNED BY public.user_type.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    staff_id integer,
    email character varying,
    password character varying,
    status boolean DEFAULT true,
    user_type_id integer,
    department_type_id integer
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: view_end; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.view_end AS
 SELECT appraisal_form.appraisal_form_id,
    staff.fname AS firstname,
    staff.sname AS lastname,
    staff.oname AS middlename,
    staff.email,
    staff.staff_id,
    staff.supervisor,
    ( SELECT (((s.fname)::text || ' '::text) || (s.oname)::text)
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_name,
    ( SELECT e.email
           FROM public.staff e
          WHERE (e.staff_id = staff.supervisor)) AS supervisor_email,
    staff.roles,
    ( SELECT roles.role_description
           FROM public.roles
          WHERE (staff.roles = roles.role_id)) AS role_description,
    performance_details.id,
    performance_details.comments,
    performance_details.status,
    performance_details.approved_date,
    performance_details.submit,
    performance_details.weight,
    performance_details.final_score,
    performance_details.performance_details_id,
    performance_details.p_a AS performance_assessments
   FROM ((public.staff
     LEFT JOIN public.appraisal_form ON ((appraisal_form.staff_id = staff.staff_id)))
     LEFT JOIN public.performance_details ON ((performance_details.appraisal_form_id = appraisal_form.appraisal_form_id)));


--
-- Name: view_mid; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.view_mid AS
 SELECT appraisal_form.appraisal_form_id,
    staff.fname AS firstname,
    staff.sname AS lastname,
    staff.oname AS middlename,
    staff.email,
    staff.staff_id,
    staff.supervisor,
    ( SELECT (((s.fname)::text || ' '::text) || (s.oname)::text)
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_name,
    ( SELECT e.email
           FROM public.staff e
          WHERE (e.staff_id = staff.supervisor)) AS supervisor_email,
    staff.roles,
    ( SELECT roles.role_description
           FROM public.roles
          WHERE (staff.roles = roles.role_id)) AS role_description,
    midyear_review.midyear_review_id,
    midyear_review.progress_review,
    midyear_review.remarks,
    midyear_review.mid_status,
    midyear_review.competency,
    midyear_review.submit,
    midyear_review.midyear_review_status
   FROM ((public.staff
     LEFT JOIN public.appraisal_form ON ((appraisal_form.staff_id = staff.staff_id)))
     LEFT JOIN public.midyear_review ON ((midyear_review.appraisal_form_id = appraisal_form.appraisal_form_id)));


--
-- Name: view_start; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.view_start AS
 SELECT appraisal_form.appraisal_form_id,
    staff.fname AS firstname,
    staff.sname AS lastname,
    staff.oname AS middlename,
    staff.email,
    staff.staff_id,
    staff.supervisor,
    ( SELECT (((s.fname)::text || ' '::text) || (s.oname)::text)
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_name,
    ( SELECT e.email
           FROM public.staff e
          WHERE (e.staff_id = staff.supervisor)) AS supervisor_email,
    staff.roles,
    ( SELECT roles.role_description
           FROM public.roles
          WHERE (staff.roles = roles.role_id)) AS role_description,
    annual_plan.annual_plan_id,
    annual_plan.result_areas,
    annual_plan.target,
    annual_plan.resources,
    annual_plan.start_status,
    annual_plan.submit,
    annual_plan.annual_plan_status
   FROM ((public.staff
     LEFT JOIN public.appraisal_form ON ((appraisal_form.staff_id = staff.staff_id)))
     LEFT JOIN public.annual_plan ON ((annual_plan.appraisal_form_id = appraisal_form.appraisal_form_id)));


--
-- Name: yearly_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yearly_details (
    department character varying NOT NULL,
    grade integer NOT NULL,
    "position" character varying NOT NULL,
    year date DEFAULT now() NOT NULL,
    staff_id integer NOT NULL,
    yearly_details_id bigint NOT NULL
);


--
-- Name: view_users_form_details; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.view_users_form_details AS
 SELECT appraisal_form.appraisal_form_id,
    staff.fname AS firstname,
    staff.sname AS lastname,
    staff.oname AS middlename,
    staff.email,
    staff.gender,
    staff.staff_id,
    staff.supervisor,
    ( SELECT (s.fname)::text AS fname
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_fname,
    ( SELECT (s.oname)::text AS oname
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_oname,
    ( SELECT (s.sname)::text AS sname
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_sname,
    ( SELECT e.email
           FROM public.staff e
          WHERE (e.staff_id = staff.supervisor)) AS supervisor_email,
    staff.roles,
    ( SELECT roles.role_description
           FROM public.roles
          WHERE (staff.roles = roles.role_id)) AS role_description,
    yearly_details.department,
    yearly_details."position" AS positions,
    yearly_details.grade,
    annual_plan.result_areas,
    annual_plan.target,
    annual_plan.resources,
    annual_plan.start_status,
    annual_plan.submit,
    annual_plan.annual_plan_status,
    supervisor_comment.annual_plan_comment,
    midyear_review.progress_review,
    midyear_review.remarks,
    midyear_review.midyear_review_status,
    midyear_review.competency,
    midyear_review.mid_status,
    supervisor_comment.midyear_review_comment,
    endofyear_review.end_status,
    endofyear_review.average_per_rating,
    endofyear_review.average_total,
    endofyear_review.average_per_rating_id,
    endofyear_review.appraisers_comment_on_workplan AS appraisal_comment_on_workplan,
    endofyear_review.training_development_comments,
    ( SELECT public.assessments(endofyear_review.appraisal_form_id, 1) AS core_assessments) AS core_assessments,
    ( SELECT public.assessments(endofyear_review.appraisal_form_id, 2) AS assessments) AS non_core_assessments,
    endofyear_review.appraisees_comments_and_plan,
    endofyear_review.head_of_divisions_comments,
    supervisor_comment.endofyear_review,
    ( SELECT public.performance_assessment(endofyear_review.appraisal_form_id) AS performance_assessment) AS performance_assessment,
    ( SELECT public.overall_total(endofyear_review.appraisal_form_id) AS overall_total) AS overall_total,
    ( SELECT public.overall_performance_rating(endofyear_review.appraisal_form_id) AS overall_performance_rating) AS overall_performance_rating,
    staff.appointment,
    ( SELECT p.positions
           FROM public.staff p
          WHERE (p.staff_id = staff.supervisor)) AS supervisor_position,
    ( SELECT r.roles
           FROM public.staff r
          WHERE (r.staff_id = staff.supervisor)) AS supervisor_role,
    ( SELECT a.appointment
           FROM public.staff a
          WHERE (a.staff_id = staff.supervisor)) AS supervisor_appointment,
    performance_details.p_a AS performance_assessments,
    training_received.programme AS training_received_programme,
    training_received.institution AS training_received_institution,
    training_received.date AS training_received_date
   FROM ((((((((public.staff
     JOIN public.appraisal_form ON ((appraisal_form.staff_id = staff.staff_id)))
     LEFT JOIN public.yearly_details ON ((yearly_details.staff_id = staff.staff_id)))
     LEFT JOIN public.annual_plan ON ((annual_plan.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.midyear_review ON ((midyear_review.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.supervisor_comment ON ((supervisor_comment.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.endofyear_review ON ((endofyear_review.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.performance_details ON ((performance_details.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.training_received ON ((training_received.appraisal_form_id = appraisal_form.appraisal_form_id)));


--
-- Name: vw_annual_plan; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_annual_plan AS
 SELECT annual_plan.result_areas,
    annual_plan.target,
    annual_plan.resources,
    annual_plan.appraisal_form_id,
    annual_plan.annual_plan_id,
    annual_plan.start_status,
    annual_plan.submit,
    annual_plan.annual_plan_status
   FROM public.annual_plan;


--
-- Name: vw_competency; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_competency AS
 SELECT competency.category,
    competency.weight,
    competency.sub,
    competency.main,
    competency.competency_id,
    competency_details.appraisal_form_id,
    competency_details.grade,
    competency_details.status,
    competency_details.submit,
    (competency.weight * (competency_details.grade)::double precision) AS score,
    competency_details.disapprove_status
   FROM (public.competency
     JOIN public.competency_details ON ((competency.competency_id = competency_details.competency_id)));


--
-- Name: vw_end; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_end AS
 SELECT competency_details.id,
    competency_details.competency_id,
    competency_details.appraisal_form_id,
    competency_details.status,
    competency_details.grade,
    competency_details.submit,
    competency_details.disapprove_status,
    performance_details.comments,
    performance_details.weight,
    performance_details.final_score,
    performance_details.performance_details_id
   FROM (public.competency_details
     LEFT JOIN public.performance_details ON ((performance_details.appraisal_form_id = competency_details.appraisal_form_id)));


--
-- Name: vw_endofyear_review; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_endofyear_review AS
 SELECT ( SELECT public.assessments(endofyear_review.appraisal_form_id, 1) AS core_assessments) AS core_assessments,
    ( SELECT public.assessments(endofyear_review.appraisal_form_id, 2) AS assessments) AS non_core_assessments,
    ( SELECT public.performance_assessment(endofyear_review.appraisal_form_id) AS performance_assessment) AS performance_assessment,
    endofyear_review.appraisal_form_id,
    endofyear_review.endofyear_review_id,
    endofyear_review.performance_details_id,
    endofyear_review.end_status,
    endofyear_review.average_per_rating,
    endofyear_review.average_total,
    endofyear_review.average_per_rating_id,
    endofyear_review.appraisers_comment_on_workplan AS appraisal_comment_on_workplan,
    endofyear_review.training_development_comments,
    endofyear_review.submit,
    performance_details.p_a AS performance_assessments
   FROM (public.endofyear_review
     LEFT JOIN public.performance_details ON ((performance_details.appraisal_form_id = endofyear_review.appraisal_form_id)));


--
-- Name: vw_midyear_review; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_midyear_review AS
 SELECT midyear_review.progress_review,
    midyear_review.remarks,
    midyear_review.mid_status,
    midyear_review.appraisal_form_id,
    midyear_review.midyear_review_id,
    midyear_review.competency,
    midyear_review.submit,
    midyear_review.midyear_review_status
   FROM public.midyear_review;


--
-- Name: vw_roles; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_roles AS
 SELECT s.roles AS role_id,
    r.role_description
   FROM (public.staff s
     LEFT JOIN public.roles r ON ((s.roles = r.role_id)));


--
-- Name: vw_users_current_form_details; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_users_current_form_details AS
 SELECT appraisal_form.appraisal_form_id,
    date_part('year'::text, appraisal_form.date) AS appraisal_year,
    staff.fname AS firstname,
    staff.sname AS lastname,
    staff.oname AS middlename,
    staff.email,
    staff.gender,
    staff.staff_id,
    staff.supervisor,
    ( SELECT (((s.fname)::text || ' '::text) || (s.oname)::text)
           FROM public.staff s
          WHERE (s.staff_id = staff.supervisor)) AS supervisor_name,
    ( SELECT e.email
           FROM public.staff e
          WHERE (e.staff_id = staff.supervisor)) AS supervisor_email,
    staff.roles,
    ( SELECT roles.role_description
           FROM public.roles
          WHERE (staff.roles = roles.role_id)) AS role_description,
    yearly_details.department,
    yearly_details."position" AS positions,
    yearly_details.grade,
    annual_plan.result_areas,
    annual_plan.target,
    annual_plan.resources,
    annual_plan.start_status,
    midyear_review.progress_review,
    midyear_review.remarks,
    midyear_review.mid_status,
    endofyear_review.end_status
   FROM (((((public.staff
     JOIN public.appraisal_form ON ((appraisal_form.staff_id = staff.staff_id)))
     JOIN public.yearly_details ON ((yearly_details.staff_id = staff.staff_id)))
     LEFT JOIN public.annual_plan ON ((annual_plan.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.midyear_review ON ((midyear_review.appraisal_form_id = appraisal_form.appraisal_form_id)))
     LEFT JOIN public.endofyear_review ON ((endofyear_review.appraisal_form_id = appraisal_form.appraisal_form_id)))
  WHERE (((appraisal_form.date IS NULL) OR (date_part('year'::text, appraisal_form.date) = date_part('year'::text, now()))) AND (date_part('year'::text, yearly_details.year) = date_part('year'::text, now())));


--
-- Name: yearly_details_yearly_details_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yearly_details_yearly_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yearly_details_yearly_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yearly_details_yearly_details_id_seq OWNED BY public.yearly_details.yearly_details_id;


--
-- Name: appraisal_form appraisal_form_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form ALTER COLUMN appraisal_form_id SET DEFAULT nextval('public.appraisal_form_appraisal_form_id_seq'::regclass);


--
-- Name: competency_details id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency_details ALTER COLUMN id SET DEFAULT nextval('public.competency_details_id_seq'::regclass);


--
-- Name: deadline deadline_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline ALTER COLUMN deadline_id SET DEFAULT nextval('public.deadline_deadline_id_seq'::regclass);


--
-- Name: department_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.department_type ALTER COLUMN id SET DEFAULT nextval('public.department_type_id_seq'::regclass);


--
-- Name: endofyear_review endofyear_review_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review ALTER COLUMN endofyear_review_id SET DEFAULT nextval('public.endofyear_review_endofyear_review_id_seq'::regclass);


--
-- Name: form_completion form_completion_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion ALTER COLUMN form_completion_id SET DEFAULT nextval('public.form_completion_form_completion_id_seq'::regclass);


--
-- Name: hash_table hash_table_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table ALTER COLUMN hash_table_id SET DEFAULT nextval('public.hash_table_hash_table_id_seq'::regclass);


--
-- Name: overall_performance id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.overall_performance ALTER COLUMN id SET DEFAULT nextval('public."overall performance_id_seq"'::regclass);


--
-- Name: performance_details id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performance_details ALTER COLUMN id SET DEFAULT nextval('public.performance_details_id_seq'::regclass);


--
-- Name: reset_password_codes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_codes ALTER COLUMN id SET DEFAULT nextval('public.reset_password_codes_id_seq'::regclass);


--
-- Name: reset_password_token id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_token ALTER COLUMN id SET DEFAULT nextval('public.reset_password_token_id_seq'::regclass);


--
-- Name: revoked_tokens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.revoked_tokens ALTER COLUMN id SET DEFAULT nextval('public.revoked_tokens_id_seq'::regclass);


--
-- Name: staff staff_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff ALTER COLUMN staff_id SET DEFAULT nextval('public.staff_staff_id_seq'::regclass);


--
-- Name: user_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_type ALTER COLUMN id SET DEFAULT nextval('public.user_type_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: yearly_details yearly_details_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yearly_details ALTER COLUMN yearly_details_id SET DEFAULT nextval('public.yearly_details_yearly_details_id_seq'::regclass);


--
-- Data for Name: annual_appraisal; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 198, 0, 88);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 1, 0, 86);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 199, 0, 89);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 200, 0, 90);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 201, 0, 91);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 202, 0, 92);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 203, 0, 93);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 204, 0, 94);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 205, 0, 95);
INSERT INTO public.annual_appraisal (comment, field, appraisal_form_id, status, annual_appraisal_id) VALUES (NULL, NULL, 206, 0, 96);


--
-- Data for Name: annual_plan; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES (NULL, NULL, NULL, 198, 435, 0, NULL, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES (NULL, NULL, NULL, 1, 433, 0, NULL, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES (NULL, NULL, NULL, 200, 437, 0, NULL, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES (NULL, NULL, NULL, 201, 438, 0, NULL, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES ('development|Training ', 'build 2 applications|Train people in Fast API', 'good internet connection|laptop', 203, 440, 1, 1, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES ('Release EduNOSS 2.0 & NOSS Destop 2.0', '	Complete piloting of NOSS and EduNOSS by July 2021 ', 'laptop', 206, 458, 1, 1, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES ('Innovation', 'Build an appraisal system to help assess staffs', 'laptop', 199, 436, 1, 1, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES ('Release EduNOSS 2.0 & NOSS Destop 2.0|Contribute to develop two client solutions|CSD Training', 'Complete piloting of NOSS and EduNOSS by July 2021 |Work with consultancy department to develop and deploy two client solutions by the end of 2021|Train at least 100 people in CSD class', 'Laptop|Laptop and internet access|', 204, 450, 1, 1, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES ('Innovation|Research', 'Build an appraisal system to help assess staffs|Research into how recommendation system works in AI ', 'laptop, internet access|laptop, internet access', 202, 439, 1, 1, 0);
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, start_status, submit, annual_plan_status) VALUES ('Release EduNOSS 2.0 & NOSS Destop 2.0|Contribute to develop two client solutions|CSD Training', 'Complete piloting of NOSS and EduNOSS by July 2021 |Work with consultancy department to develop and deploy two client solutions by the end of 2021|Train at least 100 people in CSD class', 'Laptop|Laptop and internet access|', 205, 453, 1, 1, 0);


--
-- Data for Name: appraisal_form; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 198, '2022-01-04', 2);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 1, '2022-01-04', 1);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 199, '2022-01-04', 3);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 200, '2022-01-04', 215);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 201, '2022-01-05', 216);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 202, '2022-01-05', 217);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 203, '2022-01-05', 218);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 204, '2022-01-05', 219);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 205, '2022-01-06', 220);
INSERT INTO public.appraisal_form (department, grade, positions, appraisal_form_id, date, staff_id) VALUES (NULL, NULL, NULL, 206, '2022-01-27', 221);


--
-- Data for Name: competency; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to accept challenge and execute them with confidence', 'Maximizing and maintaining Productivity', 0.3, 1);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to adhere to organization’s principles , ethics and values.', 'Supporting and Cooperating ', 0.3, 2);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to communicate decisions clearly and fluently', 'Communication (oral, written & electronic)', 0.3, 3);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to exercise good judgment', 'Leadership and Decision Making', 0.3, 4);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to initiate actions and provide direction to others', 'Leadership and Decision Making', 0.3, 5);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to manage others to achieve shared goals', 'Organization and Management:', 0.3, 6);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to mange pressure and setbacks effectively.', 'Maximizing and maintaining Productivity', 0.3, 7);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to motivate and instigate others.', 'Maximizing and maintaining Productivity', 0.3, 8);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to negotiate and mange conflict effectively ', 'Communication (oral, written & electronic)', 0.3, 9);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to plan,organize and mange work load.', 'Organization and Management:', 0.3, 10);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to relate and network cross different levels and department', 'Communication (oral, written & electronic)', 0.3, 11);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to show support to others.', 'Supporting and Cooperating ', 0.3, 12);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to think broadly and demonstrate creativity.', 'Innovation and Strategic Thinking', 0.3, 13);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to work effectively with teams, clients and staff.', 'Supporting and Cooperating ', 0.3, 14);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Ability to work systematically and maintain quality', 'Organization and Management:', 0.3, 15);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Able to develop others (subordinates)', 'Ability to Develop Staff', 0.1, 16);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Able to provide guidance and support to staff for their development.', 'Ability to Develop Staff', 0.1, 17);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Acceptance of responsibility and decision making ', 'Leadership and Decision Making', 0.3, 18);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Building, applying and sharing of necessary expertise and technology', 'Job Knowledge and Technical Skills ', 0.3, 19);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Commitment to customer satisfaction', 'Developing and improving', 0.3, 20);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Commitment to organization development', 'Developing and improving', 0.3, 21);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Demonstration of correct mental, physical and manual skills', 'Job Knowledge and Technical Skills ', 0.3, 22);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Demonstration of cross-functional awareness', 'Job Knowledge and Technical Skills ', 0.3, 23);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Eagerness to self-development. ', 'Commitment to Own Personal Development and Training', 0.1, 24);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Ensuring customer satisfaction', 'Delivering Results and Ensuring Customer Satisfaction', 0.1, 25);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Ensuring the delivery of quality service and products', 'Delivering Results and Ensuring Customer Satisfaction', 0.1, 26);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Executing result-based actions', 'Developing / Managing budgets and saving cost', 0.3, 27);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Firm awareness of financial issues and accountability.', 'Developing / Managing budgets and saving cost', 0.3, 28);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Inner drive to supplement training organization', 'Commitment to Own Personal Development and Training', 0.1, 29);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Keeping to laid down regulations and procedures', 'Following Instructions and Working Towards Organizational Goals', 0.1, 30);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Originality in thinking', 'Innovation and Strategic Thinking', 0.3, 31);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Support for organizational change', 'Innovation and Strategic Thinking', 0.3, 32);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('Core', 'Understanding of business processes and customer priorities', 'Developing / Managing budgets and saving cost', 0.3, 33);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Willingness to act on customer feedback for customer satisfaction', 'Following Instructions and Working Towards Organizational Goals', 0.1, 34);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Ability to work effectively in a team', 'Ability to work effectively in a team', 0.1, 36);
INSERT INTO public.competency (category, sub, main, weight, competency_id) VALUES ('None Core', 'Respect and commitment', 'Respect and commitment', 0.1, 35);


--
-- Data for Name: competency_details; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (65, 3, 204, 1, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2369, 3, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1185, 2, 205, 0, 4, 1, 1, '5 is to much');
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2305, 1, 202, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3521, 3, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2337, 2, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3777, 11, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5825, 3, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3457, 1, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3649, 7, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5761, 1, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3489, 2, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5793, 2, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1, 1, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1153, 1, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (33, 2, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1217, 3, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (97, 4, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1249, 4, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1313, 6, 205, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2401, 4, 202, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2433, 5, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3553, 4, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2497, 7, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5857, 4, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2465, 6, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3585, 5, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3617, 6, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5889, 5, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5953, 7, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5921, 6, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (129, 5, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1281, 5, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (161, 6, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (193, 7, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1345, 7, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (225, 8, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1377, 8, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1409, 9, 205, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2561, 9, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1473, 11, 205, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1441, 10, 205, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2625, 11, 202, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1505, 12, 205, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3713, 9, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6017, 9, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2529, 8, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (257, 9, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3681, 8, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2593, 10, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3745, 10, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6081, 11, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (5985, 8, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6049, 10, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (289, 10, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (321, 11, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (353, 12, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1569, 14, 205, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2689, 13, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (385, 13, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3841, 13, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2753, 15, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6145, 13, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2657, 12, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3809, 12, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2721, 14, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3873, 14, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6113, 12, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6177, 14, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1537, 13, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (417, 14, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (449, 15, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1601, 15, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (481, 18, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1633, 18, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (513, 19, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2849, 20, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2881, 21, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4001, 20, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2817, 19, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6305, 20, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2785, 18, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3969, 19, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3937, 18, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6273, 19, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3905, 15, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1665, 19, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6241, 18, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6209, 15, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (545, 20, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1697, 20, 205, 0, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (577, 21, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1729, 21, 205, 0, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (609, 22, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1761, 22, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (641, 23, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1825, 27, 205, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2977, 27, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3009, 28, 202, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4129, 27, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2913, 22, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6433, 27, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2945, 23, 202, 1, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4033, 21, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4065, 22, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6337, 21, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1793, 23, 205, 0, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4097, 23, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (673, 27, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6369, 22, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6401, 23, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (705, 28, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1857, 28, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (737, 31, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (769, 32, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1889, 31, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3105, 33, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3041, 31, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4161, 28, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3073, 32, 202, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6465, 28, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3137, 16, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4257, 33, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (801, 33, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1921, 32, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4193, 31, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6561, 33, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4225, 32, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6497, 31, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6529, 32, 199, 1, 1, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (833, 16, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1953, 33, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (865, 17, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1985, 16, 205, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (897, 24, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2017, 17, 205, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3169, 17, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3201, 24, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (929, 25, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4289, 16, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3233, 25, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6593, 16, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2049, 24, 205, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3265, 26, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4321, 17, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4353, 24, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6625, 17, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6657, 24, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (961, 26, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2081, 25, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (993, 29, 204, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2113, 26, 205, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1025, 30, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2145, 29, 205, 0, 2, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1057, 34, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3297, 29, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3329, 30, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3361, 34, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4449, 29, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2177, 30, 205, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3393, 35, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6753, 29, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4385, 25, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4417, 26, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6689, 25, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4481, 30, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6785, 30, 199, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1089, 35, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2209, 34, 205, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (1121, 36, 204, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6721, 26, 199, 0, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2241, 35, 205, 0, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (2273, 36, 205, 0, 3, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (3425, 36, 202, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4577, 36, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6881, 36, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4513, 34, 206, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (4545, 35, 206, 1, 4, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6817, 34, 199, 1, 5, 1, 0, NULL);
INSERT INTO public.competency_details (id, competency_id, appraisal_form_id, status, grade, submit, disapprove_status, disapprove_comments) VALUES (6849, 35, 199, 1, 4, 1, 0, NULL);


--
-- Data for Name: deadline; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.deadline (deadline_type, start_date, ending, deadline_id) VALUES ('End', '2022-01-05', '2022-06-30', 51);
INSERT INTO public.deadline (deadline_type, start_date, ending, deadline_id) VALUES ('Mid', '2022-01-06', '2022-01-31', 50);
INSERT INTO public.deadline (deadline_type, start_date, ending, deadline_id) VALUES ('Start', '2022-01-27', '2022-02-28', 49);


--
-- Data for Name: department_type; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: disapprove_competency_comment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.disapprove_competency_comment (appraisal_form_id, competency_id, comments) VALUES (205, 2, '5 is to much');


--
-- Data for Name: endofyear_review; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.endofyear_review (appraisal_form_id, endofyear_review_id, performance_details_id, end_status, average_per_rating, average_total, average_per_rating_id, appraisers_comment_on_workplan, training_development_comments, submit, endyear_review_status, appraisees_comments_and_plan, head_of_divisions_comments) VALUES (206, 19, NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 0, NULL, NULL);
INSERT INTO public.endofyear_review (appraisal_form_id, endofyear_review_id, performance_details_id, end_status, average_per_rating, average_total, average_per_rating_id, appraisers_comment_on_workplan, training_development_comments, submit, endyear_review_status, appraisees_comments_and_plan, head_of_divisions_comments) VALUES (204, 1, NULL, 1, NULL, NULL, NULL, 'I notice him making progress each year.', 'I want to further my education in software Development.', 1, 0, 'I was able to meet my deadlines and also work in a team to develop client solutions.', 'More room for improvement.');
INSERT INTO public.endofyear_review (appraisal_form_id, endofyear_review_id, performance_details_id, end_status, average_per_rating, average_total, average_per_rating_id, appraisers_comment_on_workplan, training_development_comments, submit, endyear_review_status, appraisees_comments_and_plan, head_of_divisions_comments) VALUES (199, 20, NULL, 1, NULL, NULL, NULL, 'you can do better ', 'would be taking courses to improve my skills', 1, 0, 'would work harder', 'more room for improvement');
INSERT INTO public.endofyear_review (appraisal_form_id, endofyear_review_id, performance_details_id, end_status, average_per_rating, average_total, average_per_rating_id, appraisers_comment_on_workplan, training_development_comments, submit, endyear_review_status, appraisees_comments_and_plan, head_of_divisions_comments) VALUES (205, 8, NULL, 1, NULL, NULL, NULL, 'More room for improvement. ', 'I want to further my education in Artificial Intelligence ', 1, 0, 'I was able to meet my deadlines and also work in a team to develop client solutions. ', 'can do better');
INSERT INTO public.endofyear_review (appraisal_form_id, endofyear_review_id, performance_details_id, end_status, average_per_rating, average_total, average_per_rating_id, appraisers_comment_on_workplan, training_development_comments, submit, endyear_review_status, appraisees_comments_and_plan, head_of_divisions_comments) VALUES (202, 12, NULL, 1, NULL, NULL, NULL, 'can do better than this', 'would be taking online courses to help improve my skills', 1, 0, 'Was almost able to complete all targets for the year', 'more room for improvement ');


--
-- Data for Name: form_completion; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: hash_table; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('15181a29f2676b97fd5de0bace1d2c11', 'admin@aiti.com', 1);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('8207f6cc70360d4a40a180c751b2d224', 'dg@aiti.com', 3);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('0d2f81fd1a41b8395cdf22dac844eee9', 'kingsley@aiti.com', 5);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('976b47e453e81a07afc5ceb4cb020c26', 'rebecca@aiti.com', 6);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('6f5529737f47b056564d00a04219003b', 'belinda@test.com', 9);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('9ecf580f7d990b1287f5eadf1e6d8675', 'bismark@test.com', 10);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('d7bad68b99f0e51adee6b467c3137566', 'franklin@test.com', 7);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('555c34e0a1f172b15146281676ac7cce', 'janet@aiti.com', 4);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('d336dcc4c4aa913d0cba98816ba244f3', 'nathan@test.com', 8);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('86cc290b0dd74e019b31f9448e0fc397', 'fel@test.com', 11);


--
-- Data for Name: midyear_review; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.midyear_review (midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency, submit, midyear_review_status) VALUES (47, '80% completed|COTVET Document System - 100% completed
Eye Clinic - 70% completed|80% completed', 'progress is good|progress is good| progress is good', 1, 204, 'Linux|Django|HTML/CSS', 1, 0);
INSERT INTO public.midyear_review (midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency, submit, midyear_review_status) VALUES (48, 'start year and mid year form are completed|In progress', 'undefined', 1, 202, 'likely to complete|likely to finish', 1, 0);
INSERT INTO public.midyear_review (midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency, submit, midyear_review_status) VALUES (49, 'Complete piloting of NOSS and EduNOSS by July 2021 |Work with consultancy department to develop and deploy two client solutions by the end of 2021|Train at least 100 people in CSD class', 'undefined', 1, 205, '80% completed|COTVET Document System - 100% completed Eye Clinic - 70% completed|80% completed', 1, 0);
INSERT INTO public.midyear_review (midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency, submit, midyear_review_status) VALUES (55, '	start year and mid year form are completed', 'undefined', 1, 199, 'likely to complete', 1, 0);
INSERT INTO public.midyear_review (midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency, submit, midyear_review_status) VALUES (51, 'Deployed 1 already|Trained 30 people already', 'undefined', 1, 203, 'likely to finish|Good', 1, 0);
INSERT INTO public.midyear_review (midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency, submit, midyear_review_status) VALUES (53, 'Complete piloting of NOSS and EduNOSS by July 2021 ', 'undefined', 1, 206, '	Complete piloting of NOSS and EduNOSS by July 2021 ', 1, 0);


--
-- Data for Name: overall_assessment; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: overall_performance; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.overall_performance (id, description, performance) VALUES (1, 'Outstanding  Performance', 'Employee has in all areas exceeded agreed expectations in achieving targets.');
INSERT INTO public.overall_performance (id, description, performance) VALUES (2, ' Very Good Performance', 'Employee has met all expectations in achieving set targets.');
INSERT INTO public.overall_performance (id, description, performance) VALUES (3, 'Satisfactory / Acceptable Performance', 'Employee has met most agreed expectations in achieving set targets.');
INSERT INTO public.overall_performance (id, description, performance) VALUES (4, 'Needs Improvement', 'Employee has not met most agreed expectations in achieving set targets.');
INSERT INTO public.overall_performance (id, description, performance) VALUES (5, 'Unacceptable Performance', 'Employee has failed to meet agreed expectations in achieving set targets');


--
-- Data for Name: performance_details; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (49, 152, 'Good|Good', 0, '2021-11-04', 1, '5|5', '4|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (50, 153, 'Good|Good', 1, '2021-11-04', 1, '5|5', '3|4', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (51, 157, 'Good|Good', 1, '2021-11-15', 1, '5|5', '5|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (81, 172, 'Good|Good', 1, '2021-12-23', 1, '5|5', '5|4', NULL, 'Improving|Improving');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (76, 179, 'Good|', 1, '2021-12-23', 1, '5|5', '5|5', NULL, 'Improving|Improving');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (52, 158, 'Good|Good', 1, '2021-11-20', 1, '5|5', '5|4', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (53, 162, 'Good|Good', 1, '2021-11-24', 1, '5|5', '5|4', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (54, 167, 'test', 0, '2021-11-29', 0, '5', '3', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (59, 175, 'string', 1, '2021-12-22', 1, 'string', 'string', NULL, 'string');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (87, 206, 'had challenges with the resources ', 1, '2022-01-27', 1, '5', '5', NULL, 'was able to complete targets');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (82, 184, 'Could have done better|Good', 1, '2021-12-26', 1, '5|5', '3|5', NULL, 'Had a problem with my laptop which affected productivity |I was able to complete it');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (65, 178, 'Good|
Good', 1, '2021-12-06', 1, '5|5', '4|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (83, 204, '||', 1, '2022-01-05', 1, '5|5|5', '5|5|5', NULL, 'Was able to meet deadline|Was able to meet deadline|Was able to meet deadline');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (89, 199, 'had challenges with the resources', 1, '2022-01-31', 1, '5', '5', NULL, 'was able to complete the target ');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (57, 176, 'The interns were well trained to work effectively|All 3 corporate seminars were successfully organized|Received enough feedback from questionnaires to improve sector|Not successful after losing out on scholarship opportunities|Successfully completed', 1, '2021-11-29', 1, '5|5|5|5|5', '5|5|5|2|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (66, 181, '5|5|5|5|5', 1, '2021-12-08', 1, '5|5|5|5|5', '5|5|5|5|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (60, 177, '50 people were successfully trained|completed|completed|completed|completed', 1, '2021-12-10', 1, '5|5|5|5|5', '5|5|5|5|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (70, 182, 'Good|Good|Good|Good|Good|Good|Good', 1, '2021-12-10', 1, '5|5|5|5|5|5|5', '5|5|5|5|5|5|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (84, 205, 'string', 1, '2022-01-20', 0, 'string', 'string', NULL, 'string');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (71, 183, 'Test|Test|Test|Test|Test|Test|Test', 1, '2021-12-10', 1, '5|5|5|5|5|5|5', '5|5|5|5|5|5|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (72, 171, 'Good|Good', 1, '2021-12-10', 1, '5|5', '4|5', NULL, NULL);
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (86, 202, 'Good|lack of resources to complete it', 1, '2022-01-27', 1, '5|5', '5|3', NULL, 'was able to complete the project|Research wasn''t been able to be completed');
INSERT INTO public.performance_details (id, appraisal_form_id, comments, status, approved_date, submit, weight, final_score, performance_details_id, p_a) VALUES (74, 180, 'Good|Good', 1, '2021-12-16', 1, '5|5', '5|4', NULL, NULL);


--
-- Data for Name: reset_password_codes; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.reset_password_codes (id, code, user_id, user_email, status, date_created, date_modified) VALUES (36, 'VLYYMOSQ6TLEQ297RJ2CHFQBW086USWY', NULL, 'managementappraiser@gmail.com', true, '2021-07-01 09:22:15.680069', '2021-07-01 09:22:15.680087');
INSERT INTO public.reset_password_codes (id, code, user_id, user_email, status, date_created, date_modified) VALUES (39, 'OYRODQ6IL3A1DLJ29D84PUVW915DS1CU', NULL, 'eawitikuffour@gmaill.com', true, '2021-07-02 13:33:45.464145', '2021-07-02 13:33:45.464156');
INSERT INTO public.reset_password_codes (id, code, user_id, user_email, status, date_created, date_modified) VALUES (42, 'Q4DGS2EOE0P5HOIHJ5ROZRPLEHB3BZRJ', NULL, 'eawitikuffour@gmail.com', true, '2021-07-02 13:59:19.749538', '2021-07-02 13:59:19.749545');
INSERT INTO public.reset_password_codes (id, code, user_id, user_email, status, date_created, date_modified) VALUES (43, 'WGPN2JLIFUK1O8SEONAF2439FUAT4PCF', NULL, 'louis@test.com', true, '2021-12-10 06:50:44.636679', '2021-12-10 06:50:44.636733');


--
-- Data for Name: reset_password_token; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: revoked_tokens; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.roles (role_id, role_description) VALUES (1, 'Admin/HR');
INSERT INTO public.roles (role_id, role_description) VALUES (2, 'Appraiser/Supervisor');
INSERT INTO public.roles (role_id, role_description) VALUES (3, 'Appraisee/Staff');


--
-- Data for Name: save_annual_plan; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (215, 'KIngsley', 'Oduro', 'Kwaku', 'kingsley@aiti.com', 1, 'Male', 'Finance', 'Director', 100, '2022-01-05', 2, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (1, 'Paul', 'Adu', 'Theophillus', 'admin@aiti.com', 1, 'Male', 'Corporate', 'HR
', 100, '2022-01-05', 1, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (2, 'Nafiu', 'Lawal', NULL, 'dg@aiti.com', 2, 'Male', 'Corporate
', 'DG', 100, '2022-01-05', 1, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (3, 'Janet
', 'Owusu', 'Ama', 'janet@aiti.com', 1, 'Male', 'Consultancy

', 'Director', 80, '2022-01-05', 2, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (216, 'Rebecca', 'Osei', '', 'rebecca@aiti.com', 2, 'Female', 'Research & Innovation', 'Director', 20, '2016-01-01', 2, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (217, 'Franklin', 'Appiah', '', 'franklin@test.com', 3, 'Male', 'Research & Innovation', 'Associate Programmer', 18, '2022-01-05', 3, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (218, 'Nathan', 'Asiedu', 'Quansah', 'nathan@test.com', 2, 'Male', 'Research & Innovation', 'Researcher', 10, '2022-01-05', 3, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (219, 'Belinda', 'Tetteh', '', 'belinda@test.com', 3, 'Female', 'Academics', 'Researcch Assistant', 18, '2022-01-05', 3, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (220, 'Bismark', 'Otu', '', 'bismark@test.com', 1, 'Male', 'Research & Innovation', 'Associate Programmer', 18, '2022-01-06', 3, 1);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status) VALUES (221, 'Felicity', 'Campbell', '', 'fel@test.com', 3, 'Female', 'Research & Innovation', 'Researcher', 18, '2022-01-27', 2, 1);


--
-- Data for Name: supervisor_comment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.supervisor_comment (annual_plan_comment, midyear_review_comment, endofyear_review, appraisal_form_id) VALUES ('Still not enough', NULL, NULL, 203);


--
-- Data for Name: table1; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.table1 (id, name) VALUES (1, 'prince');
INSERT INTO public.table1 (id, name) VALUES (2, 'addo');
INSERT INTO public.table1 (id, name) VALUES (3, 'samuel');
INSERT INTO public.table1 (id, name) VALUES (4, 'dead');


--
-- Data for Name: table2; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.table2 (id, name) VALUES (1, 'prince');
INSERT INTO public.table2 (id, name) VALUES (2, 'addo');
INSERT INTO public.table2 (id, name) VALUES (3, 'samuel');
INSERT INTO public.table2 (id, name) VALUES (4, 'dead');


--
-- Data for Name: training_received; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.training_received (institution, date, programme, appraisal_form_id, submit) VALUES ('AITI-KACE|AITI-KACE', '2021-12-09|2021-11-11', 'Software Testing |Penetration testing', 205, 1);
INSERT INTO public.training_received (institution, date, programme, appraisal_form_id, submit) VALUES ('AITI-KACE|NITA', '2021-12-02|2021-11-04', 'Software Development Testing |Awareness of Data Privacy', 202, 1);
INSERT INTO public.training_received (institution, date, programme, appraisal_form_id, submit) VALUES ('AITI-KACE', '2021-12-16', 'training in Oracle Database', 199, 1);


--
-- Data for Name: user_type; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (1, 1, 'admin@aiti.com', '$pbkdf2-sha256$29000$613rnXMuxdi711qrNUaoFQ$KVf5eGfhccuPSFcMT5gm3F.uXyoOW8IqHqCe8GGfbbs', true, 1, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (3, 2, 'dg@aiti.com', '$pbkdf2-sha256$29000$kPL.v3cuxVirde4dQ2hNCQ$wXf6UIqHteOC3puntzPhjsswFlNwNm3RMLV1fB5a6uo', true, 1, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (4, 3, 'janet@aiti.com', '$pbkdf2-sha256$29000$au09p5QyRijlHOPcGyMkxA$T9uXZ3Rfqzhw4YaVO/iyD79soQjYfu7ohk07F9ND03M', true, 2, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (5, 215, 'kingsley@aiti.com', '$pbkdf2-sha256$29000$COE8J.TcG0MIwZgTYiwlZA$5EuTBupDzdX08cn05tzdOZicOQQHJ8eih63Us7ootQw', true, 2, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (6, 216, 'rebecca@aiti.com', NULL, true, 2, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (7, 217, 'franklin@test.com', NULL, true, 3, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (8, 218, 'nathan@test.com', NULL, true, 3, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (9, 219, 'belinda@test.com', NULL, true, 3, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (10, 220, 'bismark@test.com', NULL, true, 3, NULL);
INSERT INTO public.users (id, staff_id, email, password, status, user_type_id, department_type_id) VALUES (11, 221, 'fel@test.com', NULL, true, 2, NULL);


--
-- Data for Name: yearly_details; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Corporate', 100, 'HR
', '2022-01-04', 1, 1);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Corporate
', 100, 'DG', '2022-01-04', 2, 3);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Consultancy

', 80, 'Director', '2022-01-04', 3, 4);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Finance', 100, 'Director', '2022-01-04', 215, 5);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Research & Innovation', 20, 'Director', '2022-01-05', 216, 6);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Research & Innovation', 18, 'Associate Programmer', '2022-01-05', 217, 7);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Research & Innovation', 18, 'Researcher', '2022-01-05', 218, 8);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Academics', 18, 'Researcch Assistant', '2022-01-05', 219, 9);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Research & Innovation', 18, 'Associate Programmer', '2022-01-06', 220, 10);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Research & Innovation', 18, 'Researcher', '2022-01-27', 221, 11);


--
-- Name: annual_appraisal_annual_appraisal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.annual_appraisal_annual_appraisal_id_seq', 96, true);


--
-- Name: annual_plan_annual_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.annual_plan_annual_plan_id_seq', 462, true);


--
-- Name: appraisal_form_appraisal_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.appraisal_form_appraisal_form_id_seq', 206, true);


--
-- Name: competency_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.competency_details_id_seq', 6912, true);


--
-- Name: deadline_deadline_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.deadline_deadline_id_seq', 66, true);


--
-- Name: department_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.department_type_id_seq', 6, true);


--
-- Name: endofyear_review_endofyear_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.endofyear_review_endofyear_review_id_seq', 23, true);


--
-- Name: form_completion_form_completion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.form_completion_form_completion_id_seq', 1, false);


--
-- Name: hash_table_hash_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hash_table_hash_table_id_seq', 11, true);


--
-- Name: midyear_review_midyear_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.midyear_review_midyear_review_id_seq', 55, true);


--
-- Name: overall performance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."overall performance_id_seq"', 1, false);


--
-- Name: performance_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.performance_details_id_seq', 89, true);


--
-- Name: reset_password_codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reset_password_codes_id_seq', 43, true);


--
-- Name: reset_password_token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reset_password_token_id_seq', 1, false);


--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.revoked_tokens_id_seq', 1, false);


--
-- Name: staff_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.staff_staff_id_seq', 221, true);


--
-- Name: user_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_type_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 11, true);


--
-- Name: yearly_details_yearly_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yearly_details_yearly_details_id_seq', 11, true);


--
-- Name: annual_plan ann_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT ann_id UNIQUE (annual_plan_id);


--
-- Name: annual_appraisal annual_appraisal_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT annual_appraisal_pkey PRIMARY KEY (annual_appraisal_id);


--
-- Name: annual_plan annual_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT annual_plan_pkey PRIMARY KEY (annual_plan_id);


--
-- Name: annual_appraisal app_ann; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT app_ann UNIQUE (annual_appraisal_id);


--
-- Name: appraisal_form app_form_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT app_form_uq UNIQUE (appraisal_form_id);


--
-- Name: annual_plan app_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT app_id UNIQUE (appraisal_form_id);


--
-- Name: annual_appraisal app_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT app_uq UNIQUE (appraisal_form_id);


--
-- Name: disapprove_competency_comment appf_comid_ukey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disapprove_competency_comment
    ADD CONSTRAINT appf_comid_ukey UNIQUE (appraisal_form_id, competency_id);


--
-- Name: supervisor_comment appraisail_form_id_unique_k; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supervisor_comment
    ADD CONSTRAINT appraisail_form_id_unique_k UNIQUE (appraisal_form_id);


--
-- Name: midyear_review appraisal_form_id_ukey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT appraisal_form_id_ukey UNIQUE (appraisal_form_id);


--
-- Name: appraisal_form appraisal_form_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT appraisal_form_pkey PRIMARY KEY (appraisal_form_id);


--
-- Name: endofyear_review appraisal_id_unique_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT appraisal_id_unique_key UNIQUE (appraisal_form_id);


--
-- Name: training_received appraisal_unique_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_received
    ADD CONSTRAINT appraisal_unique_key UNIQUE (appraisal_form_id);


--
-- Name: performance_details appraiser_form_id_ukey6; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performance_details
    ADD CONSTRAINT appraiser_form_id_ukey6 UNIQUE (appraisal_form_id);


--
-- Name: competency comp; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency
    ADD CONSTRAINT comp UNIQUE (competency_id);


--
-- Name: competency_details comp_ukey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency_details
    ADD CONSTRAINT comp_ukey UNIQUE (competency_id, appraisal_form_id);


--
-- Name: competency compe_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency
    ADD CONSTRAINT compe_pkey PRIMARY KEY (sub);


--
-- Name: deadline deadline_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline
    ADD CONSTRAINT deadline_pkey PRIMARY KEY (deadline_id);


--
-- Name: department_type department_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.department_type
    ADD CONSTRAINT department_type_pkey PRIMARY KEY (id);


--
-- Name: staff email_fk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT email_fk UNIQUE (email);


--
-- Name: hash_table email_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table
    ADD CONSTRAINT email_uq UNIQUE (email);


--
-- Name: endofyear_review endofyear_review_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT endofyear_review_pkey PRIMARY KEY (endofyear_review_id);


--
-- Name: form_completion form_completion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion
    ADD CONSTRAINT form_completion_pkey PRIMARY KEY (form_completion_id);


--
-- Name: hash_table hash_table_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table
    ADD CONSTRAINT hash_table_pkey PRIMARY KEY (hash_table_id);


--
-- Name: hash_table hash_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table
    ADD CONSTRAINT hash_uq UNIQUE (hash);


--
-- Name: competency_details id_pkey4; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency_details
    ADD CONSTRAINT id_pkey4 PRIMARY KEY (id);


--
-- Name: midyear_review midyear_review1_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT midyear_review1_pkey PRIMARY KEY (midyear_review_id);


--
-- Name: overall_performance overall performance_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.overall_performance
    ADD CONSTRAINT "overall performance_pkey" PRIMARY KEY (id);


--
-- Name: performance_details performance_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performance_details
    ADD CONSTRAINT performance_details_pkey PRIMARY KEY (id);


--
-- Name: reset_password_codes reset_password_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_codes
    ADD CONSTRAINT reset_password_codes_code_key UNIQUE (code);


--
-- Name: reset_password_codes reset_password_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_codes
    ADD CONSTRAINT reset_password_codes_pkey PRIMARY KEY (id);


--
-- Name: reset_password_codes reset_password_codes_user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_codes
    ADD CONSTRAINT reset_password_codes_user_email_key UNIQUE (user_email);


--
-- Name: reset_password_codes reset_password_codes_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_codes
    ADD CONSTRAINT reset_password_codes_user_id_key UNIQUE (user_id);


--
-- Name: reset_password_token reset_password_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_token
    ADD CONSTRAINT reset_password_token_pkey PRIMARY KEY (id);


--
-- Name: reset_password_token reset_password_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reset_password_token
    ADD CONSTRAINT reset_password_token_user_id_key UNIQUE (user_id);


--
-- Name: revoked_tokens revoked_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.revoked_tokens
    ADD CONSTRAINT revoked_tokens_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: appraisal_form staf_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT staf_uq UNIQUE (staff_id);


--
-- Name: staff staff_fk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_fk UNIQUE (staff_id);


--
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);


--
-- Name: table1 table1_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.table1
    ADD CONSTRAINT table1_pkey PRIMARY KEY (id);


--
-- Name: deadline type_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline
    ADD CONSTRAINT type_uq UNIQUE (deadline_type);


--
-- Name: user_type user_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_type
    ADD CONSTRAINT user_type_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: yearly_details yearly_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yearly_details
    ADD CONSTRAINT yearly_details_pkey PRIMARY KEY (yearly_details_id);


--
-- Name: ix_department_type_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_department_type_id ON public.department_type USING btree (id);


--
-- Name: ix_department_type_title; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_department_type_title ON public.department_type USING btree (title);


--
-- Name: ix_reset_password_codes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reset_password_codes_id ON public.reset_password_codes USING btree (id);


--
-- Name: ix_reset_password_token_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reset_password_token_id ON public.reset_password_token USING btree (id);


--
-- Name: ix_reset_password_token_token; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reset_password_token_token ON public.reset_password_token USING btree (token);


--
-- Name: ix_user_type_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_type_id ON public.user_type USING btree (id);


--
-- Name: ix_user_type_title; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_user_type_title ON public.user_type USING btree (title);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: appraisal_form annual_appraisal_form_id_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER annual_appraisal_form_id_insert_trigger AFTER INSERT ON public.appraisal_form FOR EACH ROW EXECUTE FUNCTION public.annual_appraisal_form_insert_trigger_fnc();


--
-- Name: competency_details appraisal_end_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER appraisal_end_insert_trigger AFTER INSERT ON public.competency_details FOR EACH ROW EXECUTE FUNCTION public.appraisal_id_end_insert_trigger_fnc();


--
-- Name: appraisal_form appraisalformid_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER appraisalformid_insert_trigger AFTER INSERT ON public.appraisal_form FOR EACH ROW EXECUTE FUNCTION public.appraisalformid_insert_trigger_fnc();


--
-- Name: staff date_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER date_insert_trigger AFTER INSERT OR UPDATE ON public.staff FOR EACH ROW EXECUTE FUNCTION public.date_trigger_fnc();

ALTER TABLE public.staff DISABLE TRIGGER date_insert_trigger;


--
-- Name: staff email_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER email_insert_trigger AFTER INSERT ON public.staff FOR EACH ROW EXECUTE FUNCTION public.email_insert_trigger_fnc();


--
-- Name: staff staff_all_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER staff_all_insert_trigger AFTER INSERT ON public.staff FOR EACH ROW EXECUTE FUNCTION public.sup_all_insert_trigger_fnc();


--
-- Name: staff staff_id_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER staff_id_insert_trigger AFTER INSERT ON public.staff FOR EACH ROW EXECUTE FUNCTION public.staff_id_trigger_fnc();


--
-- Name: table1 trig_copy; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trig_copy AFTER INSERT ON public.table1 FOR EACH ROW EXECUTE FUNCTION public.function_copy();


--
-- Name: staff yearly_details; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER yearly_details AFTER INSERT ON public.staff FOR EACH ROW EXECUTE FUNCTION public.yearly_details();


--
-- Name: annual_plan ann fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT "ann fk" FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: annual_appraisal ann_app_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT ann_app_fk FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: appraisal_form app1_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT app1_fk FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: overall_assessment app_f_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.overall_assessment
    ADD CONSTRAINT app_f_id_fkey FOREIGN KEY (aprpaisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id);


--
-- Name: disapprove_competency_comment app_fid_ff; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disapprove_competency_comment
    ADD CONSTRAINT app_fid_ff FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id);


--
-- Name: supervisor_comment app_s; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supervisor_comment
    ADD CONSTRAINT app_s FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: competency_details appraisal_form_id_fkey3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency_details
    ADD CONSTRAINT appraisal_form_id_fkey3 FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: training_received appraisal_form_id_for_key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_received
    ADD CONSTRAINT appraisal_form_id_for_key FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id);


--
-- Name: competency_details comp; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency_details
    ADD CONSTRAINT comp FOREIGN KEY (competency_id) REFERENCES public.competency(competency_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: endofyear_review endfk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT endfk FOREIGN KEY (performance_details_id) REFERENCES public.performance_details(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: hash_table hash_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table
    ADD CONSTRAINT hash_fk FOREIGN KEY (email) REFERENCES public.staff(email) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: performance_details performance_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performance_details
    ADD CONSTRAINT performance_fk FOREIGN KEY (performance_details_id) REFERENCES public.overall_performance(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: staff role_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT role_fk FOREIGN KEY (roles) REFERENCES public.roles(role_id) NOT VALID;


--
-- Name: staff sup_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT sup_fk FOREIGN KEY (supervisor) REFERENCES public.staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: users users_department_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_department_type_id_fkey FOREIGN KEY (department_type_id) REFERENCES public.department_type(id);


--
-- Name: users users_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_fkey FOREIGN KEY (email) REFERENCES public.staff(email) NOT VALID;


--
-- Name: users users_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) NOT VALID;


--
-- Name: yearly_details year_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yearly_details
    ADD CONSTRAINT year_fk FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- PostgreSQL database dump complete
--

