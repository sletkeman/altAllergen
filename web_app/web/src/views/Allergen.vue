<template>
  <div class="allergen">
    <v-data-table
      :headers="headers"
      :items="allergens"
      item-key="group"
      show-expand
      class="elevation-1"
      single-expand="false"
    >
      <template v-slot:item.ingredients="{ item }">
        {{ item.ingredients.length }}
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">{{ item.ingredients.join(", ") }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { fetchAllergens } from "../services/api";

export default {
  name: "Allergen",
  data() {
    return {
      allergens: [],
      headers: [
        { text: "Allergen Type", value: "group" },
        { text: "Number of Ingredients", value: "ingredients" }
      ]
    };
  },
  async mounted() {
    this.allergens = await fetchAllergens();
  }
};
</script>
