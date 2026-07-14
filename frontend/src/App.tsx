import {useEffect, useState} from "react";
import {api} from "./services/api";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    api.get("/health").then((res) => {
      setMessage(res.data.service);
    });
  }, []);

  return (
    <div
      style={{
        height: "100vh",
        display: "grid",
        placeItems: "center",
        fontSize: "2rem",
        fontFamily: "sans-serif",
      }}
    >
      {message}
    </div>
  );
}

export default App;