<script>
  import { push } from "svelte-spa-router";

  $: {
    getAllPupils();
  }

  let students = [];
  let semesters = [];

  let semester = {};
  let student = {};

  let final_assessment = {};
  let chain = [];
  let student_id;
  let semester_id;
  let firstText = "";
  let secondText = "";
  let manualText = "";
  let prompt;
  let similarity;

  let visible = false;
  let textVisible = false;
  let promptVisible = false;
  let secondTextVisible = false;
  let manualTextVisible = false;

  ///////////////////////////// GET ALL STUDENTS //////////////////////////////
  async function getAllPupils() {
    const response = await fetch("http://localhost:8000/get-all-pupils-data/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      students = responseData.data;
    } else {
      console.error("Failed to find students:", responseData);
    }
  }

  /////////////////////////// GET SPECIFIC STUDENT ////////////////////////////
  async function getPupil() {
    const response = await fetch("http://localhost:8000/get-pupil-data/" + student_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      student = responseData.data;
    } else {
      console.error("Failed to find student:", responseData);
    }
  }

  ///////// GET ALL SEMESTERS OF THE STUDENT WITH A FINAL ASSESSMENT //////////
  async function getSemestersWithFinalAssessment() {
    const response = await fetch("http://localhost:8000/semesters-with-final-assessment/" + student_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      semesters = responseData.data;
    } else {
      console.error("Failed to find semesters:", responseData);
    }
  }

  /////////////////////////// GET SPECIFIC SEMESTER ////////////////////////////
  async function getSemester() {
    const response = await fetch("http://localhost:8000/get-semester-data/" + semester_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      semester = responseData.data;
      final_assessment = semester.final_assessment;
      visible = true;
      if (semester.final_text) {
        alert(
          "Für dieses Semester gibt es bereits eine Beurteilung für den Schüler.\nMöchtest Du eine neue Beurteilung schreiben?"
        );
      }
    } else {
      console.error("Failed to find semester:", responseData);
    }
  }

  /////////////////////////// GET TEXT FROM OPENAI ////////////////////////////
  async function getFirstText() {
    const data = {
      semester: semester,
      student: student,
    };
    const response = await fetch("http://localhost:8000/generate-first-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      firstText = responseData.answer;
      chain = responseData.chain;
      textVisible = true;
    } else {
      console.error("Failed to get text:", responseData);
    }
  }

  ////////////////////// GET CORRECTED TEXT FROM OPENAI ///////////////////////
  async function getSecondText() {
    const data = {
      semester: semester,
      student: student,
      chain: chain,
      prompt: prompt,
    };
    const response = await fetch("http://localhost:8000/generate-second-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      secondText = responseData.answer;
      chain = responseData.chain;
      secondTextVisible = true;
    } else {
      console.error("Failed to get text:", responseData);
    }
  }

  //////// GET SIMILARITY OF THE RECOMMENDED AND MANUALLY CREATED TEXT /////////
  async function getTextSimilarity() {
    const data = {
      recommended: firstText,
      manually: manualText,
    };
    const response = await fetch("http://localhost:8000/get-text-similarity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      similarity = responseData.similarity;
    } else {
      console.error("Failed to get similarity:", responseData);
    }
  }

  ////////////////////////// STORE TEXT TO DATABASE ///////////////////////////
  async function createFinalText(text) {
    const finalText = {
      allgemeines_lernen: text,
    };
    const response = await fetch("http://localhost:8000/create-final-text-data/" + semester_id, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(finalText),
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
      if (manualText) {
        await getTextSimilarity();
        storeSimilarity();
        alert(
          "Die Cosine-Similarity zwischen Deinem Text und dem Text von OpenAI beträgt " +
            similarity +
            ".\nDer Text wurde in der Datenbank gespeichert."
        );
      }
      if (confirm("Möchtest Du einen weiteren Text generieren?")) {
        cancel();
        push("/create-text");
      } else {
        cancel();
        alert("Du kannst eine weitere Beurteilung machen.");
        push("/assessment");
      }
    } else {
      console.error("Failed to create entry:", responseData);
    }
  }

  ///////// STORE OPENAI-TEXT, MANUAL TEXT AND SIMILARITY TO DATABASE //////////
  async function storeSimilarity() {
    const data = {
      firstText: firstText,
      secondText: secondText,
      manualText: manualText,
      similarity: similarity,
    };
    const response = await fetch("http://localhost:8000/store-similarity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseData = await response.json();
    if (response.ok) {
      console.log("Success:", responseData);
    } else {
      console.error("Failed to create entry:", responseData);
    }
  }

  ///////////////////////////// CHANGE VISIBILITY //////////////////////////////
  function changePromptVisibility() {
    promptVisible = true;
  }

  function changeManualTextVisible() {
    manualTextVisible = true;
  }

  //////////// GO BACK TO COMBINE, TO CORRECT THE FINAL ASSESSMENT /////////////
  function correctFinalAssessment() {
    push("/combine/" + semester_id + "/" + student_id);
  }

  //////////////////////////// DELETE ALL ENTRIES /////////////////////////////
  function cancel() {
    semester = {};
    student = {};
    final_assessment = {};
    chain = [];
    student_id;
    semester_id;
    firstText = "";
    secondText = "";
    manualText = "";
    prompt;
    similarity;
    visible = false;
    textVisible = false;
    promptVisible = false;
    secondTextVisible = false;
    manualTextVisible = false;
  }
</script>

<div class="component">
  <h1>Text generieren</h1>

  <select
    class="form-control"
    bind:value={student_id}
    on:change={getSemestersWithFinalAssessment}
    on:change={getPupil}
    id="student_id"
    required
  >
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
      <button type="button" on:click={correctFinalAssessment}>Korrigieren</button>
      <button type="button" on:click={getFirstText}>Text generieren</button>
    </div>
  {/if}

  {#if textVisible}
    <div class="abschnitt">
      <div class="table-responsive">
        <table class="table">
          <tr class="styleless">
            <th class="generatedTextHeader styleless" />
            <th class="promptHeader styleless" />
          </tr>
          <tr class="styleless">
            <td class="generatedText styleless">
              {firstText}
            </td>
            <td class="styleless">
              <button type="button" class="mybutton" on:click={createFinalText(firstText)}>Beenden</button>
              <button type="button" class="mybutton" on:click={changePromptVisibility}>Korrigieren</button>
            </td>
          </tr>
          {#if promptVisible}
            <tr class="styleless">
              <td class="styleless" />
              <td class="styleless prompt">
                <textarea class="textarea styleless prompt" rows="3" bind:value={prompt} placeholder="Was möchtest du ändern?" />
                <button type="button" class="mybutton" on:click={getSecondText}>Send</button>
              </td>
            </tr>
          {/if}
          {#if secondTextVisible}
            <tr class="styleless">
              <th class="generatedTextHeader styleless" />
              <th class="promptHeader styleless" />
            </tr>
            <tr class="styleless">
              <td class="generatedText styleless">
                {secondText}
              </td>
              <td class="styleless">
                <button type="button" class="mybutton" on:click={createFinalText(secondText)}>Beenden</button>
                <button type="button" class="mybutton" on:click={changeManualTextVisible}>Eigener Text</button>
              </td>
            </tr>
          {/if}
          {#if manualTextVisible}
            <tr class="styleless">
              <td class="styleless" />
              <td class="styleless prompt">
                <textarea class="textarea styleless prompt" rows="5" bind:value={manualText} placeholder="Schreibe deinen Text." />
                <button type="button" class="mybutton" on:click={createFinalText(manualText)}>Send</button>
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
    padding: 2px;
    border: 1px solid gray;
    width: 100px;
  }

  .styleless {
    border-width: 0;
  }

  .generatedText,
  .prompt {
    background-color: white;
    border: 2px solid gray;
    width: max-content;
  }

  .generatedTextHeader,
  .promptHeader {
    width: 45%;
    margin: 0px;
    padding: 0px;
    border-width: 0px;
  }

  .textarea {
    border-width: 0px;
    width: 100%;
  }
</style>
