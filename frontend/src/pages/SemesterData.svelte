<script>
    import { push } from 'svelte-spa-router';


    let students = []
    let student = {}
    let student_id

    let visible = false

    let semester_name=''
    let grade_level=''
    let niveau=''
    let last_progress_talk=''
    let last_report=''

    $: {
        getAllPupils()
    }


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
        visible = true
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }


    async function createSemester() {
        const variable_data = {
            "student_id":student_id,
            "semester_name":semester_name,
            "grade_level":grade_level,
            "niveau":niveau,
            "last_progress_talk":last_progress_talk,
            "last_report":last_report,
            "final_assessment":null,
            "final_text":null
        };
        const response = await fetch('http://localhost:8000/create-semester-data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(variable_data)
        });
        const responseData = await response.json();
        if (response.ok) {
            console.log('Success:', responseData);
            alert("Semester wurde angelegt.")
            push('/assessment');
        } else {
            console.error('Failed to create entry:', responseData);
            alert("Irgendwas ist schief gelaufen.")
        }
    }


    function cancel() {
        if (confirm('Möchten Sie das Formular wirklich leeren?')) {  
            semester=''
            grade_level=''
            niveau=''
            last_progress_talk=''
            last_report=''
        }
    }
    
</script>
    
    <div class="component">

        <h1>
            Semester Daten anglegen 
        </h1>
        <select class="form-control" bind:value={student_id} on:change={getPupil} id="student_id" required>
            <option value="">Schüler</option>
            {#each students as student}
              <option value={student._id}>{student.firstname} {student.lastname}</option>
            {/each}
        </select>

    {#if visible}
    
    <div class="abschnitt">
        <h2>Stammdaten von {student.firstname} {student.lastname}</h2>
        <table class="table">
            <tr>
              <th class="left">Geburtsdatum</th>
              <th class="right">Eintritt</th>
            <tr>
                <td>
                    {student.birthday}
                </td>
                <td>
                    {student.school_entry}
                </td>
            </tr>
            <tr>
                <th>Klassenlehrperson</th>
                <th>Heilpädagogin</th>
            </tr>
            <tr>
                <td>
                    {student.class_teacher}
                </td>
                <td>
                    {student.special_education_teacher}
                </td>
            </tr>
            <tr>
                <th>Diagnose</th>
                <th>Nachteilsausgleich</th>
            </tr>
            <tr>
                <td>
                    {student.diagnsoe}
                </td>
                <td>
                    {student.compensation}
                </td>
            </tr>
        </table>
    </div>  

    <h2>Semester Daten</h2>

    <form on:submit|preventDefault={createSemester}>
        <div class="abschnitt">
            <select class="form-control" bind:value={semester_name} id="Semester" required>
                <option value="">Semester</option>
                <option value="FS22">FS22</option>
                <option value="HS22">HS22</option>
                <option value="FS23">FS23</option>
                <option value="HS23">HS23</option>
                <option value="FS24">FS24</option>
            </select>


            <table class="table">
                <tr>
                    <th class="left">Klassenstufe</th>
                    <th class="right">Niveau</th>
                </tr>
                <tr>
                    <td class="form">
                        <select class="form-control" bind:value={grade_level} id="Klassenstufe" required>
                            <option value="">Klassenstufe</option>
                            <option value="4.Klasse">4. Klasse</option>
                            <option value="5.Klasse">5. Klasse</option>
                            <option value="6.Klasse">6. Klasse</option>
                            <option value="1.Sekundarstufe">1. Sekundarstufe</option>
                            <option value="2.Sekundarstufe">2. Sekundarstufe</option>
                            <option value="3.Sekundarstufe">3. Sekundarstufe</option>
                            <option value="10.Schuljahr">10. Schuljahr</option>
                        </select>
                    </td>
                    <td class="form">
                        <select class="form-control" bind:value={niveau} id="Niveau" required>
                            <option value="">Niveau</option>
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="keines">keines</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <th>Letztes Standortgespräch</th>
                    <th>Letzter Bericht</th>
                </tr>
                <tr>
                    <td class="form">
                        <select class="form-control" bind:value={last_progress_talk} id="Standortgespaech">
                            <option value="">Letztes Standortgespräch</option>
                            <option value="keines">keines</option>
                            <option value="FS22">FS23</option>
                            <option value="HS22">HS23</option>
                            <option value="FS23">FS24</option>
                            <option value="HS23">HS24</option>
                            <option value="FS24">FS24</option>
                        </select>
                    </td>
                    <td class="form">
                        <select class="form-control" bind:value={last_report} id="Bericht">
                            <option value="">Letzter Bericht</option>
                            <option value="keines">keiner</option>
                            <option value="FS22">FS22</option>
                            <option value="HS22">HS22</option>
                            <option value="FS23">FS23</option>
                            <option value="HS23">HS23</option>
                            <option value="FS24">FS24</option>
                        </select>
                    </td>
                </tr>
            </table>
        </div>
        <button type="submit">Bestätigen</button>
        <button type="button" on:click={cancel}>Abbrechen</button>
    </form>
    {/if}
</div>
      
<style>
  .left, .right {
    width: 50%;
  }

  .form {
    background-color: white;
  }
</style>
    