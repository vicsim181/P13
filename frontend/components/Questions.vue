<template>
  <div>
    <b-button v-b-modal.modal-questions variant="dark">
      Participer au sondage
    </b-button>

    <b-modal
      id="modal-questions"
      size="lg"
      ref="modal"
      :title="project.name"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          :label="question.wording"
          v-for="question in questions"
          v-bind:key="question.id_question"
        >
          <b-form-input></b-form-input>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['project', 'user', 'questions']
};
</script>

<style></style>
