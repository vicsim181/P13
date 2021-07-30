<template>
  <div>
    <CustomNavbar />
    <Signup />
    <CustomFooter />
  </div>
</template>

<script>
export default {
  auth: false,
  middleware: 'guest'
};
</script>

<style></style>
