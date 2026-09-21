import React, { useState } from "react";
import Skeleton from "react-loading-skeleton";
import axios from "axios";
import "./App.css";

const App = () => {
  const [review, setReview] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [submit, setSubmit] = useState(false);
  const [skeleton, setSkeleton] = useState(false);
  const handleReviewChange = (event) => {
    setReview(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSkeleton(true);
    console.log(skeleton);
    try {
      const response = await axios.post("/api/predict", {
        review: review,
      });
      setSentiment(response.data.sentiment);
      setSubmit(true);
      setSkeleton(false);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="App">
      <h2>Restaurant Reviews Sentiment Analysis</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your restaurant review:
          <input value={review} onChange={handleReviewChange} />
        </label>
        <button type="submit">Analyze</button>
      </form>
      <div>
        {skeleton ? (
          <Skeleton />
        ) : (
          submit && (
            <p>
              It appears that the review is{" "}
              {sentiment ? "unsatisfactory" : "satisfactory"}
            </p>
          )
        )}
      </div>
    </div>
  );
};

export default App;
