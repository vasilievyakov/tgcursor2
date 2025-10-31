import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import Layout from './components/Layout';
import ChannelsPage from './pages/ChannelsPage';
import PostsPage from './pages/PostsPage';
import './index.css';

// Определяем base path для GitHub Pages
const getBasePath = () => {
  // Для GitHub Pages используем имя репозитория
  if (import.meta.env.PROD) {
    // Проверяем, запущены ли мы на GitHub Pages
    const pathname = window.location.pathname;
    if (pathname.includes('/tgcursor2/')) {
      return '/tgcursor2';
    }
  }
  return '';
};

function App() {
  return (
    <Provider store={store}>
      <Router basename={getBasePath()}>
        <Layout>
          <Routes>
            <Route path="/" element={<ChannelsPage />} />
            <Route path="/posts" element={<PostsPage />} />
            <Route path="/posts/:channelId" element={<PostsPage />} />
          </Routes>
        </Layout>
      </Router>
    </Provider>
  );
}

export default App;
