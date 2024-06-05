<script>
import { push } from "svelte-spa-router";

$: {
        getAllPupils()
    }

    let students=[]
    let student={}
    let semesters=[]
    let semester={}
    let final_assessment={}
    let student_id
    let semester_id
    let text=''
    let prompt=''

    let visible=false
    let textVisible=false
    let promptVisible=false

    async function getAllPupils() {
        const response = await fetch('http://localhost:8000/get-all-pupils-data/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const responseData = await response.json();
        students = responseData.data
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find any students:', responseData);
        }
    }


    async function getPupil() {
        const response = await fetch('http://localhost:8000/get-pupil-data/' + student_id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const responseData = await response.json();
        student = responseData.data
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }


    async function getSemestersWithFinalAssessment() {
        const response = await fetch('http://localhost:8000/semesters-with-final-assessment/' + student_id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const responseData = await response.json();
        semesters = responseData.data
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }


    async function getSemester() {
        const response = await fetch('http://localhost:8000/get-semester-data/' + semester_id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const responseData = await response.json();
        semester = responseData.data
        final_assessment = semester.final_assessment
        console.log(final_assessment.allgemeines_lernen)
        visible=true
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }


    function correctFinalAssessment() {
        push('/combine/' +semester_id +"/" +student_id);
    }


    async function getText() {
        const data = {
            semester:semester,
            student:student,
        }
        const response = await fetch('http://localhost:8000/generate-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        text = responseData.answer
        console.log(final_assessment.allgemeines_lernen)
        textVisible = true
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }


    async function createFinalText() {
        const finalText = {
            "allgemeines_lernen": text,
        };
        const response = await fetch('http://localhost:8000/create-final-text-data/' +semester_id, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(finalText)
        });
        const responseData = await response.json();
        if (response.ok) {
            console.log('Success:', responseData);
            if (confirm('Möchtest Du einen weiteren Schüler beurteilen?')){
                cancel()
                push('/assessment')
            }
            else {
                push('/combine')
            }
        } else {
             console.error('Failed to create entry:', responseData);
        }
    }


    function getFirstText() {

    }


    function changePromptVisibility() {
        promptVisible=true
    }


    function sendPrompt() {

    }

</script>

<div class="component">
<h1>Text generieren</h1>

<select class="form-control" bind:value={student_id} on:change={getSemestersWithFinalAssessment} on:change={getPupil} id="student_id" required>
    <option value="">Schüler</option>
    {#each students as student}
        <option value={student._id}>{student.firstname} {student.lastname}</option>
    {/each}
</select>

<select class="form-control" bind:value={semester_id} on:change={getSemester} id="Semester" required>
    <option value="">Semester</option>
    {#each semesters as semester}
        <option value={semester._id}>{semester.semester_name}</option>
    {/each}
</select>

{#if visible}
    <div class="abschnitt">
    <table class="table">
        <tr>
            <th class="assessment">Bewertung</th>
            <th class="notes">Anmerkungen</th>
        </tr>
        <tr>
            <td class="assessment">{final_assessment.allgemeines_lernen.AktivTeilnehmen.assessment}</td>
            <td>{final_assessment.allgemeines_lernen.AktivTeilnehmen.notes}</td>

        </tr>
        <tr>
            <td class="assessment">{final_assessment.allgemeines_lernen.LeistungZeigen.assessment}</td>
            <td>{final_assessment.allgemeines_lernen.LeistungZeigen.notes}</td>
        </tr>
        <tr>
            <td class="assessment">{final_assessment.allgemeines_lernen.AufmerksamSein.assessment}</td>
            <td>{final_assessment.allgemeines_lernen.AufmerksamSein.notes}</td>
        </tr>
        <tr>
            <td class="assessment">{final_assessment.allgemeines_lernen.SchulinhalteMerken.assessment}</td>
            <td>{final_assessment.allgemeines_lernen.SchulinhalteMerken.notes}</td>
        </tr>
        <tr>
            <td class="assessment">{final_assessment.allgemeines_lernen.SchulinhalteAbrufen.assessment}</td>
            <td>{final_assessment.allgemeines_lernen.SchulinhalteAbrufen.notes}</td>
        </tr>
    </table>
    <button type="button" on:click={getText}>Text generieren</button>
    <button type="button" on:click={correctFinalAssessment}>Korrigieren</button>
    </div>
{/if}

{#if textVisible}
    <div class="abschnitt">
        <div class="table-responsive">
            <table class="table">
                <tr class="styleless">
                    <th class="generatedTextHeader styleless"></th>
                    <th class="promptHeader styleless"></th>
                </tr>
                <tr class="styleless">
                    <td class="generatedText styleless">
                        {text}
                    </td>
                    <td class="styleless">
                    <button type="button" class="mybutton" on:click={createFinalText}>Beenden</button>
                    <button type="button" class="mybutton" on:click={changePromptVisibility}>Korrigieren</button>
                    </td>
                </tr>
                {#if promptVisible}
                    <tr class="styleless">
                        <td class="styleless"></td>
                        <td class="styleless prompt">
                            <input type="text" bind:value={prompt} placeholder="Was möchtest du ändern?">
                        </td>
                    </tr>
                {/if}
            </table>
        </div>
    </div>
{/if}


</div>
<style>
      .assessment {
        width: 150px;
      }

      .notes {
        width: auto;
      }

      .mybutton {
        padding:2px;
        border:1px solid gray;
        width: 100px;
      }

      .styleless{
        border-width: 0;
      }

      .generatedText, .prompt {
        background-color: white;
        border: 2px solid gray;
        width: max-content;
      }

      .generatedTextHeader, .promptHeader{
        width: 45%;
        margin: 0px;
        padding: 0px;
        border-width: 0px;
      }

      input {
        border-width: 0px;
        width: 100%;
      }

</style>