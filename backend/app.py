from litestar import Litestar, get, post, put, Request, MediaType
from litestar.config.cors import CORSConfig
from typing import Dict, Any

from src.db_handler import *
from src.openai_handler import *
from src.text_similarity import *


cors_config = CORSConfig(allow_origins=["http://localhost:8081"])


#################################### BASE-DATA ####################################

@post("/create-base-data-entry")
async def create_base_data_entry(request: Request) -> dict:
    data = await request.json()
    entry = insert_base(data)
    return dict(
        status="success",
        message=f"Entry created for {data.get('firstname')}",
        entry=entry
    )

################################# SEMESTER-DATA #################################

@get("/get-all-pupils-data")
async def get_all_pupils_data() -> Dict[str, Any]:
    data = get_all_pupils()
    return dict(
        status="success",
        message=f"Found all students",
        data=data
    )


@get("/get-pupil-data/{student_id:str}")
async def get_pupil_data(student_id:str) -> Dict[str, Any]:
    data = get_pupil(student_id)
    return dict(
        status="success",
        message=f"Entry found for student with ID {student_id}",
        data=data
    )


@post("/create-semester-data")
async def create_semester_data(request:Request) -> dict:
    data = await request.json()
    entry = insert_semester(data)
    return dict(
        status="success",
        message=f"Entry created for {data.get('semester_name')}",
        entry=entry
    )
    
################################# ASSESSMENTS-DATA #################################

@get("/get-all-semesters-data/{student_id:str}")
async def get_all_semesters_data(student_id:str) -> Dict[str, Any]:
    data = get_all_semesters(student_id)
    return dict(
        status="success",
        message=f"Found all semesters for student with ID {student_id}",
        data=data
    )

@get("/get-semester-data/{semester_id:str}")
async def get_semester_data(semester_id:str) -> Dict[str, Any]:
    data = get_semester(semester_id)
    return dict(
        status="success",
        message=f"Found semester with ID {semester_id}",
        data=data
    )

@post("/create-assessment-data")
async def create_assessment_data(request:Request) -> dict:
    data = await request.json()
    entry = insert_assessement(data)
    return dict(
        status="success",
        message=f"Successfully added assessement for student with ID {data.get('student_id')}",
        entry=entry
    )

################################# COMBINE #################################

@get("/get-all-assessments-data/{semester_id:str}")
async def get_all_assessments_data(semester_id:str) -> Dict[str, Any]:
    data = get_all_assessments(semester_id)
    return dict(
        status="success",
        message=f"Found all assessments for semester with ID {semester_id}",
        data=data,
    )
    
    
@post("/get-note-recommendation")
async def get_note_recommendation(request:Request) -> Dict[str, Any]:
    data = await request.json()
    notes = await get_recommendation_notes(data["student"], data["assessments"])
    return dict(
        status="success",
        message=f"Created recommendation for teacher's notes",
        notes=notes,
    )


@post("/get-notes-similarity")
async def get_notes_similarity(request:Request) -> Dict[str, Any]:
    data = await request.json()
    similarity = notes_similarity(data)
    return dict(
        status="success",
        message=f"Similarity calculated",
        similarity=similarity
    )


@put("/create-final-assessment-data/{semester_id:str}")
async def create_final_assessment_data(semester_id:str, request:Request) -> dict:
    data = await request.json()
    entry = insert_final_assessment(semester_id, data)
    return dict(
        status="success",
        message=f"Added final assessment to semester with ID {semester_id}",
        entry=entry
    )

################################# CREATE-TEXT #################################


@get("/semesters-with-final-assessment/{student_id:str}")
async def get_all_semesters_with_final_assessments(student_id:str) -> Dict[str, Any]:
    data = get_semesters_with_final_assessments(student_id)
    return dict(
        status="success",
        message=f"Found all final assessments for student with ID {student_id}",
        data=data
    )


@post("/generate-first-text")
async def get_first_text_recommendation(request:Request) -> Dict[str, Any]:
    data = await request.json()
    answer, chain = await get_first_text(data)
    return dict(
        status="success",
        message=f"Created Text",
        answer=answer,
        chain=chain,
    )


@post("/generate-second-text")
async def get_second_text_recommendation(request:Request) -> Dict[str, Any]:
    data = await request.json()    
    answer, chain = await get_other_text(data)
    return dict(
        status="success",
        message=f"Created Text",
        answer=answer,
        chain=chain,
    )


@post("/get-text-similarity")
async def get_text_similarity(request:Request) -> Dict[str, Any]:
    data = await request.json()
    similarity = text_similarity(data)
    print(similarity)
    return dict(
        status="success",
        message=f"Similarity calculated",
        similarity=similarity,
    )
    

@put("/create-final-text-data/{semester_id:str}")
async def create_final_text_data(semester_id:str, request:Request) -> dict:
    data = await request.json()
    entry = insert_final_text(semester_id, data)
    return dict(
        status="success",
        message=f"Added final text to the semester with ID {semester_id}",
        entry=entry,
    )


@post("/store-similarity")
async def store_similarity_data(request:Request) -> dict:
    data = await request.json()
    entry = store_validation(data)
    return dict(
        status="success",
        message=f"Added validation to DB",
        entry=entry,
    )



app = Litestar(
    [
        create_base_data_entry,
        get_all_pupils_data,
        get_pupil_data,
        create_semester_data,
        get_all_semesters_data,
        get_semester_data,
        create_assessment_data,
        get_all_assessments_data,
        create_final_assessment_data,
        get_all_semesters_with_final_assessments,
        get_note_recommendation,
        get_notes_similarity,
        get_first_text_recommendation,
        get_second_text_recommendation,
        get_text_similarity,
        create_final_text_data,
        store_similarity_data,
    ], cors_config=cors_config
)