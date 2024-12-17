import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import SideMenu from "./SideMenu";
import AnnuaireInterface from "./AnnuaireInterface";
import EvenementInterface from "./EvenementInterface";
import "bootstrap/dist/css/bootstrap.min.css";

const App = () => {
  const [isMenuMinimized, setIsMenuMinimized] = useState(false);

  return (
    <Router>
      <div className="d-flex">
        {/* Side Menu */}
        <SideMenu isMinimized={isMenuMinimized} toggleMenu={() => setIsMenuMinimized(!isMenuMinimized)} />

        {/* Main Content */}
        <div className="flex-grow-1 p-4">
          <Routes>
            <Route path="/annuaire" element={<AnnuaireInterface />} />
            <Route path="/evenement" element={<EvenementInterface />} />
            {/* Redirect root path to annuaire */}
            <Route path="/" element={<Navigate to="/annuaire" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
