import React from "react";
import { Link } from "react-router-dom";
import "./NotFoundPage.css";
import cute404 from "../assets/404.svg";

const NotFoundPage = () => {
  return (
    <div className="not-found-page">
      <img src={cute404} alt="404 Not Found" className="not-found-image" />
      <h1>Oops! Page Not Found</h1>
      <p>Looks like you’re lost in space. Let’s go home!</p>
      <Link to="/" className="back-home">Go Back</Link>
    </div>
  );
};

export default NotFoundPage;