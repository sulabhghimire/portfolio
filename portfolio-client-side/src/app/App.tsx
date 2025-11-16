
import './App.css';

import { ThemeProvider } from '../context/ThemeContext';
import AppRouter from '../components/AppRouter';

function App() {

  return (
    <ThemeProvider>
      <AppRouter/>
    </ThemeProvider>
  )
}

export default App
