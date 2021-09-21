<template>
  <div class="d-flex flex-column text-dark" style="min-height: 100vh">
    <CustomNavbar></CustomNavbar>
    <b-container fluid class="bg-light py-4" style="flex: 1">
      <b-container class="px-0">
        <Nuxt />
      </b-container>
    </b-container>
    <CustomFooter></CustomFooter>
  </div>
</template>
