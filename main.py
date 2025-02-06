from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
import math
import requests
from fastapi.responses import JSONResponse


app = FastAPI(
    title="Number Classification API"
)

class Num(BaseModel):
    number: int


    
@app.get("/")
def home():
    return {"message": "Hello, Welcome to Number Classification API"}

@app.post("/is_armstrong")
def check_armstrong(request: Num):
    num = request.number  

    if num < 0:
        return False
    
    num = str(abs(num))
    power = len(num)
    total = sum(int(digit) ** power for digit in num)

    return total == int(num)

@app.post("/is_prime")
def check_prime(request: Num):
    num = request.number

    if num < 2:
        return False

    for i in range(2, int(math.sqrt(abs(num))) + 1):
        if num % i == 0:
            return False
  
    return True

@app.post("/is_perfect")
def check_perfect(request: Num):
    num = request.number

    if num <= 1:
       return False

    divisors_sum = sum(i for i in range(1, abs(num)) if num % i == 0)

    return divisors_sum == num

@app.post("/digit_sum")
def check_digit_sum(request: Num):
    num = request.number

    digit_sum = sum(int(digit) for digit in str(abs(num)))
    return digit_sum

@app.post("/properties")
def check_properties(request: Num):

    properties = []
    num = request.number

    if check_armstrong(request):  
        properties.append("armstrong")

    if check_prime(request): 
        properties.append("prime")

    if check_perfect(request):  
        properties.append("perfect")

    if num % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    return properties

@app.post("/get_fun_fact")
def get_fun_fact(request: Num):
    num = request.number

    try:
        response = requests.get(f"http://numbersapi.com/{num}/math")
        if response.status_code == 200:
            return response.text
        
        return f"{num} is an interesting number with various mathematical properties."
    
    except:
        return f"{num} is an interesting number with various mathematical properties."
    
@app.post("/api/classify-number")
def classify_number(request: Num):

    try:
        num = request.number

        response = {
            "number": num,
            "is_prime": check_prime(request),
            "is_perfect": check_perfect(request),
            "properties": check_properties(request),
            "digit_sum": check_digit_sum(request),
            "fun_fact": get_fun_fact(request)
        }

        return response

    except ValidationError: 
        error_response = {
            "number": request.number,
            "error": True
        }
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )