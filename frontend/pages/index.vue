<template>
  <!DOCTYPE html>
  <div class="main">
    <CustomNavbar />
    <body>
      <div class="container">
        <div class="row h-100 w-auto justify-content-center text-center">
          <h1>Prenez part à la vie de votre ville</h1>
        </div>
        <div class="row h-100 w-auto justify-content-center text-center">
          <h3>
            Vous souhaitez apporter votre avis sur un projet lancé par la
            municipalité ?
          </h3>
        </div>
        <div class="row h-100 w-auto justify-content-center text-center">
          <h3>
            Interpeller l'équipe municipale en vue d'un conseil de quartier ?
          </h3>
        </div>
        <div class="row h-100 w-auto justify-content-center text-center">
          <h3>
            Ou même créer une pétition et recueillir les avis de vos concitoyens
            ?
          </h3>
        </div>
      </div>
    </body>
    <CustomFooter />
  </div>
</template>

<script>
export default {
  auth: false
};
</script>

<style>
body {
  min-width: 100%;
  padding-top: 6rem;
  padding-bottom: 7rem;
  color: rgb(0, 14, 116);
}
body h1 {
  font-size: 4rem;
  margin-bottom: 5rem;
}
body h3 {
  font-size: 2rem;
  margin: 1rem;
}
@media (max-width: 1024px) {
  body h1 {
    font-size: 2.5rem;
    margin-bottom: 3rem;
  }
  body {
    padding-top: 5rem;
  }
}
@media (min-width: 1200px) and (max-width: 1434px) {
  body {
    padding-top: 8rem;
  }
}
</style>
