<script>
	import Router from "svelte-spa-router";
	import routes from "./routes";
</script>

<div id="app">
        <!--Navigation-Bar-->
        <nav class="navbar navbar-expand-lg bg-body-terinary">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" href="#/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#/base-data">Stammdaten</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#/semester-data">Semester-Daten</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#/assessment">Beurteilen</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#/combine">Zusammenführen</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#/create-text">Finaler Text</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        
	<div class="container">
        <div class="component">
		    <Router {routes} />
        </div>
	</div>
</div>

<style>

.nav-link {
    font-size:x-large;
    color: #1b5068;
    margin-left: 30px;
    margin-right: 30px;
  }

  a:hover {
    color: rgb(6, 158, 192);
  }

  .navbar {
    background-color: rgba(253, 248, 153, 0.8);
    height: 90px;
    width:auto;
  }

  .navbar-collapse {
    background-color: rgba(255, 255, 255, 0.95); /* Light background with slight transparency */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    border-radius: 0 0 5px 5px; /* Rounded corners at the bottom */
  }

    /* Additional styling for the toggler icon */
  .navbar-toggler {
    border-color: rgba(0, 0, 0, 0.1); /* Optional: adds a border to the toggler icon */
  }

</style>