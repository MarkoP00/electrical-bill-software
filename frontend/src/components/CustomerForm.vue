<template>
  <section class="form-container">
    <h2>Add New Customer</h2>
    <form @submit.prevent="customerCreate">
      <div class="form-group">
        <label for="name">Full Name</label>
        <input
          v-model="form.name"
          type="text"
          id="name"
          required
          placeholder="Enter full name" />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          v-model="form.email"
          type="email"
          id="email"
          required
          placeholder="Enter email address" />
      </div>

      <div class="form-group">
        <label for="phone">Phone</label>
        <input
          v-model="form.phone"
          type="tel"
          id="phone"
          required
          placeholder="Enter phone number" />
      </div>

      <div class="form-group">
        <label for="address">Address</label>
        <input
          v-model="form.address"
          type="text"
          id="address"
          required
          placeholder="Street and number" />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="city">City</label>
          <input
            v-model="form.city"
            type="text"
            id="city"
            required
            placeholder="Enter city" />
        </div>

        <div class="form-group">
          <label for="postal">Postal Number</label>
          <input
            v-model="form.postal_number"
            type="text"
            id="postal"
            required
            placeholder="Postal code" />
        </div>
      </div>

      <button
        type="submit"
        class="btn">
        Create Customer
      </button>
    </form>
  </section>
</template>

<script setup>
import { reactive } from "vue";
import callToast from "../../services/callToast";

const baseUrl = import.meta.env.VITE_API_URL;
const emit = defineEmits(["customer-created"]);

const form = reactive({
  name: "",
  email: "",
  phone: "",
  address: "",
  city: "",
  postal_number: "",
});

async function customerCreate() {
  try {
    const response = await fetch(`${baseUrl}/customers`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(form),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Server error:", errorData);
      callToast("error", "Problem occured while creating user...");
      throw new Error(errorData.detail || "Failed to create customer");
    }

    callToast("success", "Customer created successfully");
    emit("customer-created");

    // form reset
    form.name = "";
    form.email = "";
    form.phone = "";
    form.address = "";
    form.city = "";
    form.postal_number = "";
  } catch (error) {
    console.error("Error creating customer:", error);
    callToast("error", "Something went wrong while creating user...");
    throw error;
  }
}
</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-top: 150px;
}

h2 {
  margin-bottom: 15px;
  color: #eb721c;
}

.form-group {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: 600;
}

.form-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-row {
  display: flex;
  gap: 10px;
}

.btn {
  width: 100%;
  padding: 10px;
  background-color: #eb721c;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  cursor: pointer;
}

.btn:hover {
  background-color: #d86419;
}
</style>
