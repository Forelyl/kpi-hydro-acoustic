import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router';
import LayoutWithHeader from './layouts/LayoutWithHeader';
import AddFile from './pages/AddFile';
import About from './pages/About';
import Pipeline from './pages/Pipeline';
import DownloadResult from './pages/DownloadResult';

const router = createBrowserRouter([
  {
    path: '/',
    element: <LayoutWithHeader />,
    children: [
      { index: true, element: <AddFile /> },
      { path: 'about', element: <About /> },
      { path: 'pipeline', element: <Pipeline /> },
      { path: 'downlaod', element: <DownloadResult /> }
    ]
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
