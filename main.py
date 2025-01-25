from fastapi import FastAPI , HTTPException# type: ignore
from pydantic import BaseModel, Field, conlist # type: ignore
from typing import Optional
from email_validator import validate_email, EmailNotValidError  # type: ignore


class Form(BaseModel):
    name: str
    age: int
    email: str 
    courses:list[str]

app = FastAPI()
# http://127.0.0.1:8000/students/9999?grade=false&semester=fall2025 
@app.get("/students/{student_id}")
def get_student(student_id: int,grade:bool,semester: Optional[str] = None):    
    try:
        if student_id<1000 or student_id>9999:
            raise HTTPException(status_code=422 , detail="Invalid Student ID")
         #  raise ValueError("Invalid Student ID")
        return { "student_id": student_id,
                     "status": "success"
                    ,"grade": grade
                    ,"semester": semester
                    
                }
    
    except Exception as e:
            return { 
                "message": str(e),
                "status": "error",
                "data": None
            }

@app.post("/students/register")
def register_student(form: Form):
    try:
        if(len(form.name)>50 or form.name.replace(" ", "").isalpha()==False):
            raise ValueError("Name is invalid")
        if(form.age<18 or form.age>30):
            raise ValueError("Age is invalid")
        email=validate_email(form.email)
        if(email ==False):
            raise ValueError("Email is invalid")
        if(len(form.courses)<1 or len(form.courses)>5):
            raise ValueError("invalid number of courses")
        seen = set()
        for course in form.courses:
            if not (5 <= len(course) <= 30):
                raise ValueError("Course name is invalid")
            if course in seen:
                raise ValueError("Duplicate course")
        
        return {
            
 
            "status": "success",
            "data": form
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": None	
        }
        
@app.put("/students/{student_id}/email")
def update_email(student_id: int, email: Form):
    try:
        
        if student_id<1000 or student_id>9999:
            raise HTTPException(status_code=422 , detail="Invalid Student ID")
            # raise ValueError("Invalid Student ID")
        if validate_email(email.email) == False:
            raise ValueError("Email is invalid")
        
        return {
            "status": "success",
            "message": "Email updated successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": None	
        }

        
