<template>
  <!DOCTYPE html>
  <div class="container">
    <div class="item header">
      <h1 class="title">participons</h1>
    </div>
    <div class="item body">
      <h1>Encore</h1>
    </div>
    <div class="item footer">
      <h1>Toujours</h1>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  max-width: initial;
}
.title {
  font-family: 'Verdana, sans-serif';
  text-decoration-line: underline;
  text-indent: 0.7em;
}
@media (min-width: 1200px) {
  .header {
    flex-grow: 1;
    background-color: darkorchid;
    padding: 0px;
    margin-bottom: 0.5em;
    flex-basis: auto;
  }
  .body {
    flex-grow: 4;
    background-color: darkorchid;
    padding: 0px;
    margin-bottom: 0.5em;
    flex-basis: auto;
  }
  .footer {
    flex-grow: 1;
    background-color: darkorchid;
    padding: 0px;
    margin-bottom: 0.5em;
    flex-basis: auto;
  }
}
</style>
