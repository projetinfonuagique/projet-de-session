// App.jsx
import { useState } from "react";

function App() {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const callApi = async (route) => {
    try {
      setLoading(true);
      const t0 = performance.now();
      const res = await fetch(`api/${route}`);
      const data = await res.json();
      const t1 = performance.now();
      setResult(
        `Route: /${route}\nStatus: Success\nTime: ${(t1 - t0).toFixed(2)}ms\nResponse: ${JSON.stringify(data)}`
      );
    } catch (e) {
      setResult(`Route: /${route}\nStatus: Error\n${e}`);
    } finally {
      setLoading(false);
    }
  };

  const runLoadTest = async (route, times = 10) => {
    for (let i = 0; i < times; i++) {
      await callApi(route);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>Test API</h1>
      <button onClick={() => callApi("compute")} disabled={loading}>Test CPU</button>
      <button onClick={() => callApi("io")} disabled={loading}>Test IO</button>
      <button onClick={() => callApi("status")} disabled={loading}>Status</button>
      <button onClick={() => callApi("crash")} disabled={loading}>Crash</button>
      <button onClick={() => runLoadTest("compute", 5)} disabled={loading}>Load Test (CPU x5)</button>
      <pre style={{ whiteSpace: "pre-wrap", marginTop: 20 }}>{result}</pre>
    </div>
  );
}

export default App;

