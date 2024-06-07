<script>
  import { push } from "svelte-spa-router";
  import { tick } from "svelte";

  export let params = {};

  $: {
    semester_id = params.semester_id;
    student_id = params.student_id;
    getAllAssessmentsDirectly();
  }

  let student_id;
  let semester_id;

  let assessments = [];
  let student = {};
  let semester = {};

  let recommendation = {};
  let similarity = {};

  let formVisible = false;
  let overviewVisible = false;

  let AktivTeilnehmen = "";
  let AktivTeilnehmenNotizen = "";
  let LeistungZeigen = "";
  let LeistungZeigenNotizen = "";
  let AufmerksamSein = "";
  let AufmerksamSeinNotizen = "";
  let SchulinhalteMerken = "";
  let SchulinhalteMerkenNotizen = "";
  let SchulinhalteAbrufen = "";
  let SchulinhalteAbrufenNotizen = "";

  //////////////////////// GET ALL ASSESSMENTS DIRECTLY /////////////////////////
  async function getAllAssessmentsDirectly() {
    const response = await fetch("http://localhost:8000/get-all-assessments-data/" + semester_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    assessments = responseData.data;
    if (response.ok) {
      getSemester();
      getPupil();
        console.log("Success:", responseData);
        assessments = responseData.data;
      formVisible = true;
    } else {
      console.error("Failed to find assessment:", responseData);
    }
  }

  //////////////////////// GET SPECIFIC STUDENT /////////////////////////
  async function getPupil() {
    const response = await fetch("http://localhost:8000/get-pupil-data/" + student_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    student = responseData.data;
    if (response.ok) {
      console.log("Success:", responseData);
      if (student && semester){
      if (confirm("Möchtest Du für Notizen der Lehrpersonen von OpenAI einen Textvorschlag erhalten?")) {
          getNoteRecommendation();
        }
    }
    } else {
      console.error("Failed to find student:", responseData);
    }
  }

  //////////////////////// GET SPECIFIC SEMESTER /////////////////////////
  async function getSemester() {
    const response = await fetch("http://localhost:8000/get-semester-data/" + semester_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    semester = responseData.data;
    if (response.ok) {
      console.log("Success:", responseData);
    } else {
      console.error("Failed to find student:", responseData);
    }
  }

  //////////////////////// GET ALL ASSESSMENTS FOR THE GIVEN SEMESTER /////////////////////////
  async function getNoteRecommendation() {
    const data = {
      student: student,
      assessments: assessments,
    };
    if (semester_id) {
      const response = await fetch("http://localhost:8000/get-note-recommendation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      const responseData = await response.json();
      if (response.ok) {
        console.log("Success:", responseData);
        recommendation = responseData.notes;
        AktivTeilnehmenNotizen = recommendation.AktivTeilnehmen;
        LeistungZeigenNotizen = recommendation.LeistungZeigen;
        AufmerksamSeinNotizen = recommendation.AufmerksamSein;
        SchulinhalteMerkenNotizen = recommendation.SchulinhalteMerken;
        SchulinhalteAbrufenNotizen = recommendation.SchulinhalteAbrufen;
      }
    } else {
      console.error("Failed to find assessment:", responseData);
    }
  }

  //////////////////////// GET SIMILARITY OF ALL THE NOTES /////////////////////////
  async function getTextSimilarity() {
    const data = {
      recommended: recommendation,
      manually: {
        AktivTeilnehmen: AktivTeilnehmenNotizen,
        LeistungZeigen: LeistungZeigenNotizen,
        AufmerksamSein: AufmerksamSeinNotizen,
        SchulinhalteMerken: SchulinhalteMerkenNotizen,
        SchulinhalteAbrufen: SchulinhalteAbrufenNotizen,
      },
    };
    console.log(data);
    const response = await fetch("http://localhost:8000/get-notes-similarity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseData = await response.json();
    if (response.ok) {
      overviewVisible = true;
      console.log("Success:", responseData);
      similarity = responseData.similarity;
      console.log(similarity);
      await tick();
      scroll("bestaetigen");
    } else {
      console.error("Failed to create entry:", responseData);
    }
  }

  //////////////////////// CREATE FINAL ASSESSMENT /////////////////////////
  async function createFinalAssessment() {
    const assessment_data = {
      allgemeines_lernen: {
        AktivTeilnehmen: {
          assessment: AktivTeilnehmen,
          notes: AktivTeilnehmenNotizen,
        },
        LeistungZeigen: {
          assessment: LeistungZeigen,
          notes: LeistungZeigenNotizen,
        },
        AufmerksamSein: {
          assessment: AufmerksamSein,
          notes: AufmerksamSeinNotizen,
        },
        SchulinhalteMerken: {
          assessment: SchulinhalteMerken,
          notes: SchulinhalteMerkenNotizen,
        },
        SchulinhalteAbrufen: {
          assessment: SchulinhalteAbrufen,
          notes: SchulinhalteAbrufenNotizen,
        },
      },
    };
    const response = await fetch("http://localhost:8000/create-final-assessment-data/" + semester_id, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(assessment_data),
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      if (confirm("Möchtest Du den Text generieren lassen?")) {
        push("/create-text");
      } else {
        if (confirm("Möchtest Du eine weitere Beurteilung finalisieren?")) {
          cancel();
          push("/combine");
        }
      }
    } else {
      console.error("Failed to create entry:", responseData);
    }
  }

  //////////////////////// DELETE ALL THE FORM-DATA /////////////////////////
  function cancel() {
    if (confirm("Möchten Du das Formular wirklich leeren?")) {
      author = "";
      AktivTeilnehmen = "";
      AktivTeilnehmenNotizen = "";
      LeistungZeigen = "";
      LeistungZeigenNotizen = "";
      AufmerksamSein = "";
      AufmerksamSeinNotizen = "";
      SchulinhalteMerken = "";
      SchulinhalteMerkenNotizen = "";
      SchulinhalteAbrufen = "";
      SchulinhalteAbrufenNotizen = "";
    }
  }

  //////////////////////// CHECK IF ALL REQUIRED ANSWERS ARE THERE /////////////////////////
  function checkAnswers() {
    if (AktivTeilnehmen === "") {
      alert("Bitte eine Bewertung eingeben.");
      scroll("aktivteilnehmen");
    } else if (LeistungZeigen === "") {
      alert("Bitte eine Bewertung eingeben.");
      scroll("leistungzeigen");
    } else if (AufmerksamSein === "") {
      alert("Bitte eine Bewertung eingeben.");
      scroll("aufmerksamsein");
    } else if (SchulinhalteMerken === "") {
      alert("Bitte eine Bewertung eingeben.");
      scroll("schulinhaltemerken");
    } else if (SchulinhalteAbrufen === "") {
      alert("Bitte eine Bewertung eingeben.");
      scroll("schulinhalteabrufen");
    } else {
      createFinalAssessment();
    }
  }

  //////////////////////// SCROLL TO ID /////////////////////////
  function scroll(id) {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      console.error("Element with ID " + id + " not found.");
    }
  }
</script>

<div class="component">
  <h1>Zusammenführen</h1>

  <form on:submit|preventDefault={checkAnswers}>
    <!-- ################################### AKTIV AM UNTERRICHT TEILNEHMEN ################################### -->

    {#if formVisible}
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
                <td>
                  {#if assessment.allgemeines_lernen.AktivTeilnehmen.notes}
                    {assessment.allgemeines_lernen.AktivTeilnehmen.notes}
                  {/if}
                </td>
              </tr>
            {/each}
            <tr>
              <td>Finale Bewertung</td>
              <td>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="sehr gut"
                    bind:group={AktivTeilnehmen}
                    class="custom-control-input"
                    id="AktivSehrGut"
                    required
                  />
                  <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="gut"
                    bind:group={AktivTeilnehmen}
                    class="custom-control-input"
                    id="AktivGut"
                    required
                  />
                  <label class="custom-control-label" for="AktivGut">gut</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="teilweise"
                    bind:group={AktivTeilnehmen}
                    class="custom-control-input"
                    id="AktivTeilweise"
                    required
                  />
                  <label class="custom-control-label" for="AktivTeilweise">teilweise</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="nicht immer"
                    bind:group={AktivTeilnehmen}
                    class="custom-control-input"
                    id="AktivNichtImmer"
                    required
                  />
                  <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="noch nicht"
                    bind:group={AktivTeilnehmen}
                    class="custom-control-input"
                    id="AktivNochNicht"
                    required
                  />
                  <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                </div>
              </td>
              <td>
                <textarea
                  bind:value={AktivTeilnehmenNotizen}
                  class="form-control"
                  rows="5"
                  placeholder="Weitere Anmerkungen"
                />
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
                <td>
                  {#if assessment.allgemeines_lernen.LeistungZeigen.notes}
                    {assessment.allgemeines_lernen.LeistungZeigen.notes}
                  {/if}
                </td>
              </tr>
            {/each}
            <tr>
              <td>Finale Bewertung</td>
              <td>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="sehr gut"
                    bind:group={LeistungZeigen}
                    class="custom-control-input"
                    id="AktivSehrGut"
                    required
                  />
                  <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="gut"
                    bind:group={LeistungZeigen}
                    class="custom-control-input"
                    id="AktivGut"
                    required
                  />
                  <label class="custom-control-label" for="AktivGut">gut</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="teilweise"
                    bind:group={LeistungZeigen}
                    class="custom-control-input"
                    id="AktivTeilweise"
                    required
                  />
                  <label class="custom-control-label" for="AktivTeilweise">teilweise</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="nicht immer"
                    bind:group={LeistungZeigen}
                    class="custom-control-input"
                    id="AktivNichtImmer"
                    required
                  />
                  <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="noch nicht"
                    bind:group={LeistungZeigen}
                    class="custom-control-input"
                    id="AktivNochNicht"
                    required
                  />
                  <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                </div>
              </td>
              <td>
                <textarea
                  bind:value={LeistungZeigenNotizen}
                  class="form-control"
                  rows="5"
                  placeholder="Weitere Anmerkungen"
                />
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
                <td>
                  {#if assessment.allgemeines_lernen.AufmerksamSein.notes}
                    {assessment.allgemeines_lernen.AufmerksamSein.notes}
                  {/if}
                </td>
              </tr>
            {/each}
            <tr>
              <td>Finale Bewertung</td>
              <td>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="sehr gut"
                    bind:group={AufmerksamSein}
                    class="custom-control-input"
                    id="AktivSehrGut"
                    required
                  />
                  <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="gut"
                    bind:group={AufmerksamSein}
                    class="custom-control-input"
                    id="AktivGut"
                    required
                  />
                  <label class="custom-control-label" for="AktivGut">gut</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="teilweise"
                    bind:group={AufmerksamSein}
                    class="custom-control-input"
                    id="AktivTeilweise"
                    required
                  />
                  <label class="custom-control-label" for="AktivTeilweise">teilweise</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="nicht immer"
                    bind:group={AufmerksamSein}
                    class="custom-control-input"
                    id="AktivNichtImmer"
                    required
                  />
                  <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                </div>
                <div class="custom-control">
                  <input
                    type="radio"
                    value="noch nicht"
                    bind:group={AufmerksamSein}
                    class="custom-control-input"
                    id="AktivNochNicht"
                    required
                  />
                  <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                </div>
              </td>
              <td>
                <textarea
                  bind:value={AufmerksamSeinNotizen}
                  class="form-control"
                  rows="5"
                  placeholder="Weitere Anmerkungen"
                />
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
                <td>
                  {#if assessment.allgemeines_lernen.SchulinhalteMerken.notes}
                    {assessment.allgemeines_lernen.SchulinhalteMerken.notes}
                  {/if}
                </td>
              </tr>
            {/each}
            <tr>
              <td>Finale Bewertung</td>
              <td>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="sehr gut"
                    bind:group={SchulinhalteMerken}
                    class="custom-control-input"
                    id="AktivSehrGut"
                  />
                  <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="gut"
                    bind:group={SchulinhalteMerken}
                    class="custom-control-input"
                    id="AktivGut"
                  />
                  <label class="custom-control-label" for="AktivGut">gut</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="teilweise"
                    bind:group={SchulinhalteMerken}
                    class="custom-control-input"
                    id="AktivTeilweise"
                  />
                  <label class="custom-control-label" for="AktivTeilweise">teilweise</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="nicht immer"
                    bind:group={SchulinhalteMerken}
                    class="custom-control-input"
                    id="AktivNichtImmer"
                  />
                  <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="noch nicht"
                    bind:group={SchulinhalteMerken}
                    class="custom-control-input"
                    id="AktivNochNicht"
                  />
                  <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                </div>
              </td>
              <td>
                <textarea
                  bind:value={SchulinhalteMerkenNotizen}
                  class="form-control"
                  rows="5"
                  placeholder="Weitere Anmerkungen"
                />
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
                <td>
                  {#if assessment.allgemeines_lernen.SchulinhalteAbrufen.notes}
                    {assessment.allgemeines_lernen.SchulinhalteAbrufen.notes}
                  {/if}
                </td>
              </tr>
            {/each}
            <tr>
              <td>Finale Bewertung</td>
              <td>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="sehr gut"
                    bind:group={SchulinhalteAbrufen}
                    class="custom-control-input"
                    id="AktivSehrGut"
                  />
                  <label class="custom-control-label" for="AktivSehrGut">sehr gut</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="gut"
                    bind:group={SchulinhalteAbrufen}
                    class="custom-control-input"
                    id="AktivGut"
                  />
                  <label class="custom-control-label" for="AktivGut">gut</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="teilweise"
                    bind:group={SchulinhalteAbrufen}
                    class="custom-control-input"
                    id="AktivTeilweise"
                  />
                  <label class="custom-control-label" for="AktivTeilweise">teilweise</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="nicht immer"
                    bind:group={SchulinhalteAbrufen}
                    class="custom-control-input"
                    id="AktivNichtImmer"
                  />
                  <label class="custom-control-label" for="AktivNichtImmer">nicht immer</label>
                </div>
                <div class="custom-control" required>
                  <input
                    type="radio"
                    value="noch nicht"
                    bind:group={SchulinhalteAbrufen}
                    class="custom-control-input"
                    id="AktivNochNicht"
                  />
                  <label class="custom-control-label" for="AktivNochNicht">noch nicht</label>
                </div>
              </td>
              <td>
                <textarea
                  bind:value={SchulinhalteAbrufenNotizen}
                  class="form-control"
                  rows="5"
                  placeholder="Weitere Anmerkungen"
                />
              </td>
            </tr>
          </table>
        </div>
      </div>

      <button type="button" on:click={getTextSimilarity}>Abschliessen</button>
    {/if}

    <!-- ################################### ABSENDEN ################################### -->

    {#if overviewVisible}
      <div class="abschnitt">
        <h2>Übersicht</h2>

        <p>
          Die Ähnlichkeit bezieht sich auf die Corsine-Distance zwischen den von den Openai-API vorgeschlagenen Notizen
          und den selbst verfassten Notizen.
        </p>
        <div class="table-responsive">
          <table class="table">
            <tr>
              <th class="criteria">Bereich</th>
              <th class="assessment">Bewertung</th>
              <th class="notes">Anmerkungen</th>
              <th class="similarity">Ähnlichkeit</th>
              <th class="correction">Korrektur</th>
            </tr>
            <tr>
              <td> Aktiv teilnehmen </td>
              <td>
                {AktivTeilnehmen}
              </td>
              <td>
                {#if AktivTeilnehmenNotizen}
                  {AktivTeilnehmenNotizen}
                {/if}
              </td>
              <td>
                {#if similarity.AktivTeilnehmen}
                  {similarity.AktivTeilnehmen}
                {/if}
              </td>
              <td>
                <button type="button" on:click={() => scroll("aktivteilnehmen")}>Korrigieren</button>
              </td>
            </tr>
            <tr>
              <td> Leistung zeigen </td>
              <td>
                {LeistungZeigen}
              </td>
              <td>
                {#if LeistungZeigenNotizen}
                  {LeistungZeigenNotizen}
                {/if}
              </td>
              <td>
                {#if similarity.LeistungZeigen}
                  {similarity.LeistungZeigen}
                {/if}
              </td>
              <td>
                <button type="button" on:click={() => scroll("leistungzeigen")}>Korrigieren</button>
              </td>
            </tr>
            <tr>
              <td> Aufmerksam sein </td>
              <td>
                {AufmerksamSein}
              </td>
              <td>
                {#if AufmerksamSeinNotizen}
                  {AufmerksamSeinNotizen}
                {/if}
              </td>
              <td>
                {#if similarity.AufmerksamSein}
                  {similarity.AufmerksamSein}
                {/if}
              </td>
              <td>
                <button type="button" on:click={() => scroll("aufmerksamsein")}>Korrigieren</button>
              </td>
            </tr>
            <tr>
              <td> Schulinhalte merken </td>
              <td>
                {SchulinhalteMerken}
              </td>
              <td>
                {#if SchulinhalteMerkenNotizen}
                  {SchulinhalteMerkenNotizen}
                {/if}
              </td>
              <td>
                {#if similarity.SchulinhalteMerken}
                  {similarity.SchulinhalteMerken}
                {/if}
              </td>
              <td>
                <button type="button" on:click={() => scroll("schulinhaltemerken")}>Korrigieren</button>
              </td>
            </tr>
            <tr>
              <td> Schulinhalte abrufen </td>
              <td>
                {SchulinhalteAbrufen}
              </td>
              <td>
                {#if SchulinhalteAbrufenNotizen}
                  {SchulinhalteAbrufenNotizen}
                {/if}
              </td>
              <td>
                {#if similarity.SchulinhalteAbrufen}
                  {similarity.SchulinhalteAbrufen}
                {/if}
              </td>
              <td>
                <button type="button" on:click={() => scroll("schulinhalteabrufen")}>Korrigieren</button>
              </td>
            </tr>
          </table>
        </div>
      </div>
      <div class="abschnitt">
        <button type="button" on:click={cancel}>Abbrechen</button>
        <button type="submit">Bestätigen</button>
      </div>
    {/if}
    <div id="bestaetigen" />
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
    display: block;
    padding: 0px;
  }

  textarea {
    background-color: white;
  }

  .custom-control-input {
    vertical-align: middle;
    padding: 0px;
  }

  .custom-control-label {
    display: inline-block;
    padding: 0px;
  }

  .author {
    width: 200px;
  }

  .criteria {
    width: 100px;
  }

  .assessment {
    width: 100px;
  }

  .notes {
    width: auto;
  }

  .similarity {
    width: 80px;
  }

  .correction {
    width: 100px;
  }
</style>
