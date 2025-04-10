from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from datetime import date
from pydantic import BaseModel, EmailStr
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware  # Add this import

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

templates = Jinja2Templates(directory="templates")
         
@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# =============================================================================
# pydantic model for employee
class Employee(BaseModel):
    first_name:str
    last_name:str
    gender:str
    dob:date
    mobileno:int
    email:EmailStr
    address:str
    employee_id:int
    joiningdate:date


# hardcoded employee list
employee_list: List[Employee] =[]

# get method for getting details 
@app.get("/employee",response_model= List[Employee])
def get_employees():
    return employee_list


# post method for adding employee
@app.post("/add_employee",response_model=Employee)
def add_employee(employee:Employee):
    for emp in employee_list:
        if emp.employee_id == employee.employee_id:
            raise HTTPException(status_code=404, detail="employee_id already exists")
    employee_list.append(employee)
    return employee
        