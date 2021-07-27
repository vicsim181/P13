<template>
  <!DOCTYPE html>
  <div>
    <header>
      <b-navbar fixed="top" toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand href="#" class="title">participons</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav class="navbar_elements">
            <b-nav-item href="#" class="item">CONSULTATIONS</b-nav-item>
            <b-nav-item href="#" class="item">PETITIONS</b-nav-item>
            <b-nav-item href="#" class="item">CONSEIL DE QUARTIER</b-nav-item>
          </b-navbar-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template #button-content>
                <em>User</em>
              </template>
              <b-dropdown-item href="#">Profile</b-dropdown-item>
              <b-dropdown-item href="#">Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </header>
    <div>
      <h1>Encore</h1>
    </div>
    <div class="bas">
      <h1>Toujours</h1>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
@media (min-width: 1400px) {
  .navbar {
    background-color: darkgoldenrod;
  }
  .title {
    font-family: 'Verdana, sans-serif';
    font-weight: 700;
    font-size: 4.5em;
    text-decoration-line: underline;
  }
  .navbar_elements {
    align-items: center;
    margin-left: 2rem;
  }
  .item {
    margin-left: 5rem;
    margin-right: 5rem;
    text-align: center;
    font-size: 1.4rem;
  }
  .container {
    margin: 0rem;
  }
  .bas {
    margin-top: 60rem;
  }
}
</style>
