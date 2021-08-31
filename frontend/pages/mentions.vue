<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="row h-100 w-auto justify-content-center text-center">
        <h1>Mentions légales</h1>
      </div>
      <br />
      <div class="row h-100 w-auto justify-content-center text-justify">
        <p>
          Les images utilisées proviennet de différentes sources.
        </p>
      </div>
      <br />
      <div class="row h-100 w-auto justify-content-center text-justify">
        <h5>
          Les technologies utilisées pour réaliser ce site sont les suivantes :
        </h5>
      </div>
      <div class="row h-100 w-auto justify-content-center text-justify">
        <ul>
          <li>Django REACT</li>
          <li>NuxtJS</li>
          <li>Python, JS, HTML5/CSS3</li>
        </ul>
      </div>
      <div class="row h-100 w-auto justify-content-center text-justify">
        <p>
          Ce projet a été créé dans le cadre de la formation "Développeur
          d'application Python" dispensée par
          <a href="https://openclassrooms.com/fr/">OpenClassrooms</a>. Il
          constitue le 13ème et dernier projet de la formation, avec pour
          objectif de mettre en pratique le plus de compétences et savoirs
          acquis durant les précédents projets.
        </p>
      </div>
      <div class="row h-100 w-auto justify-content-center text-justify">
        <p>
          Ce prototype de site s'inspire de modèles existants permettant de
          faciliter la participation citoyenne dans les collectivités, notamment
          les villes. Il permet de publier en ligne et rendre accessible à tous
          les consultations publiques lancées par l'administration, les conseils
          de quartier à venir ou encore les pétitions lancées par les citoyens.
          De cette façon la participation citoyenne peut s'exercer aussi bien
          via les réunions physiques organisées mais également via une
          plateforme où toutes les initiatives peuvent être centralisées.
        </p>
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
export default {
  auth: false
};
</script>

<style>
.container {
  min-width: 100%;
  padding-top: 15rem;
  padding-bottom: 11rem;
  color: rgb(0, 14, 116);
}
.container h1 {
  font-size: 3rem;
  margin-bottom: 2rem;
}
.container p {
  padding-top: 1rem;
  padding-left: 15rem;
  padding-right: 15rem;
}
@media (max-width: 1200px) {
  .container h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  .container h3 {
    font-size: 1.5rem;
  }
  .container {
    padding-top: 10rem;
  }
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .container {
    padding-top: 11rem;
  }
}
</style>
