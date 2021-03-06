<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      {{ button_label }}
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de consultation"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      @show="resetModal"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Nom de la consultation"
          label-for="name-input"
          invalid-feedback="Vous devez donner un nom à la consultation"
          :state="nameState"
        >
          <b-form-input
            id="name-input"
            v-model="consultation.name"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Lieu concerné"
          label-for="place-input"
          invalid-feedback="Entrez un lieu concerné par la consultation"
          :state="placeState"
        >
          <b-form-input
            id="place-input"
            v-model="consultation.place"
            :state="placeState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Description de la consultation"
          label-for="description-input"
          invalid-feedback="Décrivez la consultation"
          :state="descriptionState"
        >
          <b-form-textarea
            id="description-input"
            v-model="consultation.description"
            :state="descriptionState"
            required
          ></b-form-textarea>
        </b-form-group>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="primary" @click="handleQuitConsultation()">
          Sauvegarder la consultation
        </b-button>
        <b-button size="lg" variant="primary" @click="handleOkConsultation()">
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
          v-show="this.question_type_name === 'QCM'"
        >
          <b-form-spinbutton
            id="answers_number"
            v-model="question.number_of_choices"
            min="2"
            max="10"
            @change="refreshChoices()"
          ></b-form-spinbutton>
        </b-form-group>
        <div v-show="this.question_type_name === 'QCM'">
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
          Sauvegarder la consultation
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
    <b-modal id="modal-validation" title="Consultation sauvegardée" hide-footer>
      <div class="d-block text-center">
        <h3>
          Votre projet de consultation est sauvegardé et accessible depuis votre
          profil, mes consultations, non publiées.
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
    dateState() {
      return this.end_day.length > 0 ? true : false;
    },
    nameState() {
      return this.consultation.name.length > 0 ? true : false;
    },
    placeState() {
      return this.consultation.place.length > 0 ? true : false;
    },
    descriptionState() {
      return this.consultation.description.length > 0 ? true : false;
    },
    questionNameState() {
      return this.question.wording.length > 0 ? true : false;
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
      return this.question_type_name.length > 0 ? true : false;
    }
  },
  data() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const minDate = new Date(today);
    minDate.setDate(minDate.getDate() + 30);
    return {
      button_label: this.button,
      publish: false,
      quit: false,
      consultation: {
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
    // We check the form with the infos of the Consultation is valid
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      return valid;
    },

    // We check the form with the question infos is valid
    checkForm2Validity() {
      // const valid = this.$refs.form.checkValidity();
      if (this.questionNameState && this.questionTypeState) {
        if (this.question_type_name === 'QCM') {
          if (this.answerState) {
            return true;
          } else {
            return false;
          }
        }
        return true;
      } else {
        return false;
      }
    },

    // We reset the data of the first form, the consultation basic infos
    resetModal() {
      this.consultation.name = '';
      this.consultation.place = '';
      this.consultation.description = '';
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

    // We send a POST request to the API with the data about the Consultation
    async getConsultationType() {
      const data = { name: 'Consultation' };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    },

    // We send a POST request to the API with the data about the Consultation
    async postConsultationData() {
      const data = {
        name: this.consultation.name,
        place: this.consultation.place,
        description: this.consultation.description,
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
    handleOkConsultation() {
      this.handleSubmit();
    },
    // Alternative to handleOkConsultation() in the case we want to quit (publish or only saving) and not add any question
    handleQuitConsultation() {
      this.quit = true;
      this.handleSubmit();
    },

    // Function called by the previous ones, taking care of the different steps
    async handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getConsultationType();
      await this.postConsultationData();
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
        console.log('PROBLEME FORM VALIDITY');
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
