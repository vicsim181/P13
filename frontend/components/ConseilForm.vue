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
      @ok="handleOkConseil_and_create_question"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_1">
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
          label="Choisissez la date du conseil (minimum 24h après la date
          actuelle)"
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
      <div modal-footer="Quitter sans sauvegarder">
        <b>Ajouter des questions plus tard </b>
        <b-button
          size="lg"
          variant="primary"
          @click="handleOkConseil_and_quit()"
        >
          Valider et quitter
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
      @ok="handleOkQuestion_and_new_question"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_3">
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
        >
          <b-form-radio
            v-model="question_type_name"
            :aria-describedby="ariaDescribedby"
            name="some-radios"
            value="Réponse libre"
            >Question à réponse libre</b-form-radio
          >
          <b-form-radio
            v-model="question_type_name"
            :aria-describedby="ariaDescribedby"
            name="some-radios"
            value="QCM"
            >Question à choix multiples</b-form-radio
          >
        </b-form-group>
        <b-form-spinbutton
          id="answers_number"
          v-model="question.number_of_choices"
          min="2"
          v-if="this.question_type_name === 'QCM'"
        ></b-form-spinbutton>
        <div v-if="this.question_type_name === 'QCM'">
          <b-form-group
            label="Choix de réponse"
            invalid-feedback="Choisissez un type de question"
            :state="placeState"
            v-for="number in question.number_of_choices"
            :key="number"
          >
            <b-form-input
              id="question_choice-input"
              v-model="question.choices[number]"
              :state="descriptionState"
              required
            ></b-form-input>
          </b-form-group>
        </div>
      </form>
      <div modal-footer="Valider la question">
        <b>Enregistrer la question et quitter </b>
        <b-button
          id="save_quit"
          size="lg"
          variant="primary"
          @click="handleOkQuestion_and_quit()"
        >
          Valider et quitter
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
    }
  },
  data() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const minDate = new Date(today);
    minDate.setDate(minDate.getDate() + 1);
    return {
      save_and_quit: false,
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
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      if (this.dateState && this.timeState) {
        this.end_date = this.end_day + ' ' + this.end_time;
        return valid;
      } else {
        return false;
      }
    },
    resetModal() {
      this.conseil.name = '';
      this.conseil.place = '';
      this.conseil.description = '';
      this.end_day = '';
      this.end_time = '';
    },
    resetModal_2() {
      this.question.wording = '';
      this.question.type = '';
    },
    handleOkConseil_and_create_question(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    async handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getConseilType();
      this.postConseilData();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
        this.$bvModal.show('modal-prevent-closing-2');
      });
    },
    async postConseilData() {
      console.log('DATE TOTAL   :', this.end_date);
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
    async getConseilType() {
      const data = { name: 'Conseil de quartier' };
      const response = await this.$axios.get('project_type', { params: data });
      console.log(response);
      const type_id = response.data['id_project_type'];
      return type_id;
    },
    handleOkConseil_and_quit() {
      // Trigger submit handler
      this.handleSubmit_2();
    },
    async handleSubmit_2() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getConseilType();
      this.postConseilData();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
      });
    },
    handleOkQuestion_and_new_question(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit_3();
    },
    async handleSubmit_3() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      console.log(this.question.wording);
      console.log(this.question.number_of_choices);
      console.log(this.question.choices);
      this.question.type = await this.getQuestionType();
      this.postQuestionData();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-2');
        this.$bvModal.show('modal-prevent-closing-2');
      });
    },
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
            const answer_data = {
              wording: this.question.choices[choice],
              question: question_id
            };
            console.log('ANSWER DATA  :', answer_data);
            const response_2 = await this.$axios.post(
              'mcq_answer/',
              answer_data
            );
            console.log(response_2.data);
          }
        }
      } catch (error) {
        console.log(error.response);
        // const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data;
        window.alert(errorMessage);
      }
    },
    async getQuestionType() {
      const data = { name: this.question_type_name };
      const response = await this.$axios.get('question_type', { params: data });
      const question_type_id = response.data['id_question_type'];
      return question_type_id;
    },
    handleOkQuestion_and_quit() {
      // Trigger submit handler
      this.handleSubmit_4();
    },
    async handleSubmit_4() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      console.log(this.question.wording);
      console.log(this.question.number_of_choices);
      console.log('QUESTION.CHOICES   :', this.question.choices);
      this.question.type = await this.getQuestionType();
      this.postQuestionData();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-2');
      });
    }
  }
};
</script>
