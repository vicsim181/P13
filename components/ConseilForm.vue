<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      {{ button_label }}
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de conseil de quartier"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Nom du conseil"
          label-for="name-input"
          invalid-feedback="Vous devez donner un nom au conseil"
          :state="nameState"
        >
          <b-form-input
            id="name-input"
            v-model="conseil.name"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Quartier concerné"
          label-for="place-input"
          invalid-feedback="Entrez un quartier concerné par le conseil"
          :state="placeState"
        >
          <b-form-input
            id="place-input"
            v-model="conseil.place"
            :state="placeState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Description du conseil"
          label-for="description-input"
          invalid-feedback="Décrivez le conseil"
          :state="descriptionState"
        >
          <b-form-textarea
            id="description-input"
            v-model="conseil.description"
            :state="descriptionState"
            required
          ></b-form-textarea>
        </b-form-group>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="primary" @click="handleQuitConseil()">
          Sauvegarder le conseil
        </b-button>
        <b-button size="lg" variant="primary" @click="handleOkConseil()">
          Ajouter une question
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- SECOND MODAL FOR THE QUESTIONS -->
    <b-modal
      id="modal-prevent-closing-2"
      size="lg"
      ref="modal"
      title="Création d'une question"
      no-close-on-backdrop
      @show="resetModal_2"
      @hidden="resetModal_2"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_2">
        <b-form-group
          label="Titre de la question"
          label-for="question_wording-input"
          invalid-feedback="Vous devez donner un titre à la question"
          :state="questionNameState"
        >
          <b-form-input
            id="question_wording-input"
            v-model="question.wording"
            :state="questionNameState"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="question_type"
          label="Type de question"
          v-slot="{ ariaDescribedby }"
          required
          :state="questionTypeState"
          invalid-feedback="Vous devez choisir un type de question"
        >
          <b-form-radio
            v-model="question_type_name"
            :aria-describedby="ariaDescribedby"
            name="some-radios"
            :state="questionTypeState"
            value="Réponse libre"
            >Question à réponse libre</b-form-radio
          >
          <b-form-radio
            v-model="question_type_name"
            :aria-describedby="ariaDescribedby"
            name="some-radios"
            :state="questionTypeState"
            value="QCM"
            >Question à choix multiples</b-form-radio
          >
        </b-form-group>
        <b-form-group
          label="Choisissez le nombre de réponses possibles (min = 2, max = 10)"
          v-if="this.question_type_name === 'QCM'"
        >
          <b-form-spinbutton
            id="answers_number"
            v-model="question.number_of_choices"
            min="2"
            max="10"
            @change="refreshChoices()"
          ></b-form-spinbutton>
        </b-form-group>
        <div v-if="this.question_type_name === 'QCM'">
          <b-form-group
            label="Choix de réponse"
            invalid-feedback="Renseignez toutes les réponses possibles"
            v-for="number in question.number_of_choices"
            :key="number"
            :state="answerState"
          >
            <b-form-input
              id="question_choice-input"
              v-model="question.choices[number]"
              :state="answerState"
              required
            ></b-form-input>
          </b-form-group>
        </div>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="primary" @click="handleQuitQuestion()">
          Sauvegarder le conseil
        </b-button>
        <b-button size="lg" variant="primary" @click="handleOkQuestion()">
          Ajouter une question
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- THIRD MODAL FOR CONFIRMATION -->
    <b-modal id="modal-validation" title="Conseil sauvegardé" hide-footer>
      <div class="d-block text-center">
        <h3>
          Votre projet est sauvegardé et accessible depuis votre profil, mes
          conseils, non publiés.
        </h3>
      </div>
      <b-button
        class="mt-3 button"
        block
        @click="$bvModal.hide('modal-validation')"
        >Ok</b-button
      >
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['button'],
  computed: {
    nameState() {
      return this.conseil.name.length > 0;
    },
    placeState() {
      return this.conseil.place.length > 0;
    },
    descriptionState() {
      return this.conseil.description.length > 0;
    },
    questionNameState() {
      return this.question.wording.length > 0;
    },
    answerState() {
      if (
        this.question.choices.length - 1 !==
        this.question.number_of_choices
      ) {
        return false;
      } else {
        for (const choice in this.question.choices) {
          if (this.question.choices[choice].length === 0) {
            return false;
          } else if (this.question.choices[choice] === ' ') {
            return false;
          }
        }
        return true;
      }
    },
    questionTypeState() {
      return this.question_type_name.length > 0;
    }
  },
  data() {
    return {
      button_label: this.button,
      publish: false,
      quit: false,
      conseil: {
        name: '',
        place: '',
        description: '',
        project_type: ''
      },
      question: {
        type: '',
        wording: '',
        number_of_choices: 2,
        choices: []
      },
      id_project: '',
      id_owner: '',
      question_type_name: ''
    };
  },
  methods: {
    // We check the form with the infos of the Conseil is valid
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      return valid;
    },

    // We check the form with the question infos is valid
    checkForm2Validity() {
      const valid = this.$refs.form.checkValidity();
      if (this.questionNameState && this.questionTypeState) {
        if (this.question_type_name === 'QCM') {
          if (this.answerState) {
            return valid;
          } else {
            return false;
          }
        }
        return valid;
      } else {
        return false;
      }
    },

    // We reset the data of the first form, the conseil basic infos
    resetModal() {
      this.conseil.name = '';
      this.conseil.place = '';
      this.conseil.description = '';
      this.quit = false;
    },

    // We reset the data of the second form, question infos
    resetModal_2() {
      this.question.wording = '';
      this.question.type = '';
      this.question.number_of_choices = 2;
      this.quit = false;
    },

    // Function refreshing the question.choices list depending on the number of fields displayed in the question configuration modal
    refreshChoices() {
      const numb_choices = this.question.number_of_choices;
      const choices_length = this.question.choices.length;
      if (choices_length - 1 > numb_choices) {
        const diff = choices_length - 1 - numb_choices;
        for (let j = diff; j > 0; j--) {
          this.question.choices.pop();
        }
      }
    },

    // We send a GET request to the API to get the id of the project type Conseil
    async getConseilType() {
      const data = { name: 'Conseil de quartier' };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    },

    // We send a POST request to the API with the data about the Conseil
    async postConseilData() {
      const data = {
        name: this.conseil.name,
        place: this.conseil.place,
        description: this.conseil.description,
        project_type: this.projectType
      };
      try {
        const response = await this.$axios.post('project/', data);
        console.log(response.data);
        this.id_project = response.data['id_project'];
        this.id_owner = response.data['owner'];
      } catch (error) {
        console.log(error.response);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
    },

    // We send a POST request to the API to post a question
    async postQuestionData() {
      const question_data = {
        wording: this.question.wording,
        question_type: this.question.type,
        project: this.id_project
      };
      try {
        const response_1 = await this.$axios.post('question/', question_data);
        const question_id = response_1.data['id_question'];
        if (this.question_type_name === 'QCM') {
          for (const choice in this.question.choices) {
            const answer_data = {
              wording: this.question.choices[choice],
              question: question_id
            };
            await this.$axios.post('mcq_answer/', answer_data);
          }
        }
        this.question.choices = [];
      } catch (error) {
        console.log(error.response);
        const errorMessage = error.response.data;
        window.alert(errorMessage);
        this.question.choices = [];
      }
    },

    // We send a GET request to the API to get the id of the question type depending on the radio buttons choice
    async getQuestionType() {
      const data = { name: this.question_type_name };
      const response = await this.$axios.get('question_type', { params: data });
      const question_type_id = response.data['id_question_type'];
      return question_type_id;
    },

    // FUNCTIONS CALLED BY THE BUTTONS

    // We call this function when clicking on one of the 3 buttons (Save and quit, Publish and quit, add a question)
    handleOkConseil() {
      this.handleSubmit();
    },
    // Alternative to handleOkConseil() in the case we want to quit (publish or only saving) and not add any question
    handleQuitConseil() {
      this.quit = true;
      this.handleSubmit();
    },

    // Function called by the previous ones, taking care of the different steps
    async handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getConseilType();
      await this.postConseilData();
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
        if (this.quit === false) {
          this.$bvModal.show('modal-prevent-closing-2');
        } else {
          this.$bvModal.show('modal-validation');
        }
      });
    },

    // We call this function when validating a question and adding a new one
    handleOkQuestion() {
      this.handleSubmit_2();
    },

    // Alternative to handleOkQuestion() in case we want to quit (publish or just save) without adding new question
    handleQuitQuestion() {
      this.quit = true;
      this.handleSubmit_2();
    },

    // Function called by the previous ones, taking care of the different steps
    async handleSubmit_2() {
      if (!this.checkForm2Validity()) {
        return;
      }
      this.question.type = await this.getQuestionType();
      this.postQuestionData();
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-2');
        if (this.quit === false) {
          this.$bvModal.show('modal-prevent-closing-2');
        } else {
          this.$bvModal.show('modal-validation');
        }
      });
    }
  }
};
</script>
