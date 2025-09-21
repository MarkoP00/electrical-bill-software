<template>
  <div class="upload-container">
    <h1>Upload CSV File & Generate Invoice</h1>

    <form
      @submit.prevent="uploadFile"
      class="upload-form">
      <div class="form-group">
        <label for="csvFile">CSV File:</label>
        <input
          type="file"
          id="csvFile"
          accept=".csv"
          @change="onFileSelect"
          required />
        <small>Only CSV files with expected format</small>
      </div>

      <button
        type="submit"
        :disabled="uploading"
        class="upload-btn">
        {{ uploading ? "Uploading..." : "Upload CSV" }}
      </button>
    </form>

    <!-- Progress bar -->
    <div
      v-if="uploading"
      class="progress">
      <div class="progress-bar"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { uploadCSV } from "../../services/uploadService";
import { createInvoice, openPDF } from "../../services/invoiceService";
import { sendInvoice } from "../../services/sendInvoice";
import callToast from "../../services/callToast";

const baseUrl = import.meta.env.VITE_API_URL;

const props = defineProps({
  customer: { type: Object, required: true },
});

const emit = defineEmits(["upload-success"]);
const selectedFile = ref(null);
const uploading = ref(false);

const onFileSelect = (e) => {
  selectedFile.value = e.target.files[0];
};

const uploadFile = async () => {
  if (!selectedFile.value) {
    callToast("error", "Please select a CSV file first!");
    return;
  }

  uploading.value = true;

  try {
    const result = await uploadCSV(props.customer.id, selectedFile.value);

    const invoice = await createInvoice({
      customer_id: result.customer_id,
      period_from: result.period_from,
      period_to: result.period_to,
    });

    // waiting for pdf generation
    await fetch(`${baseUrl}/invoices/${invoice.id}/pdf`);
    // then sending email with pdf
    const send = await sendInvoice(invoice.id);
    // download / open pdf
    openPDF(invoice.id);
    callToast("success", "Invoice uploaded.");
    emit("upload-success");
  } catch (err) {
    console.error(err);
    callToast("error", err.message);
  } finally {
    selectedFile.value = null;
    document.getElementById("csvFile").value = "";
    uploading.value = false;
  }
};
</script>

<style scoped>
.upload-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.upload-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

input[type="file"] {
  width: 100%;
  padding: 10px;
  border: 2px dashed #eb721c;
  border-radius: 8px;
  background: #f8f9fa;
  cursor: pointer;
}

input[type="file"]:hover {
  border-color: #eb721c;
  background: #e9ecef;
}

small {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 12px;
}

.upload-btn {
  width: 100%;
  background: #eb721c;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn:hover:not(:disabled) {
  background: #ab5111;
}

.upload-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.progress {
  margin-top: 20px;
  height: 6px;
  background: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #eb721c, #eb721ca7);
  animation: progress 1.5s ease-in-out infinite;
}

@keyframes progress {
  0% {
    transform: translateX(-100%);
    width: 50%;
  }
  50% {
    transform: translateX(0%);
    width: 75%;
  }
  100% {
    transform: translateX(100%);
    width: 50%;
  }
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 24px;
}
</style>
