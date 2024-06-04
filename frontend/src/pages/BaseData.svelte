<script>
import { push } from 'svelte-spa-router';

let firstname
let lastname
let gender=''
let birthday
let school_entry
let class_teacher
let special_education_teacher
let diagnose
let compensation

let message

async function createBase() {

    if (gender==='') {
        alert("Bitte ein Geschlecht angeben")
    }
    else {
        const base_data = {
            "firstname": firstname,
            "lastname": lastname,
            "gender": gender,
            "birthday": birthday,
            "school_entry": school_entry,
            "class_teacher": class_teacher,
            "spechial_education_teacher": special_education_teacher,
            "diagnose": diagnose,
            "compensation": compensation,
        };
        const response = await fetch('http://localhost:8000/create-base-data-entry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(base_data)
        });
        const responseData = await response.json();
        if (response.ok) {
            console.log('Success:', responseData);
            if (base_data["gender"]=="Männlich"){
                message="Schüler "
            }
            else {
                message = "Schülerin "
            }
            alert(message +base_data["firstname"] +" wurde angelegt.")
            push('/semester-data')
        } else {
            console.error('Failed to create entry:', responseData);
            alert("Irgendwas ist schief gelaufen.")
        }
    }
}


function cancel() {
    if (confirm('Möchten Sie das Formular leeren?')) {
      firstname=
      lastname=
      gender=
      birthday=
      school_entry=
      class_teacher=
      special_education_teacher=
      diagnose=
      compensation='';
    }
  }

</script>

<div class="component">
<h1>
    Stammdaten
</h1>
    <form on:submit|preventDefault={createBase}>
        <p>Geschlecht</p>

        <div class="custom-control custom-radio">
            <input type="radio" value="Weiblich" bind:group={gender} id="weiblich" class="custom-control-input">
            <label class="custom-control-label" for="weiblich">Weiblich</label>
            <input type="radio" value="Männlich" bind:group={gender} id="maennlich" class="custom-control-input">
            <label class="custom-control-label" for="maennlich">Männlich</label>
        </div>

        <table>
            <tr>
                <th>Vorname</th>
                <th>Nachname</th>
            </tr>
            <tr>
                <td>
                    <input type="text" class="form-control" bind:value={firstname} placeholder="Vorname" required>
                </td>
                <td>
                    <input type="text" class="form-control" bind:value={lastname} placeholder="Nachname" required>
                </td>
            </tr>
            <tr>
                <th>Geburtsdatum</th>
                <th>Eintritt</th>
            </tr>
            <tr>
                <td>
                    <input type="date" class="form-control" bind:value={birthday} placeholder="Geburtsdatum" required>
                </td>
                <td>
                    <input type="date" class="form-control" bind:value={school_entry} placeholder="Eintritt" required>
                </td>
            </tr>
            <tr>
                <th>Klassenlehrperson</th>
                <th>Heilpädagogin</th>
            </tr>
            <tr>
                <td>
                    <input type="text" class="form-control" bind:value={class_teacher} placeholder="Klassenlehrperson" required>
                </td>
                <td>
                    <input type="text" class="form-control" bind:value={special_education_teacher} placeholder="Heilpaedagogin" required>
                </td>
            </tr>
            <tr>
                <th>Diagnose</th>
                <th>Nachteilsausgleich</th>
            </tr>
            <tr>
                <td>
                    <input type="text" class="form-control" bind:value={diagnose} placeholder="Diagnose">
                </td>
                <td>
                    <input type="text" class="form-control" bind:value={compensation} placeholder="Nachteilsausgleich">
                </td>
            </tr>
        </table>

        <button type="submit">Bestätigen</button>
        <button type="button" on:click={cancel}>Abbrechen</button>
    </form> 
</div>

<style>

</style>
