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
            "final_assessment":{},
            "text":{}
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
        <table>
            <tr>
                <th>Geburtsdatum</th>
                <th>Eintritt</th>
            </tr>
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

            <table>
                <tr>
                    <th>Klassenstufe</th>
                    <th>Niveau</th>
                </tr>
                <tr>
                    <td>
                        <select class="form-control" bind:value={grade_level} id="Klassenstufe" required>
                            <option value="">Klassenstufe</option>
                            <option value="4.Klasse">4. Klasse</option>
                            <option value="5.Klasse">5. Klasse</option>
                            <option value="6.Klasse">6. Klasse</option>
                            <option value="7.Klasse">7. Klasse</option>
                            <option value="8.Klasse">8. Klasse</option>
                            <option value="9.Klasse">9. Klasse</option>
                            <option value="10.Klasse">10. Klasse</option>
                        </select>
                    </td>
                    <td>
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
                    <th>Letzter Bericht</th>
                    <th>Letztes Standortgespräch</th>
                </tr>
                <tr>
                    <td>
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
                    <td>
                        <select class="form-control" bind:value={last_report} id="Bericht">
                            <option value="">Letzter Bericht</option>
                            <option value="keines">keines</option>
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

</style>
    