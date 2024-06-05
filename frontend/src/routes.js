import Home from "./pages/Home.svelte";
import BaseData from "./pages/BaseData.svelte";
import SemesterData from "./pages/SemesterData.svelte";
import Assessement from "./pages/Assessement.svelte";
import Combine from "./pages/Combine.svelte";
import CreateText from "./pages/CreateText.svelte";
import CombineDirectly from "./pages/CombineDirect.svelte"

export default {
    '/': Home,
    '/home': Home,
    '/base-data': BaseData,
    '/semester-data': SemesterData,
    '/assessment': Assessement,
    '/combine': Combine,
    '/combine/:semester_id/:student_id': CombineDirectly,
    '/create-text': CreateText,
}