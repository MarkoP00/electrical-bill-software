import callToast from "./callToast";

const baseUrl = import.meta.env.VITE_API_URL;

export async function sendInvoice(invoice_id) {
  const response = await fetch(`${baseUrl}/invoices/${invoice_id}/send`, {
    method: "POST",
  });

  if (!response.ok) {
    const error = await response.json();
    callToast("warning", "Problem while sending email...");
    throw new Error(error.detail || "Invoice send failed");
  }

  return response.json();
}
