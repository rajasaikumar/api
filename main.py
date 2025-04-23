from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import re


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

employee_counter = 1


class Employee(BaseModel):
    first_name: str 
    last_name: str 
    gender: str 
    dob: date
    mobileno: int 
    email: EmailStr
    address: str 
    employee_id: str 
    joiningdate: date
    employee_id: str = None 

    @model_validator(mode="after")
    def validate_dates(self):
        today = date.today()

        if self.dob > today:
            raise ValueError("Date of birth cannot be in the future.")

        age = (today - self.dob).days // 365
        if age < 18:
            raise ValueError("Employee must be at least 18 years old.")

        if self.joiningdate > today:
            raise ValueError("Joining date cannot be in the future.")

        if self.joiningdate < self.dob:
            raise ValueError("Joining date cannot be before date of birth.")

        return self


employee_list: List[Employee] = []

@app.get("/db")
async def DBdata():
    return employee_list

# Get method for employee list
@app.get("/", response_class=HTMLResponse)
async def get_employee_list(request: Request):
    return templates.TemplateResponse("employeelist.html", {"request": request, "employees": employee_list})


@app.get("/form", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})





@app.get("/employees", response_model=List[Employee])
async def get_employees():
    return employee_list


@app.post("/employees")
async def add_employee(employee: Employee):
    print(employee)
    if not employee.employee_id:
        employee.employee_id = f"EMP{employee_counter:04d}"
        employee_counter += 1

    
   
    if not employee.first_name or not re.fullmatch(r"^[A-Za-z]+$", employee.first_name):
        raise HTTPException(status_code=400, detail="First name must contain only letters")

    if not employee.last_name or not re.fullmatch(r"^[A-Za-z]+$", employee.last_name):
        raise HTTPException(status_code=400, detail="Last name must contain only letters")

    if employee.gender not in ["Male", "Female", "Other"]:
        raise HTTPException(status_code=400, detail="Gender must be Male, Female, or Other")

    if not employee.mobileno or not (1000000000 <= employee.mobileno <= 9999999999):
        raise HTTPException(status_code=400, detail="Mobile number must be a valid 10-digit number")

    if not employee.address or len(employee.address) < 5:
        raise HTTPException(status_code=400, detail="Address must be at least 5 characters")

    if not employee.employee_id or not re.fullmatch(r"^[A-Za-z0-9]{3,15}$", employee.employee_id):
        raise HTTPException(status_code=400, detail="Employee ID must be alphanumeric (3–15 characters)")

    for emp in employee_list:
        if emp.employee_id == employee.employee_id:
            raise HTTPException(status_code=409, detail="Employee ID already exists")
        if emp.mobileno == employee.mobileno:
            raise HTTPException(status_code=409, detail="Mobile number already exists")
        if emp.email == employee.email:
            raise HTTPException(status_code=409, detail="Email already exists")
       
    employee_list.append(employee)

    
    return {"message": "Employee added successfully"}

