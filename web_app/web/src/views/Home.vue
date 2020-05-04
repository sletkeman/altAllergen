<template>
  <div class="home">
    <v-form @submit.prevent="search" id="search">
      <v-container>
        <v-row>
          <v-col cols="4">
            <v-text-field
              v-model="searchParams.title"
              label="Recipe Name"
            ></v-text-field> </v-col
          ><v-col cols="4">
            <v-select
              v-model="searchParams.allergens"
              :items="allergens"
              label="Allergen Category"
              clearable
              multiple
            ></v-select>
          </v-col>
          <v-col cols="1" class="centered"
            ><v-btn type="submit" form="search">Search</v-btn></v-col
          >
        </v-row>
      </v-container>
    </v-form>
    <v-container>
      <div v-if="loading" class="centered">
        <v-progress-circular
          indeterminate
          color="primary"
          style="height: 200px;"
          :size="70"
          :width="7"
        ></v-progress-circular>
      </div>
      <div v-else>
        <div
          v-if="allergenChartData || ingredientChartData"
          style="height: 275px;"
        >
          <div
            v-if="allergenChartData"
            style="width: 50%; height: 250px; float: left"
          >
            <GChart
              type="PieChart"
              :data="allergenChartData"
              :options="allergenChartOptions"
            />
          </div>
          <div
            v-if="ingredientChartData"
            style="width: 50%; height: 250px; float: right"
          >
            <GChart
              type="BarChart"
              :data="ingredientChartData"
              :options="ingredientChartOptions"
            />
          </div>
        </div>

        <div v-if="stats.allergen">
          Retrieved {{ stats.allergen }} of {{ stats.title }} "{{
            searchParams.title
          }}" recipes that do not contain {{ textAllergen }}.
        </div>
        <div v-else-if="stats.title">
          Retrieved {{ recipes.length }} of {{ stats.title }} of "{{
            searchParams.title
          }}" recipes.
        </div>
        <v-data-table
          :headers="headers"
          :items="recipes"
          item-key="_id.$oid"
          show-expand
          class="elevation-1"
        >
          <template v-slot:item.title="{ item }">
            <router-link
              :to="{
                name: 'Recipe',
                params: { id: item._id.$oid }
              }"
              >{{ item.title }}</router-link
            >
          </template>
          <template v-slot:item.allergens="{ item }">
            {{ item.allergens ? item.allergens.length : 0 }}
          </template>
          <template v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length">
              <v-row>
                <v-col :cols="4">
                  <h4>Ingredients</h4>
                  <ul>
                    <li v-for="ing in item.ingredients" :key="ing">
                      {{ ing }}
                    </li>
                  </ul>
                </v-col>
                <v-col :cols="4">
                  <h4>Instructions</h4>
                  <div>{{ item.instructions }}</div>
                </v-col>
                <v-col :cols="4">
                  <h4>Allergens</h4>
                  <ul>
                    <li v-for="a in item.allergens" :key="a.group">
                      <div>{{ a.group }} - {{ a.ingredients.join(", ") }}</div>
                    </li>
                  </ul>
                </v-col>
              </v-row>
            </td>
          </template>
        </v-data-table>
      </div>
    </v-container>
  </div>
</template>

<script>
import { GChart } from "vue-google-charts";
import { mapState, mapActions } from "vuex";

export default {
  name: "Home",
  components: {
    GChart
  },
  data() {
    return {
      // recipes: [],
      // stats: {},
      // allergens: [],
      // searchParams: {
      //   title: "",
      //   allergens: []
      // },
      headers: [
        { text: "Recipe name", value: "title" },
        { text: "Number of possible allergens", value: "allergens" }
      ],
      loading: false,
      allergenChartData: null,
      allergenChartOptions: {
        chartArea: {
          width: "60%",
          height: "60%"
        },
        colors: ["#8B0000", "#3366cc"],
        height: 250,
        tooltip: {
          ignoreBounds: true
        },
        width: 500
      },
      ingredientChartData: null,
      ingredientChartOptions: {
        colors: ["#8B0000"],
        height: 250,
        legend: {
          position: "none"
        },
        hAxis: {
          title: "Number of Recipes",
          minValue: 0,
          textStyle: {
            fontSize: 8,
            color: "#4d4d4d"
          }
        },
        vAxis: {
          title: "Allergen Ingredient",
          textStyle: {
            fontSize: 8,
            color: "#4d4d4d"
          }
        }
      },
      showStats: false,
      ratio: 0,
      textAllergen: ""
    };
  },
  computed: {
    ...mapState({
      recipes: state => state.recipe.recipes,
      allergens: state => state.recipe.allergens,
      searchParams: state => state.recipe.searchParams,
      stats: state => state.recipe.stats
    })
  },
  methods: {
    ...mapActions(["GET_RECIPES", "GET_ALLERGENS"]),
    async search() {
      this.loading = true;
      await this.GET_RECIPES(this.searchParams);
      // this.recipes = recipes;
      // this.stats = stats;

      if (this.stats.title >= 0 && this.stats.allergen >= 0) {
        this.textAllergen = this.searchParams.allergens.join(", ");

        // Populate the table data for the Recipes Containing Allergen pie chart
        this.allergenChartData = [
          ["Label", "Count"],
          [
            `Recipes Containing ${this.textAllergen}`,
            this.stats.title - this.stats.allergen
          ],
          [`${this.textAllergen} Free Recipes`, this.stats.allergen]
        ];
        this.allergenChartOptions.title = `"${this.searchParams.title}" Recipes Containing ${this.textAllergen}`;

        // Populate the table data for the Allergen Ingredients Contained in Recipes bar chart
        if (
          this.stats.allergen_ingredients &&
          this.stats.allergen_ingredients.length > 0
        ) {
          this.ingredientChartOptions.title = `${this.searchParams.allergens[0]} Ingredients Contained in "${this.searchParams.title}" Recipes`;
          this.ingredientChartData = [
            ["Allergen Ingredient", "Number of Recipes with Allergen"]
          ];

          this.stats.allergen_ingredients.forEach(row => {
            this.ingredientChartData.push([row.ingredient, row.count]);
          });
        } else {
          this.ingredientChartData = null;
        }
      } else {
        this.allergenChartData = null;
        this.ingredientChartData = null;
      }

      this.loading = false;
    }
  },
  async mounted() {
    this.loading = true;
    await this.GET_RECIPES(this.searchParams);
    await this.GET_ALLERGENS();
    this.loading = false;
  }
};
</script>

<style scoped>
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
