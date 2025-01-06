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
    <div id="download_page">
      <img id="download_image" src="waveform-icon.svg" alt="SoundWave" />
      <button onClick={handleDownload} disabled={!resultZip} id='download_button'>
        Download ZIP
      </button>
    </div>
  );
};

export default DownloadResult;
