<script>
</script>

<div class="component">

    <h1>Welcome to my Report-Program</h1>
    <p>
        My program has the goal to simplify the writing of students-reports for teachers.
        The pupils are evaluated in different sections and for every section there are criteria that should be described.
        With the UI the teachers have the opportunity to evaluate students based on a evaluation-form.
        The evaluation-form is then anonyminized send to the backend and with the OpenAI-API, a text is generated.
        The text will be displayed in the frontend, so that the teachers can proof-read or change it.
        They can write prompts to specify which changes they would like to implement or they can do it manually.
        As soon as the text is accepted, it will be stored in a MongoDB.
    </p>
</div>

<style>
    p {
        margin-top:25px;
        font-size: large;
    }
</style>
