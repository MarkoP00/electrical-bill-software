<template>
  <section
    class="customer-page"
    v-if="customer && customer.id">
    <h1>Customer's Data</h1>
    <div class="customer-card">
      <h1>{{ customer.name }}</h1>
      <p class="customer-id">ID: {{ customer.id }}</p>

      <div class="update-customer">
        <button @click="() => (updateActive = !updateActive)">
          <i class="fa-solid fa-pen"></i>
        </button>
      </div>
      <div
        class="customer-info"
        v-if="!updateActive">
        <p><strong> Address:</strong> {{ customer.address }}</p>
        <p>
          <strong> City:</strong> {{ customer.city }} ({{
            customer.postal_number
          }})
        </p>
        <p>
          <strong> Email: </strong>
          <a :href="'mailto:' + customer.email">{{ customer.email }}</a>
        </p>
        <p>
          <strong> Phone: </strong>
          <a :href="'tel:' + customer.phone">{{ customer.phone }}</a>
        </p>
      </div>

      <!-- enable edit -->
      <div
        class="customer-info"
        v-else>
        <div class="form-group">
          <label for="name">Name</label>
          <input
            type="text"
            id="name"
            v-model="updateData.name" />
        </div>

        <div class="form-group">
          <label for="address">Address</label>
          <input
            type="text"
            id="address"
            v-model="updateData.address" />
        </div>

        <div class="form-group">
          <label for="city">City</label>
          <input
            type="text"
            id="city"
            v-model="updateData.city" />
        </div>

        <div class="form-group">
          <label for="postal_number">Postal Number</label>
          <input
            type="text"
            id="postal_number"
            v-model="updateData.postal_number" />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="updateData.email" />
        </div>

        <div class="form-group">
          <label for="phone">Phone</label>
          <input
            type="tel"
            id="phone"
            v-model="updateData.phone" />
        </div>

        <div class="customer-actions">
          <button
            class="btn save"
            @click="submitUpdate">
            Save Changes
          </button>
          <button
            class="btn cancel"
            @click="updateActive = false">
            Cancel
          </button>
        </div>
      </div>

      <div class="customer-actions">
        <button
          class="btn back"
          @click="router.push('/')">
          ⬅ Back to Customers
        </button>
      </div>
    </div>

    <main class="customer-invoice-container">
      <div class="invoice-title">
        <h1>Customer's Invoices</h1>
      </div>
      <div
        class="customer-invoices"
        v-if="customerInvoices?.length">
        <div class="invoices-wrapper">
          <div
            v-for="invoice in customerInvoices"
            :key="invoice.id">
            <InvoiceCard
              :invoice="invoice"
              @invoice-deleted="reloadData"></InvoiceCard>
          </div>
        </div>
      </div>
      <p v-else>No invoices generated yet.</p>
    </main>

    <!-- upload CSV seciton -->

    <UploadCSV
      :customer="customer"
      @upload-success="reloadData"></UploadCSV>
  </section>

  <p
    v-else
    class="loading">
    Loading customer data...
  </p>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import fetchData from "../../services/fetchData";
import InvoiceCard from "../components/InvoiceCard.vue";
import UploadCSV from "../components/UploadCSV.vue";
import callToast from "../../services/callToast";

const baseUrl = import.meta.env.VITE_API_URL;

const router = useRouter();
const route = useRoute();

const customer = ref({});
const customerID = ref(route.params.id);
const customerInvoices = ref({});

const updateData = ref();
const updateActive = ref(false);

onMounted(async () => {
  customer.value = await fetchData(`/customers/${customerID.value}`);
  updateData.value = customer.value;

  customerInvoices.value = await fetchData(
    `/customers/${customerID.value}/invoices`
  );
});

async function reloadData() {
  customerInvoices.value = await fetchData(
    `/customers/${customerID.value}/invoices`
  );
}

async function submitUpdate() {
  console.log("fire");
  console.log(`${baseUrl}/customers/${customerID.value}`);
  console.log(updateData.value);

  try {
    const response = await fetch(`${baseUrl}/customers/${customerID.value}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData.value),
    });

    if (!response.ok) {
      callToast("warning", "Problem while updating customer...");
      return;
    }

    customer.value = updateData.value;
    updateActive.value = false;
    callToast("success", "Customer updated");
  } catch (error) {
    console.error(error);
  }
}
</script>

<style scoped>
.customer-page {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  margin-top: 120px;
}

.customer-card {
  max-width: 600px;
  width: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  position: relative;
}

h1 {
  margin-bottom: 5px;
  color: #eb721c;
}

.customer-id {
  font-size: 13px;
  color: #888;
  margin-bottom: 15px;
}

.customer-info .form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}

.customer-info label {
  font-weight: bold;
  color: #eb721c;
  margin-bottom: 4px;
}

.customer-info input {
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.customer-info input:focus {
  border-color: #eb721c;
  outline: none;
}

.customer-actions .btn.save {
  background-color: #eb721c;
  color: white;
  border: none;
  padding: 8px 16px;
  margin-right: 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.customer-actions .btn.save:hover {
  background-color: #eb721c;
}

.customer-actions .btn.cancel {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ccc;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.customer-actions .btn.cancel:hover {
  background-color: #e0e0e0;
}

.customer-info p {
  margin: 8px 0;
  font-size: 14px;
}

.customer-info a {
  color: #eb721c;
  text-decoration: none;
}

.customer-info a:hover {
  text-decoration: underline;
}

.customer-actions {
  margin-top: 20px;
  text-align: right;
}

.btn {
  padding: 8px 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn.back {
  background-color: #eb721c;
  color: white;
}

.btn.back:hover {
  background-color: #d45d12;
}

.loading {
  text-align: center;
  margin-top: 50px;
  font-size: 16px;
  color: #555;
}

.customer-invoice-container p {
  text-align: center;
}
.customer-invoices {
  padding: 20px;
}

.invoice-title {
  margin-bottom: 20px;
  text-align: center;
}

.invoices-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.invoice-item {
  display: flex;
}

.update-customer {
  position: absolute;
  top: 5%;
  right: 3%;
}
.update-customer button {
  background-color: rgb(235, 114, 28, 0.2);
  color: #eb721c;
  border: none;
  padding: 15px 10px;
  border-radius: 100px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, transform 0.1s;
}

.update-customer button:hover {
  color: #fff;
  background: #eb721c;
}

.update-customer button i {
  margin-right: 4px;
}
</style>
