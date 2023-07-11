import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State variables for the video feed and attendance information
  const [videoSrc, setVideoSrc] = useState(null);
  const [attendance, setAttendance] = useState([]);

  // Function to start the face recognition attendance system
  const start = async () => {
    // Send a request to the Flask app to start the face recognition attendance system
    await fetch('http://127.0.0.1:5000/start');
  };

  // Function to update the video feed and attendance information
  const update = async () => {
    // Send a request to the Flask app to get the current video frame and attendance information
    const response = await fetch('http://127.0.0.1:5000/update');
    const data = await response.json();
    
    // Update the state variables with the received data
    setVideoSrc(data.video_src);
    setAttendance(data.attendance);
  };

  // Use the useEffect hook to call the update function repeatedly
  useEffect(() => {
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Face Recognition Attendance System</h1>
      <button onClick={start}>Take Attendance</button>
      <h2>Video Feed</h2>
      <img src={videoSrc} alt="Video feed" />
      <h2>Attendance</h2>
      <ul>
        {attendance.map((item, index) => (
          <li key={index}>{item.name} - {item.time}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
