<template>
  <div class="container">
    <div class="row h-100 w-auto justify-content-center text-center">
      <h1>Prenez part à la vie de votre ville</h1>
    </div>
    <div class="row h-100 w-auto justify-content-center text-center">
      <h3>
        Vous souhaitez participer à une consultation lancée par la municipalité
        ?
      </h3>
    </div>
    <div class="row h-100 w-auto justify-content-center text-center">
      <h3>
        Soumettre vos idées ou opinions à l'équipe municipale en vue d'un
        conseil de quartier ?
      </h3>
    </div>
    <div class="row h-100 w-auto justify-content-center text-center">
      <h3>
        Ou même créer une pétition et recueillir les avis et le soutien de vos
        concitoyens ?
      </h3>
    </div>
    <div class="row h-100 w-auto justify-content-center text-center">
      <nuxt-link to="signup/">Pas encore inscrit ? Cliquez ici.</nuxt-link>
    </div>
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
  padding-top: 5rem;
  padding-bottom: 0rem;
  color: rgb(0, 14, 116);
}
.container h1 {
  font-size: 4rem;
  margin-bottom: 5rem;
}
.container h3 {
  font-size: 2rem;
  margin: 1rem;
}
@media (max-width: 1200px) {
  .container h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
  }
  .container h3 {
    font-size: 1.5rem;
  }
  .container {
    padding-top: 2rem;
  }
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .container {
    padding-top: 3rem;
  }
}
</style>
