import logo from "./logo.svg";
import "./App.css";
import React, { useEffect, useState } from "react";
import ReactPlayer from "react-player";
import axios from "axios";
import CornerVideo from "./media/vid2.mp4";
import CardVideo from "./media/cardvid.mp4";

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
  };
  const handleCard = (e) => {
    e.preventDefault();
    setCardVisible(true);
  };

  return (
    <div className='App'>
      <header className='App-header'>
        {/* <img src={logo} className='App-logo' alt='logo' />
        <p>React + Flask Tutorial</p> */}
        <button onClick={() => console.log("clicked")}>
          Upload your clip!
        </button>
        <button onClick={handleCorner}>Get Corner Timestamps</button>
        <ReactPlayer ref={ref} url={CornerVideo} controls={true} />
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
        <button onClick={handleCard}>Get Card Timestamps</button>
        <ReactPlayer ref={cardVideo} url={CardVideo} controls={true} />
        <div>
          {getCorners.status === 200 && cardVisible == true ? (
            getCards.data.timestamps.map((time) => (
              <button onClick={() => cardVideo.current.seekTo(time)}>
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
