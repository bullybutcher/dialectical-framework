from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import uuid4

# Import your core classes
from dialectical_framework.wisdom_unit import WisdomUnit
from dialectical_framework.dialectical_component import DialecticalComponent
from dialectical_framework.synthesist.factories.wheel_builder import WheelBuilder
from dialectical_framework.synthesist.factories.wheel_builder_config import WheelBuilderConfig
from dialectical_framework.analyst.thought_mapping import ThoughtMapping
from dialectical_framework.wheel import Wheel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Simple in-memory store (replace with DB in production)
SESSIONS = {}

class SessionCreateRequest(BaseModel):
    user_message: str

class WisdomUnitInput(BaseModel):
    t_minus: str
    t: str
    t_plus: str
    a_plus: str
    a: str
    a_minus: str

class WheelCreateRequest(BaseModel):
    wisdom_units: List[WisdomUnitInput]

class WheelAutoRequest(BaseModel):
    number_of_thoughts: int = Field(default=3, ge=1)
    component_length: int = Field(default=7, ge=1)

class RedefineRequest(BaseModel):
    redefine: Dict[str, str]
    component_length: int = Field(default=7, ge=1)

class ThoughtMappingRequest(BaseModel):
    number_of_thoughts: int = Field(default=3, ge=1)

@app.post("/api/session")
def create_session(data: SessionCreateRequest):
    session_id = str(uuid4())
    SESSIONS[session_id] = {
        "user_message": data.user_message,
        "wheels": [],
        "cycles": []
    }
    return {"session_id": session_id, "user_message": data.user_message}

@app.post("/api/session/{session_id}/wheel")
def add_wheel(session_id: str, data: WheelCreateRequest):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    wisdom_units = [
        WisdomUnit(
            t_minus=DialecticalComponent.from_str("T-", wu.t_minus),
            t=DialecticalComponent.from_str("T", wu.t),
            t_plus=DialecticalComponent.from_str("T+", wu.t_plus),
            a_plus=DialecticalComponent.from_str("A+", wu.a_plus),
            a=DialecticalComponent.from_str("A", wu.a),
            a_minus=DialecticalComponent.from_str("A-", wu.a_minus)
        ) for wu in data.wisdom_units
    ]
    wheel = Wheel(wisdom_units)
    session["wheels"].append(wheel)
    return {"wheel_id": len(session["wheels"]) - 1, "wisdom_units": data.wisdom_units}

@app.post("/api/session/{session_id}/wheel/auto")
async def auto_build_wheel(session_id: str, data: WheelAutoRequest):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    wbc = WheelBuilderConfig(component_length=data.component_length)
    factory = WheelBuilder(config=wbc, text=session["user_message"])
    wheels = await factory.build(theses=[None] * data.number_of_thoughts)
    wheel_objs = [wheel for wheel in wheels]
    session["wheels"].extend(wheel_objs)
    # Serialize for response
    response = []
    for wheel in wheels:
        response.append({
            "wisdom_units": [wu.__dict__ for wu in wheel.wisdom_units]
        })
    return {"wheels": response}

@app.patch("/api/session/{session_id}/wheel/{wheel_id}")
async def redefine_wheel(session_id: str, wheel_id: int, data: RedefineRequest):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    try:
        wheel = session["wheels"][wheel_id]
    except IndexError:
        raise HTTPException(404, "Wheel not found")
    wbc = WheelBuilderConfig(component_length=data.component_length)
    wb = WheelBuilder.load(
        text=session["user_message"],
        config=wbc,
        wheels=[wheel]
    )
    # Redefine with new theses
    new_wheels = await wb.redefine(data.redefine)
    session["wheels"][wheel_id] = new_wheels[0]
    return {"wheel_id": wheel_id, "wisdom_units": [wu.__dict__ for wu in new_wheels[0].wisdom_units]}

@app.post("/api/session/{session_id}/thought-mapping")
async def thought_mapping(session_id: str, data: ThoughtMappingRequest):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    reasoner = ThoughtMapping(session["user_message"])
    cycles = await reasoner.extract(data.number_of_thoughts)
    session["cycles"] = cycles
    # Serialize for response
    response = []
    for cycle in cycles:
        response.append({
            "dialectical_components": [dc.__dict__ for dc in cycle.dialectical_components]
        })
    return {"cycles": response}

@app.get("/api/session/{session_id}")
def get_session(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    # Basic serialization for wheels/cycles
    wheels = [
        {"wisdom_units": [wu.__dict__ for wu in wheel.wisdom_units]}
        for wheel in session["wheels"]
    ]
    cycles = [
        {"dialectical_components": [dc.__dict__ for dc in cycle.dialectical_components]}
        for cycle in session.get("cycles", [])
    ]
    return {
        "user_message": session["user_message"],
        "wheels": wheels,
        "cycles": cycles
    }

@app.get("/api/session/{session_id}/cycles/pretty")
def get_pretty_cycles(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    cycles = session.get("cycles", [])
    if not cycles:
        raise HTTPException(404, "No cycles found")
    
    # Get pretty formatted cycles
    pretty_cycles = []
    for cycle in cycles:
        pretty_output = cycle.pretty(skip_dialectical_component_explanation=True)
        pretty_cycles.append(pretty_output)
    
    return {"pretty_cycles": pretty_cycles}

@app.get("/api/session/{session_id}/cycles/structured")
def get_structured_cycles(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    cycles = session.get("cycles", [])
    if not cycles:
        raise HTTPException(404, "No cycles found")
    
    # Get structured cycles with machine-readable data
    structured_cycles = []
    for cycle in cycles:
        # Build sequence array
        if cycle.causality_direction == "clockwise":
            sequence = [dc.alias for dc in cycle.dialectical_components]
        else:
            sequence = [dc.alias for dc in reversed(cycle.dialectical_components)]
        
        # Build concepts mapping
        concepts = {}
        for dc in cycle.dialectical_components:
            concepts[dc.alias] = {
                "statement": dc.statement,
                "explanation": dc.explanation
            }
        
        structured_cycle = {
            "sequence": sequence,
            "probability": cycle.probability,
            "causality_direction": cycle.causality_direction,
            "concepts": concepts,
            "reasoning": cycle.reasoning_explanation,
            "argumentation": cycle.argumentation
        }
        structured_cycles.append(structured_cycle)
    
    return {"cycles": structured_cycles}

@app.get("/api/session/{session_id}/wheels/cycles/structured")
def get_wheel_cycles_structured(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    wheels = session.get("wheels", [])
    if not wheels:
        raise HTTPException(404, "No wheels found")
    
    # Get structured cycles from wheels (which have T/A aliases)
    structured_cycles = []
    for wheel in wheels:
        if wheel.cycle is None:
            continue
            
        cycle = wheel.cycle
        # Build sequence array
        if cycle.causality_direction == "clockwise":
            sequence = [dc.alias for dc in cycle.dialectical_components]
        else:
            sequence = [dc.alias for dc in reversed(cycle.dialectical_components)]
        
        # Build concepts mapping
        concepts = {}
        for dc in cycle.dialectical_components:
            concepts[dc.alias] = {
                "statement": dc.statement,
                "explanation": dc.explanation
            }
        
        structured_cycle = {
            "sequence": sequence,
            "probability": cycle.probability,
            "causality_direction": cycle.causality_direction,
            "concepts": concepts,
            "reasoning": cycle.reasoning_explanation,
            "argumentation": cycle.argumentation
        }
        structured_cycles.append(structured_cycle)
    
    return {"cycles": structured_cycles}

@app.get("/api/session/{session_id}/wheel/{wheel_id}/wisdom-units")
def get_wheel_wisdom_units(session_id: str, wheel_id: int):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    wheels = session.get("wheels", [])
    if not wheels:
        raise HTTPException(404, "No wheels found")
    
    try:
        wheel = wheels[wheel_id]
    except IndexError:
        raise HTTPException(404, f"Wheel {wheel_id} not found")
    
    # Return wisdom units as they are (same format as session endpoint)
    return {
        "wheel_id": wheel_id,
        "wisdom_units": [wu for wu in wheel.wisdom_units]
    }