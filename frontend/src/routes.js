import Home from "./pages/Home.svelte";
import BaseData from "./pages/BaseData.svelte";
import SemesterData from "./pages/SemesterData.svelte";
import Assessement from "./pages/Assessement.svelte";
import Combine from "./pages/Combine.svelte";
import CreateText from "./pages/CreateText.svelte";

export default {
    '/': Home,
    '/home': Home,
    '/base-data': BaseData,
    '/semester-data': SemesterData,
    '/assessment': Assessement,
    '/combine': Combine,
    '/create-text': CreateText,
}