<template>
  <div>
    <b-button v-b-modal.modal-modify-project class="button">
      Modifier la pétition
    </b-button>
    <br />
    <b-button v-b-modal.modal-publication class="button">
      Publier la pétition
    </b-button>

    <b-modal
      id="modal-modify-project"
      size="lg"
      ref="modal"
      title="Modification de la pétition"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
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
          invalid-feedback="Entrez un Lieu concerné par le conseil"
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
      <template #modal-footer="{cancel}">
        <b-button size="lg" class="button" @click="handleModifyPetition()">
          Sauvegarder
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- SECOND MODAL FOR PUBLICATION -->
    <b-modal
      id="modal-publication"
      size="lg"
      ref="modal"
      title="Publication de la pétition"
      no-close-on-backdrop
    >
      <form ref="form" @submit.stop.prevent="handleSubmit_2">
        <b-form-group label="Informations de la pétition: ">
          <h5>{{ petition.name }}</h5>
          <p>{{ petition.place }}</p>
          <p class="text-justify">{{ petition.description }}</p>
        </b-form-group>
        <b-form-group
          label="Une pétition a une durée de vie de 90 jours à partir de sa publication"
        >
        </b-form-group>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="success" @click="handlePublishPetition()">
          Publier la pétition
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- FOURTH MODAL FOR VALIDATION -->
    <b-modal id="modal-validation" title="Pétition publiée" hide-footer>
      <div class="d-block text-center">
        <h3>
          Votre pétition est publiée et désormais visible par tous. Les
          utilisateurs inscrits pourront la soutenir et la commenter.
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
  props: ['button', 'project_data'],
  computed: {
    nameState() {
      return this.petition.name.length > 0;
    },
    placeState() {
      return this.petition.place.length > 0;
    },
    descriptionState() {
      return this.petition.description.length > 0;
    }
  },
  data() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const endDate = new Date(today);
    endDate.setDate(today.getDate() + 90);
    return {
      button_label: this.button,
      petition: {
        id_project: this.project_data.id_project,
        id_owner: this.project_data.owner,
        name: this.project_data.name,
        place: this.project_data.place,
        description: this.project_data.description,
        project_type: this.project_data.project_type
      },
      end_date: endDate
    };
  },
  methods: {
    // We check the form with the infos of the Conseil is valid
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      return valid;
    },

    // We send a GET request to the API to get the id of the project type Conseil
    async getPetitionType() {
      const data = { name: 'Pétition' };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    },

    // We send a POST request to the API with the data about the Conseil
    async putPetitionData() {
      const data = {
        name: this.petition.name,
        place: this.petition.place,
        description: this.petition.description,
        project_type: this.petition.project_type
      };
      try {
        const response = await this.$axios.put(
          `project/${this.petition.id_project}/`,
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
      console.log('END DATE ', this.end_date);
      const data = {
        name: this.petition.name,
        place: this.petition.place,
        description: this.petition.description,
        project_type: this.petition.project_type,
        end_date: this.end_date
      };
      try {
        const response = await this.$axios.put(
          `project/${this.petition.id_project}/`,
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
    async publishPetition() {
      const response = await this.$axios.put('publication', {
        project_id: this.petition.id_project
      });
      return response.status;
    },

    // FUNCTIONS CALLED BY THE BUTTONS

    // Alternative to handleOkConseil() in the case we want to quit (publish or only saving) and not add any question
    handleModifyPetition() {
      this.handleSubmit_modify();
    },

    // Function called by the previous ones, taking care of the different steps
    async handleSubmit_modify() {
      if (!this.checkFormValidity()) {
        return;
      }
      await this.putPetitionData();
      this.$nextTick(() => {
        this.$emit('done');
        this.$bvModal.hide('modal-modify-project');
      });
    },

    // Function managing the publication of the petition
    handlePublishPetition() {
      this.handleSubmit();
    },

    // Function called by the previous ones, taking care of the different steps
    async handleSubmit() {
      console.log('PUBLICATION EN COURS ');
      //   await this.putPetitionData();
      await this.setEndDate();
      const publish_response = await this.publishPetition();
      this.$nextTick(() => {
        if (publish_response === 200) {
          this.$bvModal.hide('modal-modify-project');
          this.$bvModal.show('modal-validation');
        } else {
          window.alert(
            'Erreur lors de la publication du projet. \n Veuillez réessayer.'
          );
        }
      });
    },

    // Function called when Ok is clicked on the confirmation the project is published
    projectPublished() {
      this.$emit('done');
    }
  }
};
</script>
