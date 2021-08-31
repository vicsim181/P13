<template>
  <div class="py-3 bg-white fixed-bottom">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-9 text-left">
          <a href="mentions"><b>Mentions Légales</b></a>
        </div>
        <div class="col-md-3 text-right"><p>@ Copyright - Victor SIMON</p></div>
      </div>
    </div>
  </div>
</template>

<style>
.container-fluid div div {
  padding-left: 3rem;
  padding-right: 3rem;
  align-items: baseline;
  text-align: center;
}
.container-fluid div div a {
  font-size: 2rem;
  color: rgb(0, 14, 116);
}
.container-fluid div div p {
  font-size: 1.5rem;
  color: rgb(0, 14, 116);
}
@media (max-width: 1024px) {
  .container-fluid div div p {
    font-size: 1rem;
  }
  .container-fluid div div a {
    font-size: 1.15rem;
  }
}
</style>
