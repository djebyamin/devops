import React, { useState } from "react";

const ClassifyMusic = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [service, setService] = useState("svm"); // Default service: "svm"
  const [loading, setLoading] = useState(false); // Loading state to show when request is in progress

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setResult(null); // Reset result when new file is selected
    setError(null);  // Reset error when new file is selected
  };

  const handleServiceChange = (event) => {
    setService(event.target.value);
    setResult(null); // Reset result when service is changed
    setError(null);  // Reset error when service is changed
  };

  const classifyMusic = async () => {
    if (!file) {
      setError("Veuillez télécharger un fichier audio.");
      return;
    }

    setLoading(true); // Set loading to true before the API call
    try {
      const formData = new FormData();
      formData.append("file", file); // Ensure the file is appended with the key "file"

      // Ensure the service name is dynamic
      const response = await fetch(`http://localhost:5000/${service}`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorDetails = await response.json();
        console.error("Erreur du serveur :", errorDetails);
        throw new Error(errorDetails.error || "Erreur lors de la classification");
      }

      const data = await response.json();
      setResult(data.genre); // Set result with the genre returned from the server
      setError(null); // Reset any previous error
    } catch (err) {
      setError("Erreur lors de la classification : " + err.message);
      setResult(null); // Reset result in case of error
      console.error("Erreur classification :", err);
    } finally {
      setLoading(false); // Reset loading state after API call completes
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-gray-900 text-white rounded-xl shadow-xl">
      <h1 className="text-3xl font-semibold mb-6 text-center">Classification de Musique</h1>
      
      <input
        type="file"
        accept="audio/*"
        onChange={handleFileChange}
        className="block w-full p-3 bg-gray-800 border-2 border-gray-600 rounded-lg text-gray-300 cursor-pointer mb-4"
      />
      
      {/* Service selection dropdown */}
      <div className="mb-4">
        <label htmlFor="service" className="block text-sm font-semibold mb-2">Choisir un service :</label>
        <select
          id="service"
          value={service}
          onChange={handleServiceChange}
          className="block w-full p-3 bg-gray-800 border-2 border-gray-600 rounded-lg text-gray-300"
        >
          <option value="svm">SVM</option>
          <option value="vgg">VGG</option>
        </select>
      </div>

      <button
        onClick={classifyMusic}
        className="w-full py-3 bg-indigo-600 text-white rounded-lg font-bold hover:bg-indigo-500 transition-colors duration-300"
        disabled={loading} // Disable button while loading
      >
        {loading ? "Classification en cours..." : "Classer la musique"}
      </button>

      {/* Display error message */}
      {error && (
        <p className="mt-4 text-red-400 font-semibold">{error}</p>
      )}
      
      {/* Display classification result */}
      {result && (
        <div className="mt-4">
          <label htmlFor="result" className="block text-sm font-semibold mb-2">Genre détecté :</label>
          <input
            id="result"
            type="text"
            value={result}
            readOnly
            className="block w-full p-3 bg-gray-800 border-2 border-gray-600 rounded-lg text-gray-300 cursor-not-allowed"
          />
        </div>
      )}
    </div>
  );
};

export default ClassifyMusic;
