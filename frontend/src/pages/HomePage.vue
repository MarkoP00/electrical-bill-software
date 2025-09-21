<template>
  <main class="main-wrapper">
    <CustomerForm @customer-created="refreshCustomers"></CustomerForm>
    <Customers
      :customers="customers"
      @customer-deleted="refreshCustomers"></Customers>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import fetchData from "../../services/fetchData.js";
import Customers from "../components/Customers.vue";
import CustomerForm from "../components/CustomerForm.vue";

const customers = ref([]);

async function refreshCustomers() {
  customers.value = await fetchData(`/customers`);
}

onMounted(async () => {
  await refreshCustomers();
});
</script>

<style scoped>
.main-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 30px;
}
</style>
