<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      Créer une consultation
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de consultation"
      ok-title="Valider et ajouter une question"
      ok-variant="success"
      cancel-title="Annuler"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_1">
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
        <div modal-footer="Quitter sans sauvegarder">
          <b>Ajouter des questions plus tard </b>
          <!-- Emulate built in modal footer ok and cancel button actions -->
          <b-button size="lg" variant="primary" @click="ok()">
            Valider et quitter
          </b-button>
        </div>
      </form>
    </b-modal>

    <b-modal
      id="modal-prevent-closing-2"
      size="lg"
      ref="modal"
      title="Création d'une question"
      ok-title="Valider et ajouter une question"
      ok-variant="success"
      cancel-title="Annuler"
      no-close-on-backdrop
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_2">
        <b-form-group
          label="Titre de la question"
          label-for="question_wording-input"
          invalid-feedback="Vous devez donner un titre à la question"
          :state="nameState"
        >
          <b-form-input
            id="question_wording-input"
            v-model="question.wording"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Type de question" v-slot="{ ariaDescribedby }">
          <b-form-radio v-model="question.type" :aria-describedby="ariaDescribedby" name="some-radios" value="Réponse libre">Question à réponse libre</b-form-radio>
          <b-form-radio v-model="question.type" :aria-describedby="ariaDescribedby" name="some-radios" value="QCM">Question à choix multiples</b-form-radio>
        </b-form-group>

        <b-form-group
          label="Choix de réponse"
          invalid-feedback="Choisissez un type de question"
          v-slot="{ ariaDescribedby }"
          :state="placeState"
          v-if="question.type === 'QCM'"
        >
          <b-form-input
            id="question_choice-input"
            :state="descriptionState"
            required
          ></b-form-input>
        </b-form-group>
        <div modal-footer="Valider la question">
          <b>Enregistrer la question et quitter </b>
          <!-- Emulate built in modal footer ok and cancel button actions -->
          <b-button size="lg" variant="primary" @click="ok()">
            Valider et quitter
          </b-button>
        </div>
<!-- Gérer les boutons pour ajouter une question, et sauvegardée celle en cours, sauvegarder la question et quitter, ou annuler -->
        
      </form>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selected: "",
      consultation: {
        name: "",
        place: "",
        description: "",
        project_type: ""
      },
      question: {
        type: "",
        wording: "",
        choices: []
      },
      id_project: "",
      nameState: null,
      placeState: null,
      descriptionState: null
    };
  },
  methods: {
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = valid;
      this.placeState = valid;
      this.descriptionState = valid;
      return valid;
    },
    resetModal() {
      this.consultation.name = "";
      this.consultation.place = "";
      this.consultation.description = "";
      this.nameState = null;
      this.placeState = null;
      this.descriptionState = null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit_1();
    },
    async handleSubmit_1() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      console.log(this.consultation.name);
      console.log(this.consultation.place);
      console.log(this.consultation.description);
      this.projectType = await this.getConsultationType();
      this.postData();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide("modal-prevent-closing-1");
        this.$bvModal.show("modal-prevent-closing-2");
      });
    },
    async postData() {
      const data = {
        name: this.consultation.name,
        place: this.consultation.place,
        description: this.consultation.description,
        project_type: this.projectType
      };
      try {
        const response = await this.$axios.post("project/", data);
        this.id_project = response.data["id_project"];
      } catch (error) {
        console.log(error.response.data);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
    },
    async getConsultationType() {
      const data = { name: "Consultation" };
      const response = await this.$axios.get("project_type", { params: data });
      const type_id = response.data["id_project_type"];
      return type_id;
    }
  }
};
</script>
