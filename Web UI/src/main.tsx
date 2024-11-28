import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router';
import LayoutWithHeader from './layouts/LayoutWithHeader';
import {
  AboutPage,
  AddFilePage,
  DownloadResultPage,
  PipelinePage
} from './pages';
import './index.css';

const router = createBrowserRouter([
  {
    path: '/',
    element: <LayoutWithHeader />,
    children: [
      { index: true, element: <AddFilePage /> },
      { path: 'about', element: <AboutPage /> },
      { path: 'pipeline', element: <PipelinePage /> },
      { path: 'downlaod', element: <DownloadResultPage /> }
    ]
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
