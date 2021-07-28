<template>
  <footer class="py-3 bg-white fixed-bottom">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-3">
          <a href="#"><b>Mentions Légales</b></a>
        </div>
        <div class="col-md-3">
          <a href="#"><b>Gestion des cookies</b></a>
        </div>
        <div class="col-md-3">
          <a href="#"><b>Contact</b></a>
        </div>
        <div class="col-md-3"><p>Copyright@ VictorSIMON 2021</p></div>
      </div>
    </div>
  </footer>
</template>

<style>
footer div div {
  align-content: space-around;
  align-items: baseline;
  text-align: center;
}
footer div div a {
  font-size: 2rem;
  color: rgb(0, 14, 116);
}
footer div div p {
  font-size: 1.5rem;
  color: rgb(0, 14, 116);
}
@media (max-width: 1024px) {
  footer div div p {
    font-size: 1rem;
  }
  footer div div a {
    font-size: 1.5rem;
  }
}
</style>
