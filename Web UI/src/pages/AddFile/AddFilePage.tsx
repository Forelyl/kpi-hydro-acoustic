import FileInputField from './FileInputField';
import SeparateTracksCheckbox from './SeparateTracksCheckbox';
import { Link } from 'react-router';
import { useAppDispatch, useAppSelector } from '../../store/store';
import Modal from '../../components/Modal/Modal';
import { resetError } from '../../store/loadedFileSlice';

const AddFile = () => {
  const dispatch = useAppDispatch();
  const { file, error } = useAppSelector((state) => state.loadedFile);

  return (
    <main id="add_file_page">
      <FileInputField />
      <SeparateTracksCheckbox />
      <button disabled={!file} id="upload_button">
        Next
      </button>
      <Link to="about">?</Link>
      <Modal open={!!error}>
        <h2>{error?.title}</h2>
        <p>{error?.message}</p>
        <button onClick={() => dispatch(resetError())}>OK</button>
      </Modal>
    </main>
  );
};

export default AddFile;
