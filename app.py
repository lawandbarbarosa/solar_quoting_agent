from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from main import agent



load_dotenv()
app = FastAPI(title="Local host api execution")


@app.get("/")
def root():
    return {"Status": "Simko Solar api", "version": "1.0"}


class quote_request(BaseModel):
    Location: str
    monthly_bill: int
    roof_type: List[str]
    shading: str
    battery_intrest: str
    Primary_goal: str

class quote_result(BaseModel):
    research_node: str
    draft_node: str
    refine_node: str

@app.post("/generate_quote", response_model=quote_result)
async def generate_quote(request: quote_request):
    """
    Triggers the LangGraph agent to research, draft, and refine 
    a quoting based on user input.
    """
    try:
        initial_state = {
            "Location": request.Location,
            "monthly_bill": request.monthly_bill,
            "roof_type": request.roof_type,
            "shading": request.shading,
            "battery_intrest": request.battery_intrest,
            "Primary_goal": request.Primary_goal,
        
            "research_notes": "",   # ✅ was 'research_node'
            "draft_quoting": "",    # ✅ was 'draft_node'
            "final_quote": ""       # ✅ was 'refine_node'
        }

        result = agent.invoke(initial_state)

        return quote_result (
            research_node=result['research_notes'],   # ✅ was 'research_node'
            draft_node=result['draft_quoting'],        # ✅ was 'draft_node'
            refine_node=result['final_quote'] 
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8001)