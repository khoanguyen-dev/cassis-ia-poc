import React, { useState, useEffect } from "react";
import axios from "axios";
import AnnuaireTable from "./AnnuaireTable";
import DuplicateWarningModal from "./DuplicateWarningModal";
import "bootstrap/dist/css/bootstrap.min.css";

const AnnuaireInterface = () => {
  const [textInput, setTextInput] = useState("");
  const [urlInput, setUrlInput] = useState("");
  const [fileInput, setFileInput] = useState(null);
  const [entries, setEntries] = useState([]);
  const [responseMessage, setResponseMessage] = useState("");
  const [duplicates, setDuplicates] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentDuplicateIndex, setCurrentDuplicateIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:5000/annuaire");
      setEntries(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setResponseMessage("Failed to fetch entries.");
      setIsLoading(false);
    }
  };

  const resetInputs = () => {
    setTextInput("");
    setUrlInput("");
    setFileInput(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("text", textInput);
    formData.append("url", urlInput);
    if (fileInput) formData.append("file", fileInput);

    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/process-annuaire", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.status === 201) {
        fetchEntries();
        setResponseMessage("Entries successfully added!");
        resetInputs();
      }
    } catch (error) {
      handleResponseError(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResponseError = (error) => {
    if (error.response) {
      const { status, data } = error.response;
      if (status === 409) {
        setDuplicates(data.duplicates || []);
        setCurrentDuplicateIndex(0);
        setShowModal(true);
      } else {
        setResponseMessage(`Error (${status}): ${data?.error || "An error occurred."}`);
      }
    } else {
      setResponseMessage("An unexpected error occurred. Please try again.");
    }
  };

  const handleNextDuplicate = () => {
    if (currentDuplicateIndex + 1 < duplicates.length) {
      setCurrentDuplicateIndex(currentDuplicateIndex + 1);
    } else {
      setShowModal(false);
      setResponseMessage("Duplicate resolution complete.");
    }
  };

  const handleCancel = () => {
    setShowModal(false);
    setResponseMessage("Duplicate resolution canceled.");
  };

  const handleDuplicateResolution = async (action, updatedEntry) => {
    try {
      const url =
        action === "replace"
          ? "http://127.0.0.1:5000/replace-annuaire"
          : "http://127.0.0.1:5000/add-annuaire";

      const method = action === "replace" ? "put" : "post";

      await axios[method](url, action === "replace" ? [updatedEntry] : updatedEntry);
      fetchEntries();
      handleNextDuplicate();
    } catch (error) {
      console.error(`Error resolving duplicate with ${action}:`, error);
      setResponseMessage(`Failed to ${action} entry.`);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center">Annuaire Management</h1>

      {isLoading && (
        <div className="alert alert-info text-center" role="alert">
          Loading...
        </div>
      )}

      <section>
        <h2 className="mt-4">Annuaire</h2>
        <AnnuaireTable entries={entries} />
      </section>

      <section>
        <h2 className="mt-4">Add New Entries</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Enter Text:</label>
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              className="form-control"
              rows="3"
              placeholder="Enter text data..."
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Or Enter URL:</label>
            <input
              type="url"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              className="form-control"
              placeholder="https://example.com"
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Or Upload File (CSV/XLSX/TXT):</label>
            <input
              type="file"
              accept=".txt,.csv,.xlsx"
              onChange={(e) => setFileInput(e.target.files[0])}
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={isLoading}>
            {isLoading ? "Submitting..." : "Submit"}
          </button>
        </form>
        {responseMessage && (
          <div className="mt-3 alert alert-info">
            <pre>{responseMessage}</pre>
          </div>
        )}
      </section>

      {showModal && duplicates.length > 0 && (
        <DuplicateWarningModal
          duplicate={duplicates[currentDuplicateIndex]}
          onUpdate={(updatedEntry) => handleDuplicateResolution("replace", updatedEntry)}
          onReplace={(replacementEntry) => handleDuplicateResolution("replace", replacementEntry)}
          onAdd={(newEntry) => handleDuplicateResolution("add", newEntry)}
          onCancel={handleCancel}
          onNext={handleNextDuplicate}
        />
      )}
    </div>
  );
};

export default AnnuaireInterface;
