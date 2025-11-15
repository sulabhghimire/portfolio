
import './App.css';

import { ThemeProvider } from '../context/ThemeContext';
import AppLayout from '../components/AppLayout';

function App() {

  return (
    <ThemeProvider>
      <AppLayout/>
    </ThemeProvider>
  )
}

export default App
