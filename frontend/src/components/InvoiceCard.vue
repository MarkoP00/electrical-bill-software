<template>
  <div class="invoice-card">
    <div class="customer-links">
      <button
        class="btn-icon view"
        @click="openPDF(invoice.id)">
        <i class="fa-solid fa-eye"></i>
      </button>
      <button
        class="btn-icon delete"
        @click="deleteInvoice(invoice.id)">
        <i class="fa-solid fa-trash"></i>
      </button>
    </div>
    <div class="icon">
      <i class="fa-solid fa-file-pdf"></i>
    </div>
    <div class="details">
      <h3>{{ fileName }}</h3>
      <p>
        <strong>Period:</strong> {{ formatDate(invoice.period_from) }} →
        {{ formatDate(invoice.period_to) }}
      </p>
      <p><strong>ID:</strong> {{ invoice.id }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import callToast from "../../services/callToast";

const emits = defineEmits(["invoice-deleted"]);
const props = defineProps({
  invoice: {
    type: Object,
    required: true,
  },
});

const baseUrl = import.meta.env.VITE_API_URL;

const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const fileName = computed(() => {
  const date = new Date(props.invoice.period_from);
  const month = monthNames[date.getMonth()];
  return `invoice_${month}.pdf`;
});

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-GB");
}

function openPDF(invoiceId) {
  window.open(`http://127.0.0.1:8000/invoices/${invoiceId}/pdf`, "_blank");
}

async function deleteInvoice(invoiceID) {
  try {
    const response = await fetch(`${baseUrl}/invoices/${invoiceID}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      callToast("warning", "Something went wrong while deleting invoice..");
      return;
    }

    callToast("success", "Invoice deleted successfully");
    emits("invoice-deleted");
  } catch (error) {
    console.error("Error while deleting invoice", error);
    callToast("error", "Error occurred while deleting invoice");
  }
}
</script>

<style scoped>
.invoice-card {
  display: flex;
  align-items: flex-start;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 15px 20px;
  margin-bottom: 15px;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

/* .invoice-card:hover {
  transform: scale(1.03);
} */

.icon {
  font-size: 30px;
  color: #e63946;
  margin-right: 15px;
}

.details h3 {
  margin: 0 0 5px;
  color: #eb721c;
  font-size: 16px;
}

.details p {
  margin: 3px 0;
  font-size: 14px;
  color: #333;
}

.invoice-id {
  font-size: 12px;
  color: #888;
  margin-top: 8px;
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
