<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      Créer une pétition
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de pétition"
      ok-title="Valider et publier la pétition"
      ok-variant="success"
      cancel-title="Annuler"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOkPetition"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Nom de la pétition"
          label-for="name-input"
          invalid-feedback="Vous devez donner un nom à la pétition"
          :state="nameState"
        >
          <b-form-input
            id="name-input"
            v-model="petition.name"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Lieu concerné"
          label-for="place-input"
          invalid-feedback="Entrez un lieu concerné par la pétition"
          :state="placeState"
        >
          <b-form-input
            id="place-input"
            v-model="petition.place"
            :state="placeState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Description de la pétition"
          label-for="description-input"
          invalid-feedback="Décrivez la pétition"
          :state="descriptionState"
        >
          <b-form-textarea
            id="description-input"
            v-model="petition.description"
            :state="descriptionState"
            required
          ></b-form-textarea>
        </b-form-group>
      </form>
      <div modal-footer="Valider la pétition">
        <b>Enregistrer la pétition et quitter </b>
        <b-button
          id="save_quit"
          size="lg"
          variant="primary"
          @click="handleOkPetition_and_quit()"
        >
          Sauvegarder et quitter
        </b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      save_and_quit: false,
      petition: {
        name: '',
        place: '',
        description: '',
        project_type: ''
      },
      id_project: '',
      id_owner: '',
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
      this.petition.name = '';
      this.petition.place = '';
      this.petition.description = '';
      this.nameState = null;
      this.placeState = null;
      this.descriptionState = null;
    },
    async postPetitionData() {
      const data = {
        name: this.petition.name,
        place: this.petition.place,
        description: this.petition.description,
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
    publishPetition() {
      console.log('PROJECT ID    :', this.id_project);
      this.$axios.put('publication', { project_id: this.id_project });
    },
    async getPetitionType() {
      const data = { name: 'Pétition' };
      const response = await this.$axios.get('project_type', { params: data });
      console.log(response);
      const type_id = response.data['id_project_type'];
      return type_id;
    },
    handleOkPetition() {
      // Trigger submit handler
      this.handleSubmit();
    },
    async handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getPetitionType();
      await this.postPetitionData();
      this.publishPetition();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
      });
    },
    handleOkPetition_and_quit() {
      // Trigger submit handler
      this.handleSubmit_2();
    },
    async handleSubmit_2() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getPetitionType();
      this.postPetitionData();

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
      });
    }
  }
};
</script>
