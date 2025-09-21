import callToast from "./callToast";

const baseUrl = import.meta.env.VITE_API_URL;

export async function createInvoice({ customer_id, period_from, period_to }) {
  const response = await fetch(`${baseUrl}/invoices`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ customer_id, period_from, period_to }),
  });

  if (!response.ok) {
    const error = await response.json();
    callToast("warning", "Problem while creating invoice..");
    throw new Error(error.detail || "Invoice creation failed");
  }

  return await response.json();
}

export function openPDF(invoiceId) {
  window.open(`${baseUrl}/invoices/${invoiceId}/pdf`, "_blank");
}
