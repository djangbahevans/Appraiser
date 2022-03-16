from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException,jwt, sys
from fastapi import HTTPException
from ..user_router.crud import read_user_by_id
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from . import schemas


# GET STAFF DETAILS
async def read_staff(db:Session):
    res = db.execute(""" SELECT staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, staff_status
	FROM public.staff; """) # READ STAFF USING DB FUNCTION
    res = res.fetchall()
    return res

async def read_staff_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_staff(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        


# READ SUPERVISORS 
async def read_supervisors(db:Session):
    res = db.execute(""" SELECT staff_id, fname, sname, oname FROM public.staff where roles=2; """) # READ SUPERVISOR FROM TABLE
    res = res.fetchall()
    return res

async def read_supervisors_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_supervisors(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        


# READ STAFF BY NAME
async def read_staff_by_name(name:str, db:Session):
    res = db.execute(""" SELECT staff_id, fname, sname, oname FROM public.staff where fname ilike :name or sname ilike :name; """, {'name':'%'+name+'%'}) # READ STAFF FROM TABLE WHERE FULL A SINGLE LETTER IN A NAME RETURNS DATA ON ALL USERS WITH THAT LETTER IN THEIR NAME
    res = res.fetchall()
    return res

async def read_staff_by_name_auth(name:str, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_staff_by_name(name, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        


# READ STAFF ROLES
async def read_roles(db:Session):
    res = db.execute(""" SELECT role_id, role_description FROM public.roles; """) # READ ROLES FROM TABLE
    res = res.fetchall()
    return res

async def read_roles_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_roles(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})         


# GET DEADLINES
async def read_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_deadline_table(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_start_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline where deadline_type='Start'; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_start_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_start_deadline_table(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_mid_deadline_table(token:str, db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline where deadline_type='Mid'; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_mid_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_mid_deadline_table(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_end_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline where deadline_type='End'; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_end_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_end_deadline_table(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# DEACTIVATE STAFF
async def deactivate_staff(staff_id:int, db:Session):
    res = db.execute(""" SELECT public.deactivate_staff (:staff_id) """, {'staff_id': staff_id}) #CHANGE STAFF STATUS FROM 1 TO 0 USING ID
    res = res.fetchall()
    db.commit()
    return res

async def deactivate_staff_auth(staff_id:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await deactivate_staff(staff_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        


# REACTIVATE STAFF
async def reactivate_staff(staff_id:int, db:Session):
    res = db.execute(""" SELECT public.reactivate_staff (:staff_id) """, {'staff_id': staff_id}) #CHANGE STAFF STATUS FROM 1 TO 0 USING ID
    res = res.fetchall()
    db.commit()
    return res

async def reactivate_staff_auth(staff_id:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await reactivate_staff(staff_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})       


# CREATE STAFF DETAILS
async def create_staff(fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, db:Session):
    res = db.execute("""insert into public.staff(fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles)
    VALUES(:fname, :sname, :oname, :email, :supervisor, :gender, :department, :positions, :grade, :appointment, :roles)""",
    {'fname':fname, 'sname':sname, 'oname':oname, 'email':email, 'supervisor':supervisor, 'gender':gender, 'department':department, 'positions':positions, 'grade':grade, 'appointment':appointment, 'roles':roles}) # INSERT STAFF DETAILS INTO TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "staff has been created"})

async def create_staff_auth(fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await create_staff(fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        


# CREATE STAFF ROLES
async def create_roles(role_description:str, db:Session):
    res = db.execute(""" INSERT INTO public.roles(role_description) VALUES(:role_description) """, {'role_description': role_description}) # TABLE INSERTION
    db.commit()
    return JSONResponse(status_code=200, content={"message": "role has been created"})

async def create_roles_auth(role_description:str, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await create_roles(role_description ,db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})         


# CREATE DEADLINES
async def create_deadline(deadline_type, start_date, ending, db:Session):
    res = db.execute("""insert into public.deadline(deadline_type,start_date,ending)
    values(:deadline_type, :start_date, :ending) on conflict (deadline_type) do 
	update set deadline_type = EXCLUDED.deadline_type, start_date = EXCLUDED.start_date, ending = EXCLUDED.ending;""",
    {'deadline_type':deadline_type, 'start_date':start_date, 'ending':ending}) # INSERT DEADLINES INTO TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "deadline has been created"})

async def create_deadline_auth(deadline_type:str, start_date:str, ending:str, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        print(data)
        if data==1:
            return await create_deadline(deadline_type, start_date, ending, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})



# UPDATE STAFF DETAILS
async def update_staff(staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles,  db:Session):
    res = db.execute("""UPDATE public.staff
    SET staff_id=:staff_id, fname=:fname, sname=:sname, oname=:oname, email=:email, supervisor=:supervisor, gender=:gender, department=:department, positions=:positions, grade=:grade, appointment=:appointment, roles=:roles
    WHERE staff_id=:staff_id;""",
    {'staff_id':staff_id, 'fname':fname, 'sname':sname, 'oname':oname, 'email':email, 'supervisor':supervisor, 'gender':gender, 'department':department, 'positions':positions, 'grade':grade, 'appointment':appointment, 'roles':roles}) # UPDATE STAFF IN STAFF TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "staff has been updated"})

async def update_staff_auth(staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await update_staff(staff_id, fname, sname, oname, email, supervisor, gender, department, positions, grade, appointment, roles, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"}) 


# UPDATE STAFF ROLES
async def update_roles(role_id, role_description, db:Session):
    res = db.execute(""" UPDATE public.roles SET role_id=:role_id, role_description=:role_description WHERE role_id=:role_id; """,
    {'role_id':role_id, 'role_description': role_description}) # UPDATE ROLES IN ROLES TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "role has been updated"})

async def update_roles_auth(role_id:int, role_description:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await create_roles(role_id, role_description ,db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# UPDATE DEADLINES
async def update_deadline(deadline:schemas.update_deadline, db:Session):
    res = db.execute("""UPDATE public.deadline
	SET deadline_id=:deadline_id, deadline_type=:deadline_type, start_date=:start_date, ending=:ending
	WHERE deadline_id=:deadline_id;""",
    {'deadline_id':deadline.deadline_id, 'deadline_type':deadline.deadline_type, 'start_date':deadline.start_date, 'ending':deadline.ending}) # UPDATE IN TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "deadline has been updated"})

async def update_deadline_auth(deadline:schemas.update_deadline, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        print(data)
        if data==1:
            return await update_deadline(deadline, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})



# DELETE STAFF DETAILS
async def delete_staff(staff_id:int, db: Session):
    res = db.execute("""DELETE FROM public.staff 
	WHERE staff_id = :staff_id;""",
    {'staff_id':staff_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message":"staff has been deleted"})

async def delete_staff_auth(staff_id:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await delete_staff(staff_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"}) 


# DELETE ROLES
async def delete_roles(role_id:int, db: Session):
    res = db.execute(""" DELETE FROM public.roles WHERE role_id = :role_id; """, {'role_id':role_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "role has been deleted"})

async def delete_roles_auth(role_id:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await delete_roles(role_id ,db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# DELETE DEADLINES
async def delete_deadline(deadline_id: int, db: Session):
    res = db.execute("""DELETE FROM public.deadline
	WHERE deadline_id=:deadline_id;""",
    {'deadline_id':deadline_id})
    db.commit() 
    return JSONResponse(status_code=200, content={"message": "deadline has been deleted"})

async def delete_deadline_auth(deadline_id:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        print(data)
        if data==1:
            return await delete_deadline(deadline_id, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})
    


