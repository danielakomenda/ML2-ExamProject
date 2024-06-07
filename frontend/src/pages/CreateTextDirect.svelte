<script>
    import { push } from "svelte-spa-router";
  
    export let params = {};

    $: {
    semester_id = params.semester_id;
    student_id = params.student_id;
    getSemester();
    getPupil();
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
  

    
    //////////////////////// GET SPECIFIC STUDENT /////////////////////////
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
  
  
    //////////////////////// GET SPECIFIC SEMESTER /////////////////////////
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
        console.error("Failed to find student:", responseData);
      }
    }
  

    //////////////////////// GO BACK TO COMBINE, TO CORRECT THE FINAL ASSESSMENT /////////////////////////
    function correctFinalAssessment() {
      push("/combine/" + semester_id + "/" + student_id);
    }
  

    //////////////////////// GET TEXT FROM OPENAI /////////////////////////
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
        console.log(final_assessment.allgemeines_lernen);
        textVisible = true;
      } else {
        console.error("Failed to find student:", responseData);
      }
    }
  
    //////////////////////// GET CORRECTED TEXT FROM OPENAI /////////////////////////
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
        console.log(chain);
        secondTextVisible = true;
      } else {
        console.error("Failed to get text:", responseData);
      }
    }
  
    //////////////////////// GET SIMILARITY OF THE RECOMMENDED AND MANUALLY CREATED TEXT /////////////////////////
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
        console.log(similarity);
      } else {
        console.error("Failed to create entry:", responseData);
      }
    }
  
    //////////////////////// STORE TEXT TO DATABASE /////////////////////////
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
          alert("Die Cosine-Similarity zwischen Deinem Text und dem Text von OpenAI beträgt " + similarity + ".\nDer Text wurde in der Datenbank gespeichert.");
        }
        if (confirm("Möchtest Du einen weiteren Text generieren?")) {
          cancel();
          push("/create-text");
        }
        cancel();
        alert("Du kannst eine weitere Beurteilung machen.")
        push("/assessment");
      } else {
        console.error("Failed to create entry:", responseData);
      }
    }
  
    function changePromptVisibility() {
      promptVisible = true;
    }
  
    function changeManualTextVisible() {
      manualTextVisible = true;
    }
  
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
                  <input type="text" bind:value={prompt} placeholder="Was möchtest du ändern?" />
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
                  <input type="text" rows="5" bind:value={manualText} placeholder="Was möchtest du ändern?" />
                  <button
                    type="button"
                    class="mybutton"
                    on:click={getTextSimilarity}
                    on:click={createFinalText(manualText)}>Send</button
                  >
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
  
    input {
      border-width: 0px;
      width: 100%;
    }
  </style>
  