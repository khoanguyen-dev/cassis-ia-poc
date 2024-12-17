import React, { useState, useEffect } from "react";
import axios from "axios";
import EvenementTable from "./EvenementTable";
import DuplicateWarningModal from "./DuplicateWarningModal";
import "bootstrap/dist/css/bootstrap.min.css";

const EvenementInterface = () => {
  const [textInput, setTextInput] = useState("");
  const [fileInput, setFileInput] = useState(null);
  const [evenements, setEvenements] = useState([]);
  const [responseMessage, setResponseMessage] = useState("");
  const [duplicates, setDuplicates] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentDuplicateIndex, setCurrentDuplicateIndex] = useState(0);

  // Fetch events from the backend
  useEffect(() => {
    const fetchEvenements = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/evenements");
        setEvenements(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchEvenements();
  }, []);

  // Handle text input change
  const handleTextChange = (e) => setTextInput(e.target.value);

  // Handle file input change
  const handleFileChange = (e) => setFileInput(e.target.files[0]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("text", textInput);
    if (fileInput) {
      formData.append("file", fileInput);
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/process-evenement", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.status === 201) {
        const updatedEvenements = await axios.get("http://127.0.0.1:5000/evenements");
        setEvenements(updatedEvenements.data);
        setResponseMessage("Evenements successfully added!");
      }
    } catch (error) {
      if (error.response?.status === 409) {
        setDuplicates(error.response.data.duplicates);
        setCurrentDuplicateIndex(0); // Reset the index for modal navigation
        setShowModal(true); // Show modal with duplicates
      } else {
        setResponseMessage("An error occurred.");
        console.error(error);
      }
    }
  };

  // Resolve duplicate: Update the event
  const handleUpdate = async (updatedEvent) => {
    try {
      await axios.put("http://127.0.0.1:5000/update-evenement", updatedEvent);

      // Refresh the table and move to the next duplicate
      const updatedEvenements = await axios.get("http://127.0.0.1:5000/evenements");
      setEvenements(updatedEvenements.data);
      handleNextDuplicate();
    } catch (error) {
      console.error("Error updating event:", error);
    }
  };

  // Resolve duplicate: Replace the event
  const handleReplace = async (replacementEvent) => {
    if (!replacementEvent.numero) {
      alert("Please select an event to replace.");
      return;
    }
    try {
      await axios.put("http://127.0.0.1:5000/replace-evenement", [replacementEvent]);

      // Refresh the table and move to the next duplicate
      const updatedEvenements = await axios.get("http://127.0.0.1:5000/evenements");
      setEvenements(updatedEvenements.data);
      handleNextDuplicate();
    } catch (error) {
      console.error("Error replacing event:", error);
    }
  };

  // Resolve duplicate: Add as new event
  const handleAdd = async (newEvent) => {
    try {
      await axios.post("http://127.0.0.1:5000/add-evenement", newEvent); // Use the /add-evenement endpoint

      // Refresh the table and move to the next duplicate
      const updatedEvenements = await axios.get("http://127.0.0.1:5000/evenements");
      setEvenements(updatedEvenements.data);
      handleNextDuplicate();
    } catch (error) {
      console.error("Error adding new event:", error);
    }
  };

  // Move to the next duplicate or close the modal
  const handleNextDuplicate = () => {
    if (currentDuplicateIndex + 1 < duplicates.length) {
      setCurrentDuplicateIndex(currentDuplicateIndex + 1);
    } else {
      setShowModal(false);
      setResponseMessage("Duplicate resolution complete.");
    }
  };

  // Cancel duplicate resolution
  const handleCancel = () => {
    setShowModal(false);
    setResponseMessage("Duplicate resolution canceled.");
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center">Evenement Management</h1>

      {/* Display Table */}
      <section>
        <h2 className="mt-4">Evenements</h2>
        <EvenementTable evenements={evenements} />
      </section>

      {/* Input Panel */}
      <section>
        <h2 className="mt-4">Add New Events</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Enter Text:</label>
            <textarea
              value={textInput}
              onChange={handleTextChange}
              className="form-control"
              rows="5"
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Or Upload File:</label>
            <input
              type="file"
              accept=".txt"
              onChange={handleFileChange}
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
        {responseMessage && (
          <div className="mt-3 alert alert-info">
            <pre>{responseMessage}</pre>
          </div>
        )}
      </section>

      {/* Duplicate Warning Modal */}
      {showModal && duplicates.length > 0 && (
        <DuplicateWarningModal
          duplicate={duplicates[currentDuplicateIndex]}
          onUpdate={handleUpdate}
          onReplace={handleReplace}
          onAdd={handleAdd} // Pass the handleAdd function here
          onCancel={handleCancel}
          onNext={handleNextDuplicate}
        />
      )}
    </div>
  );
};

export default EvenementInterface;
