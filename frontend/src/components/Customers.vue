<template>
  <section class="customer-section">
    <h1>Customers in your base</h1>
    <div v-if="customers?.length">
      <div
        class="customer_wrapper"
        v-for="customer in customers"
        :key="customer.id">
        <div class="customer-card">
          <div class="customer-links">
            <button
              class="btn-icon view"
              @click="router.push(`/customers/${customer.id}`)">
              <i class="fa-solid fa-eye"></i>
            </button>
            <button
              class="btn-icon delete"
              @click="deleteUser(customer.id)">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
          <div class="customer-header">
            <h2>{{ customer.name }}</h2>
            <p class="customer-id">ID: {{ customer.id }}</p>
          </div>

          <div class="customer-info">
            <p><strong> Address:</strong> {{ customer.address }}</p>
            <p>
              <strong> City:</strong> {{ customer.city }} ({{
                customer.postal_number
              }})
            </p>
            <p>
              <strong> Email: </strong>
              <a :href="'mailto:' + customer.email"> {{ customer.email }}</a>
            </p>
            <p>
              <strong> Phone: </strong>
              <a :href="'tel:' + customer.phone">{{ customer.phone }}</a>
            </p>
          </div>
        </div>
      </div>
    </div>
    <p
      v-else
      class="paragraph-info">
      No customers created yet...
    </p>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
import callToast from "../../services/callToast";

const baseUrl = import.meta.env.VITE_API_URL;
const router = useRouter();
const emits = defineEmits(["customer-deleted"]);

defineProps({
  customers: {
    type: Array,
    required: true,
  },
});

async function deleteUser(id) {
  try {
    const response = await fetch(`${baseUrl}/customers/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      callToast("warning", "An error occured while deleting user");
      throw new Error(
        response.detail || "An error occured while deleting customer"
      );
    }
    callToast("success", "Customer deleted");
    emits("customer-deleted");
  } catch (error) {
    console.error(error);
    callToast("error", "Error ocured while deleting customer.");
  }
}
</script>

<style scoped>
.customer-section {
  padding: 0 8px;
}
.customer-section h1,
.paragraph-info {
  text-align: center;
  color: #eb721c;
}
.customer-card {
  max-width: 500px;
  width: 100%;
  margin: 20px auto;
  padding: 20px;
  border-radius: 12px;
  background: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  position: relative;
}

.customer-header {
  border-bottom: 1px solid #ddd;
  margin-bottom: 15px;
  padding-bottom: 10px;
}

.customer-header h2 {
  margin: 0;
  color: #333;
}

.customer-id {
  font-size: 0.85rem;
  color: #666;
}

.customer-info p {
  margin: 8px 0;
  font-size: 0.95rem;
  color: #444;
}

.customer-info a {
  color: #0066cc;
  text-decoration: none;
}

.customer-info a:hover {
  text-decoration: underline;
}

.customer-links {
  position: absolute;
  right: 3%;
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: #f1f1f1;
  color: #555;
  transition: all 0.2s ease-in-out;
  font-size: 16px;
}

.btn-icon:hover {
  background-color: #eb721c;
  color: #fff;
  transform: scale(1.05);
}

.btn-icon.delete {
  background-color: #ffeaea;
  color: #d9534f;
}

.btn-icon.delete:hover {
  background-color: #d9534f;
  color: #fff;
}

.btn-icon.view {
  background-color: #eaf4ff;
  color: #0275d8;
}

.btn-icon.view:hover {
  background-color: #0275d8;
  color: #fff;
}
</style>
