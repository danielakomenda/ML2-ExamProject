<div class="component">

    <h1>Welcome to My Report Program</h1>
    <p>
        This program aims to simplify the process of writing student reports for teachers.
        Students are evaluated based on five criteria, allowing teachers to assess how well each student performs.
        Teachers can add notes about each criterion, and all assessments are stored in a database.
    </p>
    <p>
        The teacher primarily responsible for a student's report can view assessments from other teachers.
        These assessments are then combined into a final assessment. Additional notes from all teachers are anonymized and consolidated into a single text note using the OpenAI API.
    </p>
    <p>
        The final assessment is anonymized and sent to the OpenAI API, where a text is generated. This text is displayed in the frontend, allowing teachers to proofread and modify it if necessary.
        They can specify changes via a prompt or rewrite the text themselves. The similarity between the OpenAI-generated text and the teacher's manually written text is evaluated.
        Once the final text is approved, it is stored in a MongoDB database.
    </p>
    
    <h3>Beurteilen</h3>
    <p>
        Select a student and a semester to create assessments based on different criteria. You may also add notes to each assessment. Multiple assessments can be created per student and semester, allowing various teachers to evaluate the student individually. All assessments are stored in a separate collection in the database.
    </p>

    <h3>Zusammenführen</h3>
    <p>
        This section allows you to view all assessments made for a specific student and semester. You can combine these into a final assessment. While a suggestion for the notes is provided by combining input from various teachers, you have the freedom to write an alternative note. If you choose to write your own, the cosine similarity between the recommended note and yours is calculated. The final assessment is then stored with the semester data in the database.
    </p>

    <h3>Finaler Text</h3>
    <p>
        After choosing a student and viewing semesters with final assessments, you can review the final assessments and make corrections if necessary. Texts are generated using the OpenAI API, which uses prompt engineering with a few-shot dataset. All entries are anonymized before being sent to OpenAI, ensuring that no personal data is transmitted. If you are unsatisfied with the generated text, you can provide a specific prompt to guide the modifications or write the text yourself. Once finalized, the text, along with the semester data, is stored in the database.
    </p>

</div>

<style>
    p {
        margin-top: 25px;
        font-size: large;
    }
</style>
