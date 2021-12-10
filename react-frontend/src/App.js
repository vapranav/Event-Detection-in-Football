import logo from "./logo.svg";
import "./App.css";
import React, { useEffect, useState } from "react";
import ReactPlayer from "react-player";
import axios from "axios";
import OverallVideo from "./media/cards-corners.mp4";

function App() {
  const ref = React.createRef();
  const cardVideo = React.createRef();
  const [getCorners, setCorners] = useState({});
  const [getCards, setCards] = useState({});
  const [cornerVisible, setCornerVisible] = useState(false);
  const [cardVisible, setCardVisible] = useState(false);

  useEffect(() => {
    axios
      .get("http://localhost:5000/corners")
      .then((response) => {
        console.log("SUCCESS", response);
        setCorners(response);
      })
      .catch((error) => {
        console.log(error);
      });
    axios
      .get("http://localhost:5000/cards")
      .then((response) => {
        console.log("SUCCESS", response);
        setCards(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const handleCorner = (e) => {
    e.preventDefault();
    setCornerVisible(true);
    setCardVisible(false);
  };
  const handleCard = (e) => {
    e.preventDefault();
    setCardVisible(true);
    setCornerVisible(false);
  };

  return (
    <div className='App'>
      <header className='App-header'>
        {/* <img src={logo} className='App-logo' alt='logo' />
        <p>React + Flask Tutorial</p> */}
        <h2> Analyze your clips </h2>
        <button onClick={() => console.log("clicked")}>
          Upload your clip!
        </button>
        <button style={{ margin: 5 }} onClick={handleCorner}>
          Get Corner Timestamps
        </button>
        <button onClick={handleCard}>Get Card Timestamps</button>
        <ReactPlayer ref={ref} url={OverallVideo} controls={true} />
        <div>
          {getCards.status === 200 && cardVisible == true ? (
            getCards.data.timestamps.map((time) => (
              <button onClick={() => ref.current.seekTo(time)}>
                Seek to {time}
              </button>
            ))
          ) : (
            <h3></h3>
          )}
        </div>
        <div>
          {getCorners.status === 200 && cornerVisible == true ? (
            getCorners.data.timestamps.map((time) => (
              <button onClick={() => ref.current.seekTo(time)}>
                Seek to {time}
              </button>
            ))
          ) : (
            <h3></h3>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
