import callToast from "./callToast";

export default async function fetchData(endpoint) {
  const baseUrl = import.meta.env.VITE_API_URL;
  try {
    console.log(baseUrl);

    const response = await fetch(`${baseUrl}${endpoint}`);
    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error("Error while fetching users:", error);
    callToast("error", "Something went wrong...");
  }
}
