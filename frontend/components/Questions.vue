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
      @hidden="resetModal_questions"
    >
      <form ref="form" @submit.stop.prevent="handlePublishAnswers">
        <b-form-group
          invalid-feedback="Renseignez toutes vos réponses"
          v-for="number in number_of_questions"
          :key="number"
          :state="answerState"
        >
          <b-card-title>{{ questions[number - 1][0].wording }}</b-card-title>
          <div v-if="questions[number - 1][0].question_type === free_type_id">
            <b-form-textarea
              id="question_answer"
              v-model="user_answers[questions[number - 1][0].id_question]"
              :state="answerState"
            ></b-form-textarea>
          </div>
          <div v-else>
            <b-form-select
              v-model="user_answers[questions[number - 1][0].id_question]"
              :options="mcq_answers[questions[number - 1][0].id_question]"
              :state="answerState"
            >
            </b-form-select>
          </div>
        </b-form-group>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="success" @click="handlePublishAnswers()">
          Valider mes réponses
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- SECOND MODAL FOR VALIDATION -->
    <b-modal
      id="modal-validation"
      title="Vous avez participé au sondage"
      hide-footer
    >
      <div class="d-block text-center">
        <h3>
          Votre participation au sondage a bien été enregistrée.
        </h3>
      </div>
      <b-button
        class="mt-3 button"
        block
        @click="
          answersSaved();
          $bvModal.hide('modal-validation');
        "
        >Ok</b-button
      >
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['project', 'user', 'questions', 'mcqanswers'],
  computed: {
    answerState() {
      if (Object.keys(this.user_answers).length !== this.number_of_questions) {
        return false;
      } else {
        for (const answer in this.user_answers) {
          if (this.user_answers[answer].length === 0) {
            return false;
          } else if (this.user_answers[answer] === ' ') {
            return false;
          }
        }
        return true;
      }
    }
  },
  data() {
    return {
      number_of_questions: Object.keys(this.questions).length,
      questions_data: this.questions,
      mcq_answers: this.mcqanswers,
      user_answers: {},
      qcm_type_id: '',
      free_type_id: '',
      loaded: false
    };
  },

  // Function getting the ids of the two different kinds of question
  async fetch() {
    let data = { name: 'QCM' };
    let response = await this.$axios.get('question_type', { params: data });
    let type_id = response.data['id_question_type'];
    this.qcm_type_id = type_id;
    data = { name: 'Réponse libre' };
    response = await this.$axios.get('question_type', { params: data });
    type_id = response.data['id_question_type'];
    this.free_type_id = type_id;
    this.loaded = true;
  },

  methods: {
    // Emptying the user's answers
    resetModal_questions() {
      this.user_answers = {};
    },

    // We check the form with the infos of the Consultation is valid
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      if (this.answerState) {
        return valid;
      } else {
        return false;
      }
    },

    // Function sending the post request to save the user's answers
    async postUserAnswer() {
      for (const [id, answer] of Object.entries(this.user_answers)) {
        const data = {
          owner: this.user,
          question: id,
          answer: answer
        };
        try {
          const response = await this.$axios.post('user_answer/', data);
          console.log(response.data);
        } catch (error) {
          console.log(error.response);
          const keys = Object.keys(error.response.data);
          const errorMessage = error.response.data[keys[0]];
          window.alert(errorMessage);
          return false;
        }
      }
      return true;
    },

    // Function handling the validation of the answers
    async handlePublishAnswers() {
      if (!this.checkFormValidity()) {
        return;
      } else {
        const response = await this.postUserAnswer();
        console.log('response ', response);
        this.$nextTick(() => {
          if (response) {
            this.$bvModal.hide('modal-questions');
            this.$bvModal.show('modal-validation');
          } else {
            window.alert(
              'Erreur lors de la sauvegarde de vos réponses. \n Veuillez réessayer.'
            );
          }
        });
      }
    },

    // Function called when Ok is clicked on the confirmation the answers are saved
    answersSaved() {
      this.$emit('hasparticipated');
    }
  }
};
</script>

<style></style>
