import os
import json
import re
from typing import Any

import dotenv
import openai


# criteria
allgemeines_lernen = {
    "AktivTeilnehmen": 'aktiv am Unterricht teilnehmen',
    "LeistungZeigen": 'im Unterricht Leistung zeigen',
    "AufmerksamSein": 'während dem Unterricht Aufmerksam sein und den Instruktionen der Lehrperson folgen',
    "SchulinhalteMerken": 'sich schulische Inhalte merken',
    "SchulinhalteAbrufen": 'schulische Inhalte bei Bedarf abrufen',
}


def get_api_key():
    dotenv.load_dotenv()
    os.getenv("OPENAI_APIKEY")
    return os.getenv("OPENAI_APIKEY")
    

def _openai(messages, chain=True) -> openai.types.chat.chat_completion.Choice:
    """
    Request is sent to OpenAI
    Return the response in a ChatCompletion-Object
    """
    openai.api_key = get_api_key()
    model_result = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
        top_p=1,
    )
    response = model_result.choices[0]
    if chain:
        chain = messages + [response.message]
        return response.message.content, chain
    return response.message.content


def anonymise(student, text):
    if student["gender"].lower()=="männlich":
        aliasname = "John"
    else:
        aliasname = "Jane"
    alias_text = text.replace(student["firstname"], aliasname)
    return alias_text


def deanonymise(student, text):
    if student["gender"].lower()=="männlich":
        aliasname = "John"
    else:
        aliasname = "Jane"
    alias_text = text.replace(aliasname, student["firstname"])
    return alias_text


#################################### COMBINE ####################################


def prompt_for_note_recommendation(notes):
    system_content = f"""
    Du wirst ein JSON-Object bekommen, das aus einem Key-Value-Pair besteht.
    Die Values sind mehrere Strings, die mit einem Komma getrennt wurden.
    Dein Task ist es, die Strings so zusammenzusetzen, dass sie einen Fliesstext ergeben.
    Der Fliesstext soll professionell sein.
    Der Fliesstext soll nur Informationen enthalten, die in den Values mitgegeben werden.
    Der Fliesstext soll die Schweizer Rechtschreibung nutzen, das heisst, Scharf-S wird durch Doppel-S ersetzt.
    Die Antwort soll ein JSON-Object sein.
    Der Key soll dabei unverändert bleiben und die Values sollen mit dem Fliesstext ersetzt werden.
    """
    first_prompt = f"""
    Bitte mache aus den Values des folgenden Dictionary einen professionellen Fliesstext:
    {notes}
    """
    return [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": """
    'AktivTeilnehmen': {'insbesondere bei Fächer, die ihn interessieren', 'insbesondere in Physik und Chemie'}
    'SchulinhalteAbrufen': {'sehr Themenabhängig', 'manchmal, manchmal nicht', 'grundsätzlich schon, aber nur, wenn es ihn interessiert'}
    'AufmerksamSein': {'wenn er einen schlechten Tag hat, geht es nicht', 'meistens gelingt es gut, ausser er hat private Probleme'}
    'SchulinhalteMerken': {'wenn ihn das Thema interessiert', 'nur bei speziellen Themen', 'an guten Tagen', 'nicht unbedingt schulische Themen, aber sonst kann er sich viele Sachen merken'}
    'LeistungZeigen': {'häufig hat er Migräne', 'wenn er zu wenig geschlafen hat, ist es schwierig'}
            """
        },
        {
            "role": "assistant",
            "content": """
    'AktivTeilnehmen': {'Insbesondere bei Fächer, die ihn interessieren, wie beispielsweise Physik oder Chemie.'}
    'SchulinhalteAbrufen': {'Grundsätzlich gelingt es ihm, wenn ihn ein Thema interessiert. Manchmal ist es aber auch schwierig für ihn.'}
    'AufmerksamSein': {'Meistens gelingt es ihm, wenn er aber einen schlechten Tag oder Probleme in seinem privaten Umfeld hat, fällt es ihm schwer.'}
    'SchulinhalteMerken': {'Er hat grundsätzlich ein gutes Gedächtnis, aber nicht bei allen schulischen Themen, kann er sich die Inhalte merken. An guten Tagen geht es besser.'}
    'LeistungZeigen': {'wenn er Migräne hat oder zu wenig geschlafen hat, ist es schwierig. Leider kommt das häufiger vor.'}
            """
        },
        {
            "role": "user",
            "content": first_prompt
        },
    ]


def collect_notes(student, assessments):
    """Collects notes from criteria, if there is more than one note."""
    notes = dict()
    for assessment in assessments:
        for k, v in assessment["allgemeines_lernen"].items():
            if v["notes"]:
                notes.setdefault(k, []).append(anonymise(student, v["notes"]))
    notes = {k:v for k,v in notes.items() if len(v)>0}
    return notes



async def get_recommendation_notes(student, assessments: list[dict[str, Any]]) -> dict[str, str]:
    notes = collect_notes(student, assessments)    
    if notes:
        messages = prompt_for_note_recommendation(json.dumps(notes, ensure_ascii=False))
        print(messages) # to check, if anonymise() worked
        answer = _openai(messages, False)
        note_raw = json.loads(deanonymise(student, answer))
    else:
        note_raw = {}
    note = {}
    for k in allgemeines_lernen:
        v = note_raw.get(k)
        if isinstance(v, (list,tuple)):
            v = "".join(v)
        else:
            assert v is None or isinstance(v, str)
        note[k] = v or ""
    return note


#################################### CREATE-TEXT ####################################


def format_prompt_content(semester, student):
    assessment = semester["final_assessment"]["allgemeines_lernen"]
    text = "\n".join(
        f" - {student['firstname']} kann {v['assessment']} {allgemeines_lernen[k]} {v['notes']}"
        for k, v in assessment.items()
    )
    return anonymise(student, text)


def prompt_for_textgeneration(semester, student):
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


async def get_first_text(data):
    messages = prompt_for_textgeneration(data["semester"], data["student"])
    print(messages) # to check, if anonymise() worked
    answer, chain = _openai(messages)    
    return deanonymise(data["student"], answer), chain



#################################### FOLLOWUP-PROMPT ####################################


def prompt_for_follow_up(chain, prompt):
    chain.append({
        "role":"user",
        "content":prompt
    })


async def get_other_text(data):
    prompt_for_follow_up(data["chain"], anonymise(data["student"], data["prompt"]))
    print(data["chain"]) # to check, if anonymise() worked
    answer, chain = _openai(data["chain"])
    return deanonymise(data["student"], answer), chain