<script>
    import { push } from "svelte-spa-router";


    export let params = {};


    $: {
            semester_id = params.semester_id
            student_id = params.student_id
            getAllAssessmentsDirectly()
    };
  
    let student_id
    let semester_id
    let assessments=[]
    let semester={}
    let student={}
    let visible=false
    let recommendation='Zusätzliche Anmerkungen Vorschlag'

    let AktivTeilnehmen=semester["AktivTeilnehmen"]
    let AktivTeilnehmenNotizen=semester.AktivTeilnehmenNotizen
    let LeistungZeigen=semester.LeistungZeigen
    let LeistungZeigenNotizen=semester.LeistungZeigenNotizen
    let AufmerksamSein=semester.AufmerksamSein
    let AufmerksamSeinNotizen=semester.AufmerksamSeinNotizen
    let SchulinhalteMerken=semester.SchulinhalteMerken
    let SchulinhalteMerkenNotizen=semester.SchulinhalteMerkenNotizen
    let SchulinhalteAbrufen=semester.SchulinhalteAbrufen
    let SchulinhalteAbrufenNotizen=semester.SchulinhalteAbrufenNotizen
  


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

    async function getSemester() {
        const response = await fetch('http://localhost:8000/get-semester-data/' + semester_id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const responseData = await response.json();
        semester = responseData.data


        AktivTeilnehmen=semester.final_assessment.allgemeines_lernen.AktivTeilnehmen.assessment
        AktivTeilnehmenNotizen=semester.final_assessment.allgemeines_lernen.AktivTeilnehmen.notes
        LeistungZeigen=semester.final_assessment.allgemeines_lernen.LeistungZeigen.assessment
        LeistungZeigenNotizen=semester.final_assessment.allgemeines_lernen.LeistungZeigen.notes
        AufmerksamSein=semester.final_assessment.allgemeines_lernen.AufmerksamSein.assessment
        AufmerksamSeinNotizen=semester.final_assessment.allgemeines_lernen.AufmerksamSein.notes
        SchulinhalteMerken=semester.final_assessment.allgemeines_lernen.SchulinhalteMerken.assessment
        SchulinhalteMerkenNotizen=semester.final_assessment.allgemeines_lernen.SchulinhalteMerken.notes
        SchulinhalteAbrufen=semester.final_assessment.allgemeines_lernen.SchulinhalteAbrufen.assessment
        SchulinhalteAbrufenNotizen=semester.final_assessment.allgemeines_lernen.SchulinhalteAbrufen.notes


        if (response.ok) {
            console.log('Success:', responseData);
        } else {
            console.error('Failed to find student:', responseData);
        }
    }
  
      async function getAllAssessmentsDirectly(){
        const response = await fetch('http://localhost:8000/get-all-assessments-data/' + semester_id, {
              method: 'GET',
              headers: {
                  'Content-Type': 'application/json'
              },
          });
          const responseData = await response.json();
          assessments = responseData.data
          if (response.ok) {
                getSemester()
                getPupil()
                console.log('Success:', responseData);
                console.log(assessments[0])
          } else {
              console.error('Failed to find student:', responseData);
          }
      }

  
    async function createFinalAssessment() {
        const assessment_data = {
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
        const response = await fetch('http://localhost:8000/create-final-assessment-data/' +semester_id, {
            method: 'PUT',
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
                push('/combine')
            }
            else {
                push('/create-text')
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
  

    function checkAnswers() {
        if (AktivTeilnehmen===''){
            alert("Bitte eine Bewertung eingeben.")
            scroll('aktivteilnehmen')
        }
        else if (LeistungZeigen===''){
            alert("Bitte eine Bewertung eingeben.")
            scroll('leistungzeigen')
        }
        else if (AufmerksamSein===''){
            alert("Bitte eine Bewertung eingeben.")
            scroll('aufmerksamsein')
        }
        else if (SchulinhalteMerken===''){
            alert("Bitte eine Bewertung eingeben.")
            scroll('schulinhaltemerken')
        }
        else if (SchulinhalteAbrufen===''){
            alert("Bitte eine Bewertung eingeben.")
            scroll('schulinhalteabrufen')
        }
        else {
            createFinalAssessment()
        }
    }

    function scroll(id) {
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            console.error('Element with ID ' + id + ' not found.');
        }
    }

    function changeVisibility() {
        visible=true
    }

  </script>
      
  <div class="component">
      <h1>
          Zusammenführen
      </h1>
  
      <h2>Studentname: {student.firstname} {student.lastname}</h2>
      <h2>Semester: {semester.semester_name}</h2>

      <form on:submit|preventDefault={checkAnswers}>


        {#if visible}

<!-- ################################### AKTIV AM UNTERRICHT TEILNEHMEN ################################### -->

            <div class="abschnitt" id="aktivteilnehmen">
                <h2>Aktiv am Unterricht teilnehmen</h2>
                <div class="table-responsive">
                    <table class="table">
                        <tr>
                            <th>Autor</th>
                            <th>Bewertung</th>
                            <th>Anmerkungen</th>
                        </tr>
                        {#each assessments as assessment}
                            <tr>
                                <td class="author">{assessment.author}</td>
                                <td class="assessment">{assessment.allgemeines_lernen.AktivTeilnehmen.assessment}</td>
                                <td>{assessment.allgemeines_lernen.AktivTeilnehmen.notes}</td>
                            </tr>
                        {/each}
                        <tr>
                            <td>Finale Bewertung</td>
                            <td>
                                <div class="custom-control">
                                    <input type="radio" value="sehr gut" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivSehrGut" required>
                                    <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="gut" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivGut" required>
                                    <label class="custom-control-label" for="AktivGut">gut</label>
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="teilweise" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivTeilweise" required>
                                    <label class="custom-control-label" for="AktivTeilweise">teilweise</label>  
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="nicht immer" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivNichtImmer" required>
                                    <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                                </div>               
                                <div class="custom-control">
                                    <input type="radio" value="noch nicht" bind:group={AktivTeilnehmen} class="custom-control-input" id="AktivNochNicht" required>
                                    <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                                </div>
                            </td>
                            <td>
                                <textarea bind:value={AktivTeilnehmenNotizen} class="form-control" rows="5" placeholder={recommendation}></textarea>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>

<!-- ################################### LEISTUNGEN ZEIGEN ################################### -->

            <div class="abschnitt" id="leistungzeigen">
                <h2>Leistungen zeigen</h2>
                <div class="table-responsive">
                    <table class="table">
                        <tr>
                            <th>Autor</th>
                            <th>Bewertung</th>
                            <th>Anmerkungen</th>
                        </tr>
                        {#each assessments as assessment}
                            <tr>
                                <td class="author">{assessment.author}</td>
                                <td class="assessment">{assessment.allgemeines_lernen.LeistungZeigen.assessment}</td>
                                <td>{assessment.allgemeines_lernen.LeistungZeigen.notes}</td>
                            </tr>
                        {/each}
                        <tr>
                            <td>Finale Bewertung</td>
                            <td>
                                <div class="custom-control">
                                    <input type="radio" value="sehr gut" bind:group={LeistungZeigen} class="custom-control-input" id="AktivSehrGut" required>
                                    <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="gut" bind:group={LeistungZeigen} class="custom-control-input" id="AktivGut" required>
                                    <label class="custom-control-label" for="AktivGut">gut</label>
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="teilweise" bind:group={LeistungZeigen} class="custom-control-input" id="AktivTeilweise" required>
                                    <label class="custom-control-label" for="AktivTeilweise">teilweise</label>  
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="nicht immer" bind:group={LeistungZeigen} class="custom-control-input" id="AktivNichtImmer" required>
                                    <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                                </div>               
                                <div class="custom-control">
                                    <input type="radio" value="noch nicht" bind:group={LeistungZeigen} class="custom-control-input" id="AktivNochNicht" required>
                                    <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                                </div>
                            </td>
                            <td>
                                <textarea bind:value={LeistungZeigenNotizen} class="form-control" rows="5" placeholder={recommendation}></textarea>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>

<!-- ################################### AUFMERKSAM SEIN ################################### -->
  
            <div class="abschnitt" id="aufmerksamsein">
                <h2>Aufmerksam sein</h2>
                <div class="table-responsive">
                    <table class="table">
                        <tr>
                            <th>Autor</th>
                            <th>Bewertung</th>
                            <th>Anmerkungen</th>
                        </tr>
                        {#each assessments as assessment}
                            <tr>
                                <td class="author">{assessment.author}</td>
                                <td class="assessment">{assessment.allgemeines_lernen.AufmerksamSein.assessment}</td>
                                <td>{assessment.allgemeines_lernen.AufmerksamSein.notes}</td>
                            </tr>
                        {/each}
                        <tr>
                            <td>Finale Bewertung</td>
                            <td>
                                <div class="custom-control">
                                    <input type="radio" value="sehr gut" bind:group={AufmerksamSein} class="custom-control-input" id="AktivSehrGut" required>
                                    <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="gut" bind:group={AufmerksamSein} class="custom-control-input" id="AktivGut" required>
                                    <label class="custom-control-label" for="AktivGut">gut</label>
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="teilweise" bind:group={AufmerksamSein} class="custom-control-input" id="AktivTeilweise" required>
                                    <label class="custom-control-label" for="AktivTeilweise">teilweise</label>  
                                </div>
                                <div class="custom-control">
                                    <input type="radio" value="nicht immer" bind:group={AufmerksamSein} class="custom-control-input" id="AktivNichtImmer" required>
                                    <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                                </div>               
                                <div class="custom-control">
                                    <input type="radio" value="noch nicht" bind:group={AufmerksamSein} class="custom-control-input" id="AktivNochNicht" required>
                                    <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                                </div>
                            </td>
                            <td>
                                <textarea bind:value={AufmerksamSeinNotizen} class="form-control" rows="5" placeholder={recommendation}></textarea>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
  
  <!-- ################################### SCHULINHALTE MERKEN ################################### -->
  
            <div class="abschnitt" id="schulinhaltemerken">
                <h2>Schulinhalte merken</h2>
                <div class="table-responsive">
                    <table class="table">
                        <tr>
                            <th>Autor</th>
                            <th>Bewertung</th>
                            <th>Anmerkungen</th>
                        </tr>
                        {#each assessments as assessment}
                            <tr>
                                <td class="author">{assessment.author}</td>
                                <td class="assessment">{assessment.allgemeines_lernen.SchulinhalteMerken.assessment}</td>
                                <td>{assessment.allgemeines_lernen.SchulinhalteMerken.notes}</td>
                            </tr>
                        {/each}
                        <tr>
                            <td>Finale Bewertung</td>
                            <td>
                                <div class="custom-control" required>
                                    <input type="radio" value="sehr gut" bind:group={SchulinhalteMerken} class="custom-control-input" id="AktivSehrGut">
                                    <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                                </div>
                                <div class="custom-control" required>
                                    <input type="radio" value="gut" bind:group={SchulinhalteMerken} class="custom-control-input" id="AktivGut">
                                    <label class="custom-control-label" for="AktivGut">gut</label>
                                </div>
                                <div class="custom-control" required>
                                    <input type="radio" value="teilweise" bind:group={SchulinhalteMerken} class="custom-control-input" id="AktivTeilweise">
                                    <label class="custom-control-label" for="AktivTeilweise">teilweise</label>  
                                </div>
                                <div class="custom-control" required>
                                    <input type="radio" value="nicht immer" bind:group={SchulinhalteMerken} class="custom-control-input" id="AktivNichtImmer">
                                    <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                                </div>               
                                <div class="custom-control" required>
                                    <input type="radio" value="noch nicht" bind:group={SchulinhalteMerken} class="custom-control-input" id="AktivNochNicht">
                                    <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                                </div>
                            </td>
                            <td>
                                <textarea bind:value={SchulinhalteMerkenNotizen} class="form-control" rows="5" placeholder={recommendation}></textarea>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
  
<!-- ################################### SCHULINHALTE ABRUFEN ################################### -->
  
            <div class="abschnitt" id="schulinhalteabrufen">
                <h2>Schulinhalte abrufen</h2>
                <div class="table-responsive">
                    <table class="table">
                        <tr>
                            <th>Autor</th>
                            <th>Bewertung</th>
                            <th>Anmerkungen</th>
                        </tr>
                        {#each assessments as assessment}
                            <tr>
                                <td class="author">{assessment.author}</td>
                                <td class="assessment">{assessment.allgemeines_lernen.SchulinhalteAbrufen.assessment}</td>
                                <td>{assessment.allgemeines_lernen.SchulinhalteMerken.notes}</td>
                            </tr>
                        {/each}
                        <tr>
                            <td>Finale Bewertung</td>
                            <td>
                                <div class="custom-control" required>
                                    <input type="radio" value="sehr gut" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AktivSehrGut">
                                    <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                                </div>
                                <div class="custom-control" required>
                                    <input type="radio" value="gut" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AktivGut">
                                    <label class="custom-control-label" for="AktivGut">gut</label>
                                </div>
                                <div class="custom-control" required>
                                    <input type="radio" value="teilweise" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AktivTeilweise">
                                    <label class="custom-control-label" for="AktivTeilweise">teilweise</label>  
                                </div>
                                <div class="custom-control" required>
                                    <input type="radio" value="nicht immer" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AktivNichtImmer">
                                    <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                                </div>               
                                <div class="custom-control" required>
                                    <input type="radio" value="noch nicht" bind:group={SchulinhalteAbrufen} class="custom-control-input" id="AktivNochNicht">
                                    <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                                </div>
                            </td>
                            <td>
                                <textarea bind:value={SchulinhalteAbrufenNotizen} class="form-control" rows="5" placeholder={recommendation}></textarea>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>

            {/if}
<!-- ################################### ABSENDEN ################################### -->
        
        <div class="abschnitt">
            <h2>Übersicht</h2>
            <div class="table-responsive">
                <table class="table">
                    <tr>
                        <th class="author">Bereich</th>
                        <th class="assessment">Bewertung</th>
                        <th class="notes">Anmerkungen</th>
                        <th class="correction">Korrektur</th>
                    </tr>
                    <tr>
                        <td>
                            Aktiv teilnehmen
                        </td>
                        <td>
                            {AktivTeilnehmen}
                        </td>
                        <td>
                            {AktivTeilnehmenNotizen}
                        </td>
                        <td>
                            <button type="button" on:click={changeVisibility} on:click={() => scroll('aktivteilnehmen')}>Korrigieren</button>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Leistung zeigen
                        </td>
                        <td>
                            {LeistungZeigen}
                        </td>
                        <td>
                            {LeistungZeigenNotizen}
                        </td>
                        <td>
                            <button type="button" on:click={changeVisibility} on:click={() => scroll('leistungzeigen')}>Korrigieren</button>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Aufmerksam sein
                        </td>
                        <td>
                            {AufmerksamSein}
                        </td>
                        <td>
                            {AufmerksamSeinNotizen}
                        </td>
                        <td>
                            <button type="button" on:click={changeVisibility} on:click={() => scroll('aufmerksamsein')}>Korrigieren</button>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Schulinhalte merken
                        </td>
                        <td>
                            {SchulinhalteMerken}
                        </td>
                        <td>
                            {SchulinhalteMerkenNotizen}
                        </td>
                        <td>
                            <button type="button" on:click={changeVisibility} on:click={() => scroll('schulinhaltemerken')}>Korrigieren</button>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Schulinhalte abrufen
                        </td>
                        <td>
                            {SchulinhalteAbrufen}
                        </td>
                        <td>
                            {SchulinhalteAbrufenNotizen}
                        </td>
                        <td>
                            <button type="button" on:click={changeVisibility} on:click={() => scroll('schulinhalteabrufen')}>Korrigieren</button>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
            <div class="abschnitt">
                <button type="submit">Bestätigen</button>
                <button type="button" on:click={cancel}>Abbrechen</button>
            </div>
    </form>
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
  
      .table {
        padding: 0px;
      }

      .custom-control {
          display: block; /* Ensures each control group starts on a new line */
          padding: 0px;
      }

      textarea {
        background-color: white;
      }
  
      .custom-control-input {
          vertical-align: middle; /* Aligns the radio button vertically with the text */
          padding: 0px;
      }
  
      .custom-control-label {
          display: inline-block; /* Keeps label on the same line as the radio button */
          padding: 0px;
      }

      .author {
        width: 200px;
      }

      .assessment {
        width: 150px;
      }

      .notes {
        width: auto;
      }

      .correction {
        width: 100px;
      }

  </style>
      