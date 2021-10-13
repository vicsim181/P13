<template>
  <div>
    <h1 v-if="error.statusCode === 404">
      Page Not Found ({{ error.statusCode }})
    </h1>
    <h1 v-else-if="error.statusCode === 500">
      An error occured on the server ({{ error.statusCode }})
    </h1>
    <h1 v-else>An error occured ({{ error.statusCode }})</h1>
    <div>{{ error.message }}</div>
  </div>
</template>

<script>
export default {
  props: ["error"],
  layout: "headless"
};
</script>
