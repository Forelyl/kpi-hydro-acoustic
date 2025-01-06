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
import { Provider } from 'react-redux';
import store from './store/store';

const router = createBrowserRouter([
  {
    path: '/',
    element: <LayoutWithHeader />,
    children: [
      { index: true, element: <AddFilePage /> },
      { path: 'about', element: <AboutPage /> },
      { path: 'pipeline', element: <PipelinePage /> },
      { path: 'download', element: <DownloadResultPage /> }
    ]
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </StrictMode>
);
