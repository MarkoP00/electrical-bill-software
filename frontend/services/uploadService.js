import callToast from "./callToast";

const baseUrl = import.meta.env.VITE_API_URL;

export async function uploadCSV(customerId, file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${baseUrl}/upload/${customerId}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    callToast("error", "An error occured while uploading file...");
    throw new Error(errorData.detail || "Upload failed");
  }

  return response.json();
}
