import os

import dotenv
import openai



def get_api_key():
    dotenv.load_dotenv()
    os.getenv("OPENAI_APIKEY")
    return os.getenv("OPENAI_APIKEY")


def anonymise(student, text):
    if student["gender"].lower()=="männlich":
        aliasname = "[John]"
    else:
        aliasname = "[Jane]"
    alias_text = text.replace(student["firstname"], aliasname)
    return alias_text
    
    
def format_prompt_content(semester, student):
    allgemeines_lernen = {
        "AktivTeilnehmen": 'aktiv am Unterricht teilnehmen',
        "LeistungZeigen": 'im Unterricht Leistung zeigen',
        "AufmerksamSein": 'während dem Unterricht Aufmerksam sein und den Instruktionen der Lehrperson folgen',
        "SchulinhalteMerken": 'sich schulische Inhalte merken',
        "SchulinhalteAbrufen": 'schulische Inhalte bei Bedarf abrufen',
    }
    assessment = semester["final_assessment"]["allgemeines_lernen"]
    text = "\n".join(
        f" - {student['firstname']} kann {v['assessment']} {allgemeines_lernen[k]} {v['notes']}"
        for k, v in assessment.items()
    )
    return anonymise(student, text)


def prepare_first_prompt(semester, student):
    system_content = f"""
    Du wirst eine Evaluation eines Schülers oder einer Schülerin bekommen.
    Die Evaluation wird in kurzen einfachen Sätzen sein.
    Dein Task ist es, diese Sätze zu einem Fliesstext zusammenzubringen.
    Der Fliesstext soll professionell sein.
    Der Fliesstext soll nur Informationen enthalten, die von der Evaluation mitgegeben werden.
    Der Fliesstext soll die Schweizer Rechtschreibung nutzen, das heisst, Scharf-S wird durch Doppel-S ersetzt.
    """
    first_prompt = f"""
    Bitte mache aus der folgenden Einschätzung einen professionellen Fliesstext:
    {format_prompt_content(semester, student)}
    """
    return [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": """
    John Doe kann gut aktiv am Unterricht teilnehmen.
    John Doe kann gut im schulischen Umfeld Leistung zeigen.
    John Doe kann nicht immer während des Unterrichts Aufmerksam sein und den Instruktionen der Lehrperson folgen.
    John Doe kann teilweise sich schulische Inhalte merken.
    John Doe kann noch nicht schulische Inhalte bei Bedarf abrufen.
            """
        },
        {
            "role": "assistant",
            "content": """
    John Doe gelingt es gut, aktiv am Unterricht teilzunehmen.
    Ausserdem zeigt er meist gute Leistungen im schulischen Umfeld.
    Er kann jedoch während des Unterrichts nicht immer Aufmerksam sein und den Instruktionen der Lehrperson folgen.
    Ausserdem hat John Doe teilweise Mühe, sich schulische Inhalte zu merken.
    Auch gelingt es ihm noch nicht, die gemerkten Inhalte bei Bedarf abzurufen.
            """
        },
        {
            "role": "user",
            "content": """
    Jane Doe kann teilweise aktiv am Unterricht teilnehmen.
    Jane Doe kann nicht immer im schulischen Umfeld Leistung zeigen.
    Jane Doe kann gut während des Unterrichts Aufmerksam sein und den Instruktionen der Lehrperson folgen.
    Jane Doe kann gut sich schulische Inhalte merken.
    Jane Doe kann teilweise schulische Inhalte bei Bedarf abrufen.
            """
        },
        {
            "role": "assistant",
            "content": """
    Jane Doe kann nur teilweise aktiv am Unterricht teilnehmen.
    Nicht immer gelingt es ihr im schulischen Umfeld Leistungen zu zeigen.
    Sie kann jedoch gut während des Unterrichts Aufmerksam sein und den Instruktionen der Lehrperson folgen.
    Ausserdem merkt sie sich schulische Inhalte gut, kann diese jedoch nur teilweise bei Bedarf abrufen.
            """
        },
        {
            "role": "user",
            "content": first_prompt
        },
    ]


def _openai(messages) -> openai.types.chat.chat_completion.Choice:
    """
    Request is sent to OpenAI
    Return the response in a ChatCompletion-Object
    """
    model_result = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
        top_p=1,
    )
    response = model_result.choices[0]
    chain = messages + [response.message]
    return response.message.content, chain


def get_text(data):
    messages = prepare_first_prompt(data["semester"], data["student"])
    openai.api_key = get_api_key()
    answer, chain = _openai(messages)
    print("Checkpoint")
    return answer, chain