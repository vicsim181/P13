<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      Créer un conseil de quartier
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de conseil de quartier"
      ok-title="Valider et ajouter une question"
      ok-variant="success"
      cancel-title="Annuler"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOkConseil"
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
        <b-form-group
          label="Choisissez la date du conseil (minimum le lendemain)"
          label-for="datepicker"
          invalid-feedback="Choisissez une date"
          :state="dateState"
        >
          <b-form-datepicker
            id="datepicker"
            :state="dateState"
            v-model="end_day"
            class="mb-2"
            :min="min_date"
          ></b-form-datepicker>
        </b-form-group>
        <b-form-group
          label="Choisissez l'heure du conseil"
          label-for="timepicker"
          invalid-feedback="Choisissez une heure"
          :state="timeState"
        >
          <b-form-timepicker
            id="timepicker"
            :state="timeState"
            v-model="end_time"
            class="mb-3"
            locale="fr"
          ></b-form-timepicker>
        </b-form-group>
      </form>
      <div modal-footer="Sauvegarder et quitter ">
        <b>Sauvegarder et quitter (sans publier) </b>
        <b-button
          size="lg"
          variant="primary"
          @click="
            handleOkConseil();
            quit = true;
          "
        >
          Sauvegarder
        </b-button>
      </div>
      <div modal-footer="Publier et quitter">
        <b>Publier sans question</b>
        <b-button
          size="lg"
          variant="primary"
          @click="
            handleOkConseil();
            publish = true;
          "
        >
          Publier
        </b-button>
      </div>
    </b-modal>

    <!-- SECOND MODAL FOR THE QUESTIONS -->
    <b-modal
      id="modal-prevent-closing-2"
      size="lg"
      ref="modal"
      title="Création d'une question"
      ok-title="Valider et ajouter une question"
      ok-variant="success"
      cancel-title="Annuler"
      no-close-on-backdrop
      @show="resetModal_2"
      @hidden="resetModal_2"
      @ok="handleOkQuestion"
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
        >
          <b-form-spinbutton
            id="answers_number"
            v-model="question.number_of_choices"
            min="2"
            max="10"
            v-if="this.question_type_name === 'QCM'"
          ></b-form-spinbutton>
        </b-form-group>
        <div v-if="this.question_type_name === 'QCM'">
          <b-form-group
            label="Choix de réponse"
            invalid-feedback="Entrez une réponse"
            v-for="number in question.number_of_choices"
            :key="number"
          >
            <b-form-input
              id="question_choice-input"
              v-model="question.choices[number]"
              required
            ></b-form-input>
          </b-form-group>
        </div>
      </form>
      <div modal-footer="Valider la question">
        <b>Enregistrer la question et sauvegarder le projet </b>
        <b-button
          id="save_quit"
          size="lg"
          variant="primary"
          @click="
            handleOkQuestion();
            quit = true;
          "
        >
          Sauvegarder le projet et quitter
        </b-button>
      </div>
      <div modal-footer="Valider la question">
        <b>Enregistrer et publier le projet </b>
        <b-button
          id="save_quit"
          size="lg"
          variant="primary"
          @click="
            handleOkQuestion();
            publish = true;
          "
        >
          Publier le projet
        </b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  computed: {
    dateState() {
      return this.end_day.length > 0 ? true : false;
    },
    timeState() {
      return this.end_time.length > 0 ? true : false;
    },
    nameState() {
      return this.conseil.name.length > 0 ? true : false;
    },
    placeState() {
      return this.conseil.place.length > 0 ? true : false;
    },
    descriptionState() {
      return this.conseil.description.length > 0 ? true : false;
    },
    questionNameState() {
      return this.question.wording.length > 0 ? true : false;
    },
    answerState() {
      if (this.question.number_of_choices > 0) {
        for (const choice in this.question.choices) {
          if (choice.length == 0) {
            return false;
          }
        }
        return true;
      } else {
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
    minDate.setDate(minDate.getDate() + 1);
    return {
      publish: false,
      quit: false,
      conseil: {
        name: '',
        place: '',
        description: '',
        end_date: '',
        project_type: ''
      },
      question: {
        type: '',
        wording: '',
        number_of_choices: 2,
        choices: []
      },
      min_date: minDate,
      end_day: '',
      end_time: '',
      end_date: '',
      id_project: '',
      id_owner: '',
      question_type_name: ''
    };
  },
  methods: {
    // We check the form with the infos of the Conseil is valid
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      if (this.dateState && this.timeState) {
        this.end_date = this.end_day + ' ' + this.end_time;
        return valid;
      } else {
        return false;
      }
    },

    // We check the form with the question infos is valid
    checkForm2Validity() {
      const valid = this.$refs.form.checkValidity();
      if (
        this.questionNameState &&
        this.answerState &&
        this.questionTypeState
      ) {
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
      this.end_day = '';
      this.end_time = '';
      this.quit = false;
      this.publish = false;
    },

    // We reset the data of the second form, question infos
    resetModal_2() {
      this.question.wording = '';
      this.question.type = '';
      this.question.number_of_choices = 2;
      this.quit = false;
      this.publish = false;
      // this.question.choices = [];
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
        project_type: this.projectType,
        end_date: this.end_date
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

    // We send a PUT request to the API with the id of the Conseil project to publish it
    publishConseil() {
      this.$axios.put('publication', { project_id: this.id_project });
    },

    // We call this function when clicking on one of the 3 buttons (Save and quit, Publish and quit, add a question)
    handleOkConseil() {
      this.handleSubmit();
    },

    // Function called by the previous one, taking care of the different steps
    async handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getConseilType();
      await this.postConseilData();
      if (this.publish == true) {
        this.publishConseil();
      }
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
        if (this.quit == false && this.publish == false) {
          this.$bvModal.show('modal-prevent-closing-2');
        }
      });
    },

    // We call this function when validating a question and adding a new one
    handleOkQuestion() {
      // bvModalEvt.preventDefault();
      this.handleSubmit_2();
    },

    // Function called by the previous one, taking care of the different steps
    async handleSubmit_2() {
      if (!this.checkForm2Validity()) {
        return;
      }
      console.log('number of choices  ', this.question.number_of_choices);
      console.log('question choices:  ', this.question.choices);
      this.question.type = await this.getQuestionType();
      await this.postQuestionData();
      if (this.publish == true) {
        this.publishConseil();
      }
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-2');
        if (this.quit == false && this.publish == false) {
          console.log('ON REOUVRE LE MODAL 2');
          this.$bvModal.show('modal-prevent-closing-2');
        }
      });
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
        console.log(response_1.data);
        const question_id = response_1.data['id_question'];
        if (this.question_type_name === 'QCM') {
          for (const choice in this.question.choices) {
            console.log('CHOICES    :', this.question.choices);
            console.log('CHOICE NUMBER    :', choice);
            console.log('CHOICE NAME  :', this.question.choices[choice]);
            const answer_data = {
              wording: this.question.choices[choice],
              question: question_id
            };
            const response_2 = await this.$axios.post(
              'mcq_answer/',
              answer_data
            );
            console.log(response_2.data);
          }
        }
        this.question.choices = [];
      } catch (error) {
        console.log(error.response);
        // const keys = Object.keys(error.response.data);
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
    }
  }
};
</script>
