import { useAppSelector } from '../store/store';

interface Props {
  zipFileName?: string;
}

const DownloadResult = ({ zipFileName = 'results.zip' }: Props) => {
  const { resultZip } = useAppSelector((state) => state.loadedFile);

  const handleDownload = () => {
    if (resultZip) {
      const url = window.URL.createObjectURL(resultZip);
      const a = document.createElement('a');
      a.href = url;
      a.download = zipFileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    }
  };

  return (
    <div id="download_page" style={{ textAlign: 'center', margin: '20px' }}>
      <img src="waveform-icon.svg" alt="SoundWave" />
      <button onClick={handleDownload} disabled={!resultZip}>
        {resultZip ? 'Download ZIP' : 'Loading...'}
      </button>
    </div>
  );
};

export default DownloadResult;
