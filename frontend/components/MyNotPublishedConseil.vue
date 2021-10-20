<template>
  <div>
    <b-button v-b-modal.modal-modify-project class="button">
      Modifier le conseil
    </b-button>
    <br />
    <b-button v-b-modal.modal-add-question class="button">
      Ajouter une question
    </b-button>
    <br />
    <b-button v-b-modal.modal-publication class="button">
      Publier le conseil
    </b-button>

    <b-modal
      id="modal-modify-project"
      size="lg"
      ref="modal"
      title="Modification du conseil de quartier"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
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
        <b-button size="lg" class="button" @click="handleModifyConseil()">
          Sauvegarder
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- SECOND MODAL FOR THE QUESTIONS -->
    <b-modal
      id="modal-add-question"
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
        <b-button size="lg" class="button" @click="handleAddQuestion()">
          Sauvegarder
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- THIRD MODAL FOR PUBLICATION -->
    <b-modal
      id="modal-publication"
      size="lg"
      ref="modal"
      title="Publication du conseil de quartier"
      no-close-on-backdrop
      @show="resetModal_2"
      @hidden="resetModal_2"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_2">
        <b-form-group label="Informations du conseil: ">
          <h5>{{ conseil.name }}</h5>
          <p>{{ conseil.place }}</p>
          <p class="text-justify">{{ conseil.description }}</p>
        </b-form-group>

        <b-form-group
          label="Choisissez la date du conseil (minimum 7 jours à partir d'aujourd'hui)"
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
            placeholder="Choisissez une date"
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
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="success" @click="handlePublishConseil()">
          Publier le conseil
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- FOURTH MODAL FOR VALIDATION -->
    <b-modal id="modal-validation" title="Conseil publié" hide-footer>
      <div class="d-block text-center">
        <h3>
          Votre projet est publié et désormais visible par tous. Si vous y avez
          attaché un sondage, les membres inscrits pourront y participer.
        </h3>
      </div>
      <b-button
        class="mt-3 button"
        block
        @click="
          projectPublished();
          $bvModal.hide('modal-validation');
        "
        >Ok</b-button
      >
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ["button", "project_data"],
  computed: {
    dateState() {
      return this.end_day.length > 0;
    },
    timeState() {
      return this.end_time.length > 0;
    },
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
          } else if (this.question.choices[choice] === " ") {
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
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const minDate = new Date(today);
    minDate.setDate(minDate.getDate() + 7);
    return {
      button_label: this.button,
      conseil: {
        id_project: this.project_data.id_project,
        id_owner: this.project_data.owner,
        name: this.project_data.name,
        place: this.project_data.place,
        description: this.project_data.description,
        project_type: this.project_data.project_type,
        questions: [this.project_data.question]
      },
      question: {
        type: "",
        wording: "",
        number_of_choices: 2,
        choices: []
      },
      min_date: minDate,
      end_day: "",
      end_time: "",
      end_date: "",
      question_type_name: ""
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
      if (this.questionNameState && this.questionTypeState) {
        if (this.question_type_name === "QCM") {
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

    // We check the form with the date before publishing
    checkForm3Validity() {
      const valid = this.$refs.form.checkValidity();
      if (this.dateState && this.timeState) {
        this.end_date = this.end_day + " " + this.end_time;
        return valid;
      } else {
        return false;
      }
    },

    // We reset the data of the second form, question infos
    resetModal() {
      this.question.wording = "";
      this.question.type = "";
      this.question.number_of_choices = 2;
      this.question.choices = [];
    },

    // We reset the data of the second form, question infos
    resetModal_2() {
      this.end_day = "";
      this.end_time = "";
      this.end_date = "";
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
      console.log("NUMBER OF CHOCIES ", this.question.number_of_choices);
    },

    // We send a GET request to the API to get the id of the project type Conseil
    async getConseilType() {
      const data = { name: "Conseil de quartier" };
      const response = await this.$axios.get("project_type", { params: data });
      const type_id = response.data["id_project_type"];
      return type_id;
    },

    // We send a POST request to the API with the data about the Conseil
    async putConseilData() {
      console.log("END DATE ", this.end_date);
      const data = {
        name: this.conseil.name,
        place: this.conseil.place,
        description: this.conseil.description,
        project_type: this.conseil.project_type
      };
      try {
        const response = await this.$axios.put(
          `project/${this.conseil.id_project}/`,
          data
        );
        console.log(response.data);
      } catch (error) {
        console.log(error.response);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
    },

    // Set the end_date of the project when published
    async setEndDate() {
      const data = {
        name: this.conseil.name,
        place: this.conseil.place,
        description: this.conseil.description,
        project_type: this.conseil.project_type,
        end_date: this.end_date
      };
      try {
        const response = await this.$axios.put(
          `project/${this.conseil.id_project}/`,
          data
        );
        console.log(response.data);
      } catch (error) {
        console.log(error.response);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
    },

    // We send a PUT request to the API with the id of the Conseil project to publish it
    async publishConseil() {
      const response = await this.$axios.put("publication", {
        project_id: this.project_data.id_project
      });
      return response.status;
    },

    // We send a POST request to the API to post a question
    async postQuestionData() {
      const question_data = {
        wording: this.question.wording,
        question_type: this.question.type,
        project: this.project_data.id_project
      };
      try {
        const response_1 = await this.$axios.post("question/", question_data);
        console.log(response_1.data);
        const question_id = response_1.data["id_question"];
        if (this.question_type_name === "QCM") {
          for (const choice in this.question.choices) {
            const answer_data = {
              wording: this.question.choices[choice],
              question: question_id
            };
            await this.$axios.post("mcq_answer/", answer_data);
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
      const response = await this.$axios.get("question_type", { params: data });
      const question_type_id = response.data["id_question_type"];
      return question_type_id;
    },

    // FUNCTIONS CALLED BY THE BUTTONS

    // Alternative to handleOkConseil() in the case we want to quit (publish or only saving) and not add any question
    handleModifyConseil() {
      this.handleSubmit_modify();
    },

    // Function called by the previous ones, taking care of the different steps
    async handleSubmit_modify() {
      if (!this.checkFormValidity()) {
        return;
      }
      await this.putConseilData();
      this.$nextTick(() => {
        this.$emit("done");
        this.$bvModal.hide("modal-modify-project");
      });
    },

    handlePublishConseil() {
      this.handleSubmit();
    },
    // Function called by the previous ones, taking care of the different steps
    async handleSubmit() {
      if (!this.checkForm3Validity()) {
        return;
      }
      // await this.putConseilData();
      await this.setEndDate();
      const publish_response = await this.publishConseil();
      this.$nextTick(() => {
        if (publish_response === 200) {
          this.$bvModal.hide("modal-modify-project");
          this.$bvModal.show("modal-validation");
        } else {
          window.alert(
            "Erreur lors de la publication du projet. \n Veuillez réessayer."
          );
        }
      });
    },

    // Function called when Ok is clicked on the confirmation the project is published
    projectPublished() {
      this.$emit("done");
    },

    // Alternative to handleOkQuestion() in case we want to quit (publish or just save) without adding new question
    handleAddQuestion() {
      this.handleSubmit_2();
    },
    // Function called by the previous ones, taking care of the different steps
    async handleSubmit_2() {
      if (!this.checkForm2Validity()) {
        return;
      }
      this.question.type = await this.getQuestionType();
      await this.postQuestionData();
      this.$nextTick(() => {
        this.$emit("done");
        this.$bvModal.hide("modal-add-question");
      });
    }
  },
  async fetch() {
    this.conseil.questions = this.project_data.question;
    if (this.conseil.questions.length > 0) {
      for (const question in this.conseil.questions) {
        let mcq = this.conseil.questions[question].mcqanswer;
        if (typeof mcq !== "undefined" && mcq.length > 0) {
          for (const choice in mcq) {
            const response = await this.$axios.get(mcq[choice]);
            this.mcq_answers.push(response.data["wording"]);
          }
        }
      }
    }
    this.loaded = true;
  }
};
</script>
