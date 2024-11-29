import FileInputField from './FileInputField';
import SeparateTracksCheckbox from './SeparateTracksCheckbox';
import { Link } from 'react-router';
import { useAppSelector } from '../../store/store';

const AddFile = () => {
  const { file, separateTracks } = useAppSelector((state) => state.loadedFile);

  console.log(file, separateTracks);

  return (
    <main id="add_file_page">
      <FileInputField />
      <SeparateTracksCheckbox />
      <button disabled={!file} id="upload_button">
        Next
      </button>
      <Link to="about">?</Link>
    </main>
  );
};

export default AddFile;
