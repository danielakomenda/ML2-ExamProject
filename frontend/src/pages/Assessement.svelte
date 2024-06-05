<script>
  import { push } from "svelte-spa-router";

$: {
    getAllPupils()
}

    let students=[]
    let semesters=[]
    let semester={}

    let student_id
    let semester_id

    let visible = false

    let author
    let AktivTeilnehmen=''
    let AktivTeilnehmenNotizen=null
    let LeistungZeigen=''
    let LeistungZeigenNotizen=null
    let AufmerksamSein=''
    let AufmerksamSeinNotizen=null
    let SchulinhalteMerken=''
    let SchulinhalteMerkenNotizen=null
    let SchulinhalteAbrufen=''
    let SchulinhalteAbrufenNotizen=null


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
            console.error('Failed to find pupil:', responseData);
        }
    }


    async function getSemestersOfPupil() {
        const response = await fetch('http://localhost:8000/get-all-semesters-data/' + student_id, {
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


    function handleSemesterChange() {
        if (semester_id === 'new') {
            newSemester();
        } else {
            getSemester();
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
        visible = true
        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }


    async function newSemester() {
        push('/semester-data')
    }


    async function createAssessment() {
        const assessment_data = {
            "student_id": student_id,
            "semester_id": semester_id,
            "author": author,
            "allgemeines_lernen": {
                "AktivTeilnehmen": {
                    "assessment": AktivTeilnehmen,
                    "notes": AktivTeilnehmenNotizen,
                },
                "LeistungZeigen":{
                    "assessment": LeistungZeigen,
                    "notes": LeistungZeigenNotizen,
                },
                "AufmerksamSein": {
                    "assessment": AufmerksamSein,
                    "notes": AufmerksamSeinNotizen,
                },
                "SchulinhalteMerken": {
                    "assessment" :SchulinhalteMerken,
                    "notes": SchulinhalteMerkenNotizen,
                },
                "SchulinhalteAbrufen": {
                    "assessment": SchulinhalteAbrufen,
                    "notes": SchulinhalteAbrufenNotizen,
                },
            }
        };
        const response = await fetch('http://localhost:8000/create-assessment-data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(assessment_data)
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

    
    function cancel() {
        if (confirm('Möchten Sie das Formular wirklich leeren?')) {
            author=''
            AktivTeilnehmen=''
            AktivTeilnehmenNotizen=''
            LeistungZeigen=''
            LeistungZeigenNotizen=''
            AufmerksamSein=''
            AufmerksamSeinNotizen=''
            SchulinhalteMerken=''
            SchulinhalteMerkenNotizen=''
            SchulinhalteAbrufen=''
            SchulinhalteAbrufenNotizen=''
        }
    }


</script>
    
<div class="component">
    <h1>
        Einschätzungen
    </h1>

    <select class="form-control" bind:value={student_id} on:change={getSemestersOfPupil} id="student_id" required>
        <option value="">Schüler</option>
        {#each students as student}
            <option value={student._id}>{student.firstname}</option>
        {/each}
    </select>

    <select class="form-control" bind:value={semester_id} on:change={handleSemesterChange} id="Semester" required>
        <option value="">Semester</option>
        {#each semesters as semester}
            <option value={semester._id}>{semester.semester_name}</option>
        {/each}
        <option value="new">Semester anlegen</option>
    </select>


    {#if visible}

    <div class="abschnitt">
        <h2>Semesterdaten</h2>
        <table>
            <tr>
                <th>Semester</th>
            </tr>
            <tr>
                <td>
                    {semester.semester_name}
                </td>
            </tr>
            <tr>
                <th>Klassenstufe</th>
                <th>Niveau</th>
            </tr>
            <tr>
                <td>
                    {semester.grade_level}
                </td>
                <td>
                    {semester.niveau}
                </td>
            </tr>
            <tr>
                <th>Letztes Standortgespräch</th>
                <th>Letzter Bericht</th>
            </tr>
            <tr>
                <td>
                    {semester.last_progress_talk}
                </td>
                <td>
                    {semester.last_report}
                </td>
            </tr>
        </table>
    </div>  

    <form on:submit|preventDefault={createAssessment}>
        
        <div class="abschnitt">
            <div class="custom-control">
                <label class="custom-control-label" for="Autor">Autor</label>
                <input type="text" bind:value={author} class="custom-control-input" id="Autor" required>
            </div>
        </div>

<!-- ################################### AKTIV AM UNTERRICHT TEILNEHMEN ################################### -->

        <div class="abschnitt">
            <h2>Aktiv am Unterricht teilnehmen</h2>
            <p><b>Frage: Wie gut kann {name} aktiv am Unterricht teilnehmen?</b></p>                
            <div class="custom-control">
                <input type="radio" value="sehr gut" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivSehrGut">
                <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="gut" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivGut">
                <label class="custom-control-label" for="AktivGut">gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="teilweise" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivTeilweise">
                <label class="custom-control-label" for="AktivTeilweise">teilweise</label>  
            </div>
            <div class="custom-control">
                <input type="radio" value="nicht immer" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivNichtImmer">
                <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
            </div>               
            <div class="custom-control">
                <input type="radio" value="noch nicht" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivNochNicht">
                <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
            </div>               
            <p>Gibt es Beispiele oder weitere Anmerkungen?</p>
            <textarea bind:value={AktivTeilnehmenNotizen} class="form-control" rows="3" placeholder="Zusätzliche Anmerkungen"></textarea>
        </div>

<!-- ################################### LEISTUNGEN ZEIGEN ################################### -->

        <div class="abschnitt">
            <h2>Leistungen zeigen</h2>
            <p><b>Frage: Wie gut kann {name} während dem Unterricht Leistungen zeigen?</b></p>            
            <div class="custom-control">
                <input type="radio" value="sehr gut" bind:group={LeistungZeigen} class="custom-control-input" id="LeistungSehrGut">
                <label class="custom-control-label" for="LeistungSehrGut">sehr gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="gut" bind:group={LeistungZeigen} class="custom-control-input" id="LeistungGut">
                <label class="custom-control-label" for="LeistungGut">gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="teilweise" bind:group={LeistungZeigen} class="custom-control-input" id="LeistungTeilweise">
                <label class="custom-control-label" for="LeistungTeilweise">teilweise</label>  
            </div>
            <div class="custom-control">
                <input type="radio" value="nicht immer" bind:group={LeistungZeigen} class="custom-control-input" id="LeistungNichtImmer">
                <label class="custom-control-label" for="LeistungNichtImmer">nicht immer</label>
            </div>           
            <div class="custom-control">
                <input type="radio" value="noch nicht" bind:group={LeistungZeigen} class="custom-control-input" id="LeistungNochNicht">
                <label class="custom-control-label" for="LeistungNochNicht">noch nicht</label>
            </div>            
            <p>Gibt es Beispiele oder weitere Anmerkungen?</p>
            <textarea bind:value={LeistungZeigenNotizen} class="form-control" rows="3" placeholder="Zusätzliche Anmerkungen"></textarea>
        </div>

<!-- ################################### AUFMERKSAM SEIN ################################### -->

        <div class="abschnitt">
            <h2>Aufmerksam sein</h2>
            <p><b>Frage: Wie gut kann {name} während dem Unterricht aufmerksam sein und folgen?</b></p>        
            <div class="custom-control">
                <input type="radio" value="sehr gut" bind:group={AufmerksamSein} class="custom-control-input" id="AufmerksamSehrGut">
                <label class="custom-control-label" for="AufmerksamSehrGut">sehr gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="gut" bind:group={AufmerksamSein} class="custom-control-input" id="AufmerksamGut">
                <label class="custom-control-label" for="AufmerksamGut">gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="teilweise" bind:group={AufmerksamSein} class="custom-control-input" id="AufmerksamTeilweise">
                <label class="custom-control-label" for="AufmerksamTeilweise">teilweise</label>  
            </div>
            <div class="custom-control">
                <input type="radio" value="nicht immer" bind:group={AufmerksamSein} class="custom-control-input" id="AufmerksamNichtImmer">
                <label class="custom-control-label" for="AufmerksamNichtImmer">nicht immer</label>
            </div>       
            <div class="custom-control">
                <input type="radio" value="noch nicht" bind:group={AufmerksamSein} class="custom-control-input" id="AufmerksamNochNicht">
                <label class="custom-control-label" for="AufmerksamNochNicht">noch nicht</label>
            </div>        
            <p>Gibt es Beispiele oder weitere Anmerkungen?</p>
            <textarea bind:value={AufmerksamSeinNotizen} class="form-control" rows="3" placeholder="Zusätzliche Anmerkungen"></textarea>
        </div>

<!-- ################################### SCHULINHALTE MERKEN ################################### -->

        <div class="abschnitt">
            <h2>Schulinhalte merken</h2>
            <p><b>Frage: Wie gut kann sich {name} Schulinhalte merken?</b></p>             
            <div class="custom-control">
                <input type="radio" value="sehr gut" bind:group={SchulinhalteMerken} class="custom-control-input" id="MerkenSehrGut">
                <label class="custom-control-label" for="MerkenSehrGut">sehr gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="gut" bind:group={SchulinhalteMerken} class="custom-control-input" id="MerkenGut">
                <label class="custom-control-label" for="MerkenGut">gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="teilweise" bind:group={SchulinhalteMerken} class="custom-control-input" id="MerkenTeilweise">
                <label class="custom-control-label" for="MerkenTeilweise">teilweise</label>  
            </div>
            <div class="custom-control">
                <input type="radio" value="nicht immer" bind:group={SchulinhalteMerken} class="custom-control-input" id="MerkenNichtImmer">
                <label class="custom-control-label" for="MerkenNichtImmer">nicht immer</label>
            </div>           
            <div class="custom-control">
                <input type="radio" value="noch nicht" bind:group={SchulinhalteMerken} class="custom-control-input" id="MerkenNochNicht">
                <label class="custom-control-label" for="MerkenNochNicht">noch nicht</label>
            </div>            
            <p>Gibt es Beispiele oder weitere Anmerkungen?</p>
            <textarea bind:value={SchulinhalteMerkenNotizen} class="form-control" rows="3" placeholder="Zusätzliche Anmerkungen"></textarea>
        </div>

<!-- ################################### SCHULINHALTE ABRUFEN ################################### -->

        <div class="abschnitt">
            <h2>Schulinhalte abrufen</h2>
            <p><b>Frage: Wie gut kann {name} Schulinhalte bei Bedarf abrufen?</b></p>        
            <div class="custom-control">
                <input type="radio" value="sehr gut" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AbrufenSehrGut">
                <label class="custom-control-label" for="AbrufenSehrGut">sehr gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="gut" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AbrufenGut">
                <label class="custom-control-label" for="AbrufenGut">gut</label>
            </div>
            <div class="custom-control">
                <input type="radio" value="teilweise" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AbrufenTeilweise">
                <label class="custom-control-label" for="AbrufenTeilweise">teilweise</label>  
            </div>
            <div class="custom-control">
                <input type="radio" value="nicht immer" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AbrufenNichtImmer">
                <label class="custom-control-label" for="AbrufenNichtImmer">nicht immer</label>
            </div>       
            <div class="custom-control">
                <input type="radio" value="noch nicht" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AbrufenNochNicht">
                <label class="custom-control-label" for="AbrufenNochNicht">noch nicht</label>
            </div>  
            <p>Gibt es Beispiele oder weitere Anmerkungen?</p>
            <textarea bind:value={SchulinhalteAbrufenNotizen} class="form-control" rows="3" placeholder="Zusätzliche Anmerkungen"></textarea>
        </div>

        <div class="abschnitt">
            <button type="submit">Bestätigen</button>
            <button type="button" on:click={cancel}>Abbrechen</button>
        </div>
    </form>
    {/if}
</div>
      

<style>
    .abschnitt {
        padding-top: 20px;
        padding-bottom: 10px;
        margin-top: 5px;
        margin-bottom: 10px;
        border-top-style: solid;
        border-top-color: gray;
        border-top-width: 2px;
    }

    .custom-control {
        margin-top: 10px; /* Adds space between groups */
        display: block; /* Ensures each control group starts on a new line */
    }

    .custom-control-input {
        vertical-align: middle; /* Aligns the radio button vertically with the text */
        margin-right: 10px; /* Space between radio button and label */
    }

    .custom-control-label {
        display: inline-block; /* Keeps label on the same line as the radio button */
    }

    p {
        padding-top: 10px;
        margin-bottom: 5px;
    }

    h2 {
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
    